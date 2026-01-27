# Deployment Guide - Smart Token System

## Deployment Options

### Option 1: Local Network (Recommended for Small Clinics)

#### Requirements
- Computer/Server running 24/7
- Local network (WiFi/LAN)
- Python 3.8+

#### Steps

1. **Install on Server**
   ```bash
   git clone <repository-url>
   cd Smart-Digital-Token-System-for-Small-Clinics
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. **Configure for Network Access**
   
   Edit `main.py`:
   ```python
   uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
   ```

3. **Find Server IP**
   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

4. **Access from Devices**
   - Reception: `http://SERVER_IP:8000/reception`
   - Doctor: `http://SERVER_IP:8000/doctor`
   - Display: `http://SERVER_IP:8000/display`

5. **Auto-start on Boot**

   **Windows (Task Scheduler):**
   - Create batch file `start_clinic.bat`:
     ```batch
     cd C:\path\to\clinic
     venv\Scripts\python.exe main.py
     ```
   - Add to Task Scheduler to run at startup

   **Linux (systemd):**
   ```bash
   sudo nano /etc/systemd/system/clinic.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Smart Token System
   After=network.target

   [Service]
   User=youruser
   WorkingDirectory=/path/to/clinic
   ExecStart=/path/to/clinic/venv/bin/python main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable:
   ```bash
   sudo systemctl enable clinic
   sudo systemctl start clinic
   ```

---

### Option 2: Cloud Deployment (Heroku)

#### Steps

1. **Create `Procfile`**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Create `runtime.txt`**
   ```
   python-3.10.0
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-clinic-name
   git push heroku main
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set TWILIO_ACCOUNT_SID=your_sid
   heroku config:set TWILIO_AUTH_TOKEN=your_token
   ```

---

### Option 3: VPS Deployment (DigitalOcean, AWS, etc.)

#### Steps

1. **Create VPS**
   - Ubuntu 20.04 LTS recommended
   - Minimum 1GB RAM

2. **SSH into Server**
   ```bash
   ssh root@your_server_ip
   ```

3. **Install Dependencies**
   ```bash
   apt update
   apt install python3 python3-pip python3-venv nginx
   ```

4. **Clone and Setup**
   ```bash
   cd /var/www
   git clone <repository-url> clinic
   cd clinic
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Nginx**
   ```bash
   nano /etc/nginx/sites-available/clinic
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }

       location /static {
           alias /var/www/clinic/static;
       }
   }
   ```

   Enable:
   ```bash
   ln -s /etc/nginx/sites-available/clinic /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx
   ```

6. **Setup SSL (Let's Encrypt)**
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d your_domain.com
   ```

7. **Create Systemd Service**
   (Same as Option 1 Linux steps)

---

### Option 4: Docker Deployment

#### Create `Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./clinic.db:/app/clinic.db
    environment:
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - TWILIO_PHONE_NUMBER=${TWILIO_PHONE_NUMBER}
    restart: unless-stopped
```

#### Deploy

```bash
docker-compose up -d
```

---

## Post-Deployment

### 1. Test All Features
- [ ] Patient registration
- [ ] QR code generation
- [ ] Doctor dashboard
- [ ] Public display
- [ ] Patient status tracking
- [ ] SMS notifications (if configured)

### 2. Configure Devices

**Reception Computer:**
- Bookmark: `http://SERVER_IP:8000/reception`
- Keep browser open
- Disable screen sleep

**Doctor Computer/Tablet:**
- Bookmark: `http://SERVER_IP:8000/doctor`
- Enable notifications

**Public Display (TV/Monitor):**
- Bookmark: `http://SERVER_IP:8000/display`
- Set to fullscreen (F11)
- Disable screensaver

### 3. Train Staff

- Show reception how to register patients
- Demonstrate doctor dashboard
- Explain patient tracking

### 4. Monitor & Maintain

```bash
# Check logs
tail -f clinic_system.log

# Monitor resource usage
htop

# Backup database
cp clinic.db backups/clinic_$(date +%Y%m%d).db
```

---

## Troubleshooting

### Can't Access from Other Devices
- Check firewall settings
- Ensure devices on same network
- Verify server IP address

### Application Crashes
- Check logs for errors
- Ensure database file has write permissions
- Verify all dependencies installed

### SMS Not Working
- Verify Twilio credentials
- Check Twilio account balance
- Ensure phone numbers include country code

---

## Performance Optimization

### For High Traffic

1. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Enable Caching**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.inmemory import InMemoryBackend

   @app.on_event("startup")
   async def startup():
       FastAPICache.init(InMemoryBackend())
   ```

3. **Database Optimization**
   - Add indexes to frequently queried columns
   - Consider PostgreSQL for larger deployments

---

## Scaling

For multiple clinics or locations:

1. **Multi-tenant Setup**
   - Add clinic_id to database
   - Separate queues per clinic

2. **Load Balancing**
   - Use nginx load balancer
   - Deploy multiple instances

3. **Centralized Database**
   - Use PostgreSQL/MySQL
   - Enable remote access

---

**Need Help?** Check the documentation or open an issue on GitHub.
