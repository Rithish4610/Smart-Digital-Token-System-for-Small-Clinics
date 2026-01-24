import os
import io
import base64
import sqlite3
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

import qrcode
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv();

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

# --- Twilio Setup ---
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

def send_sms(to_phone: str, message: str):
    # WhatsApp Sandbox: send WhatsApp message instead of SMS
    # Patient must join sandbox by sending 'join <sandbox-code>' to +14155238886
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_PHONE]) or \
       TWILIO_SID == "your_sid_here" or \
       TWILIO_TOKEN == "your_token_here" or \
       TWILIO_PHONE == "your_twilio_number_here":
        print(f"------------ MOCK WhatsApp (No Valid Credentials) ------------")
        print(f"To: whatsapp:{to_phone}")
        print(f"Message: {message}")
        print(f"-------------------------------------------------------------")
        return

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            body=message,
            from_=f"whatsapp:{TWILIO_PHONE}",
            to=f"whatsapp:{to_phone}"
        )
        print(f"WhatsApp SENT: To {to_phone}")
    except Exception as e:
        print(f"WhatsApp FAILED: {str(e)}")

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
async def reception_page(request: Request):
    return templates.TemplateResponse("reception.html", {"request": request})

@app.get("/doctor", response_class=HTMLResponse)
async def doctor_page(request: Request):
    return templates.TemplateResponse("doctor.html", {"request": request})

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
    
    # Send WhatsApp Notification
    whatsapp_instructions = ("To receive notifications, send 'join <your-sandbox-code>' to +14155238886 on WhatsApp if you haven't already.")
    sms_message = f"Hello {data.name}, your token is #{next_token}. Track your turn live: {qr_url}\n{whatsapp_instructions}"
    send_sms(data.phone, sms_message)
    
    return {
        "id": new_id,
        "token": next_token,
        "qr_code": img_str,
        "qr_url": qr_url
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
