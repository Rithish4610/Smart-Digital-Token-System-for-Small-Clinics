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

## 📱 How to Enable SMS Notifications
To send real SMS messages to patients' phones (e.g., to Google Messages), you need a configured SMS gateway.

The code is pre-configured for **Twilio**, which offers a free trial.

1.  **Sign Up:** Go to [Twilio.com](https://www.twilio.com/) and create a free account.
2.  **Get a Number:** Get a free Trial Phone Number from their dashboard.
3.  **Get Credentials:** Copy your **Account SID** and **Auth Token**.
4.  **Configure App:**
    - Open the `.env` file in this folder.
    - Replace the placeholder text with your actual keys:
      ```ini
      TWILIO_ACCOUNT_SID=AC... (your long ID)
      TWILIO_AUTH_TOKEN=... (your token)
      TWILIO_PHONE_NUMBER=+1234567890 (your Twilio number)
      ```
5.  **Restart:** Run `python main.py` again.

> **Note:** Without these keys, the system runs in "Mock Mode". It will simulate sending an SMS by printing it to the terminal and providing a "Tracking Link" in the modal.

## Workflow
1. **Receptionist** registers the patient.
2. A **Token & QR Code** is generated.
3. **Patient** scans the QR code to see "People ahead of me" and "Serving now".
4. **Doctor** clicks "Call Next".
5. **Public Display** updates instantly and **announces** the token number.
**PUBLIC**
