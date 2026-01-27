# 🏥 Smart Digital Token System for Small Clinics

> A modern, low-cost solution for managing patient queues efficiently with a beautiful, premium UI.

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## ✨ Features

- 🎫 **Easy Registration**: Quick patient entry via modern reception dashboard
- 📱 **QR Code Tokens**: Patients scan QR codes to track their turn live on their phones
- 👨‍⚕️ **Doctor Dashboard**: Simple "Next" button interface for doctors to manage the flow
- 📺 **Public Display**: High-visibility queue display with voice announcements for the waiting area
- 🔒 **Offline First**: Runs on a local LAN; only uses internet for optional SMS alerts
- 🎨 **Premium UI**: Modern, gradient-based design with smooth animations and glassmorphism effects
- 📊 **Real-time Updates**: Live queue status updates every few seconds
- 🔔 **Notifications**: Browser notifications when it's your turn

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python) - Fast, modern web framework
- **Database**: SQLite - Lightweight, serverless database
- **Frontend**: HTML5, CSS3 (Modern Vanilla), JavaScript
- **QR Generation**: Python-qrcode library
- **UI Design**: Custom CSS with gradients, animations, and glassmorphism
- **SMS (Optional)**: Twilio integration for real SMS notifications

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the System

Open your browser and navigate to:

- 🏠 **Home**: `http://localhost:8000/`
- 📋 **Reception (Registration)**: `http://localhost:8000/reception`
- 👨‍⚕️ **Doctor Dashboard**: `http://localhost:8000/doctor`
- 📺 **Public Display**: `http://localhost:8000/display`
- 🎫 **Patient Tracking**: Scan QR code or visit patient link

## 📱 SMS Notifications Setup (Optional)

To send real SMS messages to patients' phones, configure Twilio:

1. **Sign Up**: Go to [Twilio.com](https://www.twilio.com/) and create a free account
2. **Get a Number**: Obtain a free Trial Phone Number from the dashboard
3. **Get Credentials**: Copy your **Account SID** and **Auth Token**
4. **Configure App**: 
   - Create a `.env` file in the project root
   - Add your credentials:
     ```ini
     TWILIO_ACCOUNT_SID=AC... (your account SID)
     TWILIO_AUTH_TOKEN=... (your auth token)
     TWILIO_PHONE_NUMBER=+1234567890 (your Twilio number)
     ```
5. **Restart**: Run `python main.py` again

> **Note:** Without these keys, the system runs in "Mock Mode" - it simulates SMS by printing to the terminal and providing a tracking link in the modal.

## 🔄 Workflow

1. **Receptionist** registers the patient with name and phone number
2. System generates a **Token Number & QR Code**
3. **Patient** scans the QR code to track their position in real-time
4. **Doctor** clicks "Call Next" to summon the next patient
5. **Public Display** updates instantly and announces the token number via voice
6. Patient receives browser notification when it's their turn

## 🎨 UI Features

- ✅ Modern gradient backgrounds
- ✅ Smooth micro-animations
- ✅ Glassmorphism effects
- ✅ Premium color palette
- ✅ Professional typography (Outfit & Inter fonts)
- ✅ Interactive hover states
- ✅ Responsive design for all devices
- ✅ Animated transitions
- ✅ Toast notifications
- ✅ Ripple button effects

## 📂 Project Structure

```
Smart-Digital-Token-System-for-Small-Clinics/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── clinic.db              # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── reception.html     # Registration page
│   ├── doctor.html        # Doctor dashboard
│   ├── display.html       # Public display screen
│   ├── patient.html       # Patient status page
│   └── patient_login.html # Patient verification
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Premium CSS styles
    └── js/
        └── app.js         # Interactive JavaScript

```

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ for modern healthcare facilities

---

**Made with Python & FastAPI** | **Designed for Efficiency** | **Built for Small Clinics**
