# Smart Token System - Installation & Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** (Check with `python --version`)
- **pip** (Python package manager)
- **Git** (for version control)

## 🚀 Quick Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/Smart-Digital-Token-System-for-Small-Clinics.git
cd Smart-Digital-Token-System-for-Small-Clinics
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment (Optional)

For SMS notifications, create a `.env` file:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` and add your Twilio credentials (optional).

### Step 5: Run the Application

```bash
python main.py
```

The application will start at `http://localhost:8000`

## 🌐 Accessing the System

Once running, open your browser and visit:

- **Home Page**: http://localhost:8000
- **Reception**: http://localhost:8000/reception
- **Doctor Dashboard**: http://localhost:8000/doctor
- **Public Display**: http://localhost:8000/display
- **Statistics**: http://localhost:8000/statistics

## 📱 Network Access (LAN)

To access from other devices on your network:

1. Find your computer's IP address:
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - **Linux/Mac**: `ifconfig` or `ip addr`

2. Other devices can access at: `http://YOUR_IP:8000`
   - Example: `http://192.168.1.100:8000`

## 🔧 Troubleshooting

### Port Already in Use
If port 8000 is busy, edit `main.py` and change:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
```

### Database Issues
Delete `clinic.db` and restart the application to reset the database.

### Module Not Found
Ensure you're in the virtual environment and run:
```bash
pip install -r requirements.txt --upgrade
```

## 🎨 Customization

### Change Clinic Name
Edit `config.env`:
```ini
CLINIC_NAME=Your Clinic Name
```

### Change Colors
Edit `static/css/style.css` and modify the `:root` variables:
```css
:root {
    --primary: #06d6a0;  /* Your primary color */
    --secondary: #5e60ce; /* Your secondary color */
}
```

### Adjust Wait Time Calculation
Edit `config.env`:
```ini
AVG_CONSULTATION_TIME=10  # Minutes per patient
```

## 📊 Database Backup

The SQLite database (`clinic.db`) contains all patient data. Back it up regularly:

```bash
# Windows
copy clinic.db clinic_backup_%date%.db

# Linux/Mac
cp clinic.db clinic_backup_$(date +%Y%m%d).db
```

## 🔐 Security Recommendations

For production use:
1. Enable HTTPS with a reverse proxy (nginx/Apache)
2. Set up firewall rules
3. Use strong authentication
4. Regular database backups
5. Update dependencies regularly

## 📞 Support

For issues or questions:
- Check the README.md
- Review the CHANGELOG.md
- Open an issue on GitHub

## 🎉 You're Ready!

Your Smart Token System is now set up and running. Enjoy efficient queue management!

---

**Next Steps:**
1. Register your first patient at `/reception`
2. Test the doctor dashboard at `/doctor`
3. View the public display at `/display`
4. Check analytics at `/statistics`
