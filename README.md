# Smart Digital Token System for Small Clinics

A modern, low-cost solution for managing patient queues efficiently.

## Features
- **Easy Registration**: Quick patient entry via reception dashboard.
- **QR Code Tokens**: Patients scan a QR code to track their turn live on their phones.
- **Doctor Dashboard**: Simple "Next" button interface for doctors to manage the flow.
- **Public Display**: High-visibility queue display with voice announcements for the waiting area.
- **Offline First**: Runs on a local LAN; only uses internet for (optional) SMS alerts.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **QR Generation**: Python-qrcode

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```
   Or using uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access Dashboards**:
   - **Reception (Registration)**: `http://localhost:8000/`
   - **Doctor Dashboard**: `http://localhost:8000/doctor`
   - **Public Display**: `http://localhost:8000/display`

## Workflow
1. **Receptionist** registers the patient.
2. A **Token & QR Code** is generated.
3. **Patient** scans the QR code to see "People ahead of me" and "Serving now".
4. **Doctor** clicks "Call Next".
5. **Public Display** updates instantly and **announces** the token number.
