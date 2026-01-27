# Frequently Asked Questions (FAQ)

## General Questions

### What is the Smart Digital Token System?
The Smart Digital Token System is a queue management solution designed for small clinics. It helps manage patient flow efficiently by providing digital tokens, real-time status updates, and automated notifications.

### Who can use this system?
- **Small to medium-sized clinics**
- **Dental practices**
- **Diagnostic centers**
- **Outpatient departments**
- Any healthcare facility with a waiting queue

### How much does it cost?
The software is **completely free and open source** (MIT License). You only need:
- A computer to run the server
- Devices to access the system (existing computers/tablets)
- Optional: Twilio account for SMS ($0.0075 per SMS)

---

## Technical Questions

### What are the system requirements?
- **Server**: Any computer with Python 3.8+ (Windows/Linux/Mac)
- **Network**: Local WiFi/LAN
- **Clients**: Any device with a web browser
- **Storage**: Minimal (SQLite database)

### Can it work offline?
Yes! The system works entirely on your local network without internet. Internet is only needed for:
- SMS notifications (optional)
- Initial software download

### How many patients can it handle?
The system can easily handle:
- **100+ patients per day**
- **20+ concurrent waiting patients**
- Multiple doctors/departments

### What browsers are supported?
All modern browsers:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

---

## Setup & Installation

### How long does setup take?
- **Basic setup**: 10-15 minutes
- **With SMS**: Additional 15 minutes
- **Network configuration**: 5-10 minutes

### Do I need technical knowledge?
Basic computer skills are sufficient. The installation guide provides step-by-step instructions.

### Can I use my existing computer?
Yes! Any computer that can run Python will work. You can even use an old laptop as a dedicated server.

### How do I update the system?
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## Features & Usage

### How do patients track their status?
Patients can:
1. **Scan QR code** from their registration receipt
2. **Click SMS link** (if SMS enabled)
3. **Enter token number** on the patient portal

### Can I customize the design?
Yes! You can:
- Change colors in `static/css/style.css`
- Modify clinic name in `config.env`
- Adjust wait time calculations
- Customize all text and labels

### Does it support multiple doctors?
Currently, it's designed for single-queue systems. For multiple doctors:
- Run separate instances on different ports
- Or modify the code to add department/doctor fields

### Can patients print their tokens?
Yes! The system includes print-friendly token receipts with QR codes.

---

## SMS & Notifications

### Is SMS required?
No, SMS is completely optional. The system works perfectly without it using:
- QR codes
- Direct links
- Manual token checking

### Which SMS service do you recommend?
**Twilio** is recommended because:
- Free trial with $15 credit
- Easy setup
- Reliable delivery
- WhatsApp support

### How much do SMS cost?
- **Twilio**: ~$0.0075 per SMS
- **100 patients/day**: ~$0.75/day or $22.50/month
- **Free trial**: Covers ~2000 messages

### Can I use WhatsApp instead of SMS?
Yes! Twilio supports WhatsApp. Patients need to join your WhatsApp sandbox first.

---

## Display & Hardware

### What should I use for the public display?
Options:
- **TV with HDMI**: Connect to computer/Raspberry Pi
- **Old monitor**: Repurpose existing hardware
- **Tablet**: Mount on wall in kiosk mode
- **Smart TV**: Built-in browser

### How do I prevent the display from sleeping?
- **Windows**: Settings → Power → Never sleep
- **Linux**: Disable screensaver
- **Browser**: Use extensions like "Keep Awake"

### Can I use tablets for doctors?
Absolutely! iPads, Android tablets, or any device with a browser works perfectly.

---

## Data & Privacy

### Where is patient data stored?
All data is stored locally in `clinic.db` (SQLite database) on your server. Nothing is sent to external servers (except SMS if configured).

### How do I backup data?
```bash
# Manual backup
cp clinic.db backups/clinic_backup.db

# Automated (add to cron/Task Scheduler)
cp clinic.db backups/clinic_$(date +%Y%m%d).db
```

### Is patient data secure?
- Data stays on your local network
- No cloud storage
- You control all data
- For production, follow the SECURITY.md guide

### How long is data kept?
By default, data is kept indefinitely. You can:
- Manually delete old records
- Implement auto-cleanup (modify code)
- Reset daily (for privacy)

---

## Troubleshooting

### "Can't access from other devices"
1. Check firewall settings
2. Ensure all devices on same network
3. Verify server IP address
4. Try `http://SERVER_IP:8000` instead of `localhost`

### "Port 8000 already in use"
Change port in `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8080)
```

### "SMS not sending"
1. Verify Twilio credentials in `.env`
2. Check Twilio account balance
3. Ensure phone numbers include country code
4. Check Twilio dashboard for errors

### "Database locked" error
- Close other instances of the application
- Check file permissions
- Restart the application

---

## Customization

### Can I change the wait time calculation?
Yes! Edit `config.env`:
```ini
AVG_CONSULTATION_TIME=10  # Minutes per patient
```

### How do I change the clinic name?
Edit `config.env`:
```ini
CLINIC_NAME=Your Clinic Name
```

### Can I add more languages?
Yes, but requires code modification. All text is in HTML templates - translate and create language variants.

### Can I integrate with my existing system?
Yes! Use the REST API (see API.md) to:
- Register patients from your system
- Get queue status
- Integrate with EMR/HIS

---

## Support & Community

### Where can I get help?
1. Check this FAQ
2. Read the documentation (README.md, INSTALL.md)
3. Open an issue on GitHub
4. Check existing issues for solutions

### Can I contribute?
Yes! See CONTRIBUTING.md for guidelines.

### Is commercial use allowed?
Yes! The MIT license allows commercial use.

### Can I hire someone to set it up?
Yes, you can hire a developer to:
- Set up the system
- Customize features
- Provide training
- Ongoing support

---

## Future Plans

### What features are planned?
- Multi-doctor support
- Appointment scheduling
- Patient history
- Analytics dashboard enhancements
- Mobile apps
- Multi-language support

### Can I request features?
Yes! Open a feature request on GitHub.

---

**Still have questions?** Open an issue on GitHub or check the documentation!
