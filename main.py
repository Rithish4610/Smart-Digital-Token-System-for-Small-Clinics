import os
import io
import base64
from datetime import datetime
from typing import List, Optional

import qrcode
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# --- Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./clinic.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    token_number = Column(Integer)
    status = Column(String, default="waiting") # waiting, calling, completed
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- Twilio Setup ---
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

def send_sms(to_phone: str, message: str):
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_PHONE]):
        print(f"SMS MOCK (No Credentials): To {to_phone} -> {message}")
        return
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=to_phone
        )
        print(f"SMS SENT: To {to_phone}")
    except Exception as e:
        print(f"SMS FAILED: {str(e)}")

# --- FastAPI App ---
app = FastAPI(title="Smart Clinic Token System")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
async def patient_login_page(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    # This page will now be a login screen if not verified
    return templates.TemplateResponse("patient_login.html", {"request": request, "patient_id": patient_id})

@app.get("/patient/{patient_id}/status", response_class=HTMLResponse)
async def patient_status_page(request: Request, patient_id: int, token: str = None, db: Session = Depends(get_db)):
    # Simple token validation (in a real app, use JWT)
    if not token or token != f"verified_{patient_id}":
        return templates.TemplateResponse("patient_login.html", {"request": request, "patient_id": patient_id, "error": "Please login first"})
        
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    return templates.TemplateResponse("patient.html", {"request": request, "patient": patient})

@app.post("/api/verify-patient")
async def verify_patient(patient_id: int = Form(...), token_number: int = Form(...), last_4_digits: str = Form(...), db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Patient not found"})
        
    # Check token and last 4 digits of phone
    if patient.token_number == token_number and patient.phone[-4:] == last_4_digits:
        return {"success": True, "access_token": f"verified_{patient_id}"}
    else:
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})

# --- API Endpoints ---
@app.post("/api/register")
async def register_patient(data: PatientCreate, request: Request, db: Session = Depends(get_db)):
    # Calculate next token (simplified for daily reset in production)
    last_patient = db.query(Patient).order_by(Patient.id.desc()).first()
    next_token = (last_patient.token_number + 1) if last_patient else 1
    
    new_patient = Patient(name=data.name, phone=data.phone, token_number=next_token)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    # Generate QR Code
    base_url = str(request.base_url).rstrip('/')
    qr_url = f"{base_url}/patient/{new_patient.id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    # Send SMS Notification
    sms_message = f"Hello {data.name}, your token is #{next_token}. Track your turn live: {qr_url}"
    send_sms(data.phone, sms_message)
    
    return {
        "id": new_patient.id,
        "token": next_token,
        "qr_code": img_str,
        "qr_url": qr_url
    }

@app.get("/api/queue")
async def get_queue(db: Session = Depends(get_db)):
    waiting = db.query(Patient).filter(Patient.status == "waiting").order_by(Patient.token_number).all()
    calling = db.query(Patient).filter(Patient.status == "calling").first()
    completed_today = db.query(Patient).filter(Patient.status == "completed").count()
    
    return {
        "waiting": [{"id": p.id, "name": p.name, "token": p.token_number} for p in waiting],
        "current": {"name": calling.name, "token": calling.token_number} if calling else None,
        "count": len(waiting),
        "completed_count": completed_today
    }

@app.post("/api/next")
async def call_next(db: Session = Depends(get_db)):
    # 1. Complete current calling patient
    current = db.query(Patient).filter(Patient.status == "calling").first()
    if current:
        current.status = "completed"
    
    # 2. Call next waiting patient
    next_patient = db.query(Patient).filter(Patient.status == "waiting").order_by(Patient.token_number).first()
    if next_patient:
        next_patient.status = "calling"
        db.commit()
        return {"success": True, "patient": {"name": next_patient.name, "token": next_patient.token_number}}
    
    db.commit()
    return {"success": True, "message": "Queue empty"}

@app.get("/api/patient-status/{patient_id}")
async def get_patient_status(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    # Find how many people are ahead
    ahead = db.query(Patient).filter(Patient.status == "waiting", Patient.token_number < patient.token_number).count()
    
    current_calling = db.query(Patient).filter(Patient.status == "calling").first()
    
    return {
        "status": patient.status,
        "token": patient.token_number,
        "people_ahead": ahead,
        "current_token": current_calling.token_number if current_calling else "N/A"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
