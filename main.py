import os
import io
import base64
import sqlite3
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

import qrcode
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from fast2sms_client import send_sms

load_dotenv()

# --- Database Setup ---
DB_NAME = "clinic.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            token_number INTEGER,
            status TEXT DEFAULT 'waiting',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

def get_db_conn():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Allow accessing columns by name
    try:
        yield conn
    finally:
        conn.close()

# --- FastAPI App ---
app = FastAPI(title="Smart Clinic Token System")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Schemas ---
class PatientCreate(BaseModel):
    name: str
    phone: str

# --- Pages ---
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Home page with navigation to all system features"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reception")
async def reception_page():
    return RedirectResponse(url="/")

@app.get("/doctor")
async def doctor_page():
    return RedirectResponse(url="/")

@app.get("/display", response_class=HTMLResponse)
async def display_page(request: Request):
    return templates.TemplateResponse("display.html", {"request": request})

@app.get("/patient/{patient_id}", response_class=HTMLResponse)
async def patient_login_page(request: Request, patient_id: int, conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    # This page will now be a login screen if not verified
    return templates.TemplateResponse("patient_login.html", {"request": request, "patient_id": patient_id})

@app.get("/patient/{patient_id}/status", response_class=HTMLResponse)
async def patient_status_page(request: Request, patient_id: int, token: str = None, conn: sqlite3.Connection = Depends(get_db_conn)):
    # Simple token validation (in a real app, use JWT)
    if not token or token != f"verified_{patient_id}":
        return templates.TemplateResponse("patient_login.html", {"request": request, "patient_id": patient_id, "error": "Please login first"})
        
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    return templates.TemplateResponse("patient.html", {"request": request, "patient": patient})

@app.post("/api/verify-patient")
async def verify_patient(patient_id: int = Form(...), token_number: int = Form(...), last_4_digits: str = Form(...), conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Patient not found"})
        
    # Check token and last 4 digits of phone
    # patient is a Row object, access by key
    if patient['token_number'] == token_number and patient['phone'][-4:] == last_4_digits:
        return {"success": True, "access_token": f"verified_{patient_id}"}
    else:
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})

# --- API Endpoints ---
@app.post("/api/register")
async def register_patient(data: PatientCreate, request: Request, conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    # Calculate next token (simplified for daily reset in production)
    cursor.execute("SELECT token_number FROM patients ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    next_token = (last_row['token_number'] + 1) if last_row else 1
    
    cursor.execute("INSERT INTO patients (name, phone, token_number, status, created_at) VALUES (?, ?, ?, 'waiting', ?)",
                   (data.name, data.phone, next_token, datetime.utcnow()))
    conn.commit()
    new_id = cursor.lastrowid
    
    # Generate QR Code
    base_url = str(request.base_url).rstrip('/')
    qr_url = f"{base_url}/patient/{new_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    # Send SMS Notification
    sms_message = f"Hello {data.name}, your token is #{next_token}. Track your turn live: {qr_url}"
    sms_success, sms_status = send_sms(data.phone, sms_message)
    
    return {
        "id": new_id,
        "token": next_token,
        "qr_code": img_str,
        "qr_url": qr_url,
        "sms_success": sms_success,
        "sms_status": sms_status
    }

@app.get("/api/queue")
async def get_queue(conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE status = 'waiting' ORDER BY token_number")
    waiting = cursor.fetchall()
    
    cursor.execute("SELECT * FROM patients WHERE status = 'calling' LIMIT 1")
    calling = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as count FROM patients WHERE status = 'completed'")
    completed_today = cursor.fetchone()['count']
    
    return {
        "waiting": [{"id": p['id'], "name": p['name'], "token": p['token_number']} for p in waiting],
        "current": {"name": calling['name'], "token": calling['token_number']} if calling else None,
        "count": len(waiting),
        "completed_count": completed_today
    }

@app.post("/api/next")
async def call_next(conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    # 1. Complete current calling patient
    cursor.execute("UPDATE patients SET status = 'completed' WHERE status = 'calling'")
    
    # 2. Call next waiting patient
    cursor.execute("SELECT * FROM patients WHERE status = 'waiting' ORDER BY token_number LIMIT 1")
    next_patient = cursor.fetchone()
    
    if next_patient:
        cursor.execute("UPDATE patients SET status = 'calling' WHERE id = ?", (next_patient['id'],))
        conn.commit()
        return {"success": True, "patient": {"name": next_patient['name'], "token": next_patient['token_number']}}
    
    conn.commit()
    return {"success": True, "message": "Queue empty"}

@app.get("/api/patient-status/{patient_id}")
async def get_patient_status(patient_id: int, conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    # Find how many people are ahead
    cursor.execute("SELECT COUNT(*) as count FROM patients WHERE status = 'waiting' AND token_number < ?", (patient['token_number'],))
    ahead = cursor.fetchone()['count']
    
    cursor.execute("SELECT * FROM patients WHERE status = 'calling' LIMIT 1")
    current_calling = cursor.fetchone()
    
    return {
        "status": patient['status'],
        "token": patient['token_number'],
        "people_ahead": ahead,
        "current_token": current_calling['token_number'] if current_calling else "N/A"
    }

@app.get("/statistics", response_class=HTMLResponse)
async def statistics_page(request: Request):
    """Statistics dashboard page"""
    return templates.TemplateResponse("statistics.html", {"request": request})

@app.get("/api/statistics")
async def get_statistics(period: str = "today", conn: sqlite3.Connection = Depends(get_db_conn)):
    """Get comprehensive statistics with filtering"""
    cursor = conn.cursor()
    
    # Date Filtering Logic
    date_filter = "DATE(created_at) = DATE('now')"
    if period == "week":
        date_filter = "DATE(created_at) >= DATE('now', '-7 days')"
    elif period == "month":
        date_filter = "DATE(created_at) >= DATE('now', '-30 days')"
    elif period == "all":
        date_filter = "1=1"  # No filter

    # Total patients for period
    cursor.execute(f"SELECT COUNT(*) as count FROM patients WHERE {date_filter}")
    total = cursor.fetchone()['count']
    
    # Completed for period
    cursor.execute(f"SELECT COUNT(*) as count FROM patients WHERE status = 'completed' AND {date_filter}")
    completed = cursor.fetchone()['count']
    
    # Waiting now (Always current waiting queue, independent of history view usually, but helps context)
    # Actually, "Waiting" is a current state, so it shouldn't really be filtered by history, 
    # but for consistent "Totals" it makes sense to show how many *from that period* are waiting (if any still are).
    # However, usually "Waiting" implies "Currently in queue". 
    # Let's keep "Waiting" as "Current Realtime Queue" because that's what the card implies ⏳.
    cursor.execute("SELECT COUNT(*) as count FROM patients WHERE status = 'waiting'")
    waiting_now = cursor.fetchone()['count']
    
    # Average wait time (simplified - 5 mins per patient)
    avg_wait = waiting_now * 5
    
    # Hourly flow for period
    # For 'week'/'month'/'all', hourly flow might look messy if aggregated by hour of day across multiple days.
    # But for simplicity, let's just show graph of "Activity by Hour of Day" (Time distribution)
    # Or "Activity by Date" would be better for week/month?
    # Given the frontend chart calls it "Patient Flow Today" it implies hourly.
    # Let's keep it as "Hour of creation" to show peak times regardless of day for aggregate views.
    cursor.execute(f"""
        SELECT strftime('%H:00', created_at) as hour, COUNT(*) as count 
        FROM patients 
        WHERE {date_filter}
        GROUP BY hour
        ORDER BY hour
    """)
    hourly_flow = [{"hour": row['hour'], "count": row['count']} for row in cursor.fetchall()]
    
    # Peak hours (top 3)
    peak_hours = sorted(hourly_flow, key=lambda x: x['count'], reverse=True)[:3]
    peak_hours = [{"time": h['hour'], "count": h['count']} for h in peak_hours]
    
    return {
        "total": total,
        "completed": completed,
        "waiting": waiting_now,
        "avgWaitTime": avg_wait,
        "hourlyFlow": hourly_flow,
        "peakHours": peak_hours
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
