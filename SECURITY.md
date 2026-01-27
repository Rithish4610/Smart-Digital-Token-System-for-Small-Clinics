# Security Best Practices

## Overview
This document outlines security considerations for deploying the Smart Token System in production.

## Authentication & Authorization

### Current Implementation
- Patient verification using token number + last 4 digits of phone
- Simple token-based access for patient status pages

### Recommendations for Production

1. **Implement JWT Tokens**
   ```python
   from jose import JWTError, jwt
   from datetime import datetime, timedelta

   SECRET_KEY = "your-secret-key-here"
   ALGORITHM = "HS256"

   def create_access_token(data: dict):
       to_encode = data.copy()
       expire = datetime.utcnow() + timedelta(hours=24)
       to_encode.update({"exp": expire})
       return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   ```

2. **Add Rate Limiting**
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter

   @app.post("/api/register")
   @limiter.limit("10/minute")
   async def register_patient(...):
       ...
   ```

3. **Implement CORS Properly**
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourclinic.com"],  # Specific origins only
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   ```

## Data Protection

### Database Security

1. **Encrypt Sensitive Data**
   - Encrypt phone numbers at rest
   - Use SQLCipher for encrypted SQLite

2. **Regular Backups**
   ```bash
   # Automated backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   cp clinic.db backups/clinic_$DATE.db
   ```

3. **Access Control**
   - Limit database file permissions
   - Use separate database user with minimal privileges

### Input Validation

1. **Sanitize All Inputs**
   ```python
   from pydantic import BaseModel, validator

   class PatientCreate(BaseModel):
       name: str
       phone: str

       @validator('name')
       def name_must_be_valid(cls, v):
           if not v.strip():
               raise ValueError('Name cannot be empty')
           if len(v) > 100:
               raise ValueError('Name too long')
           return v.strip()
   ```

2. **Prevent SQL Injection**
   - Always use parameterized queries (already implemented)
   - Never concatenate user input into SQL

## Network Security

### HTTPS/TLS

1. **Use Reverse Proxy**
   ```nginx
   # Nginx configuration
   server {
       listen 443 ssl;
       server_name yourclinic.com;

       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. **Force HTTPS**
   ```python
   from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
   app.add_middleware(HTTPSRedirectMiddleware)
   ```

### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP (redirect to HTTPS)
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

## Session Management

### Secure Cookies

```python
from fastapi import Response

response.set_cookie(
    key="session",
    value=token,
    httponly=True,  # Prevent XSS
    secure=True,    # HTTPS only
    samesite="strict"  # CSRF protection
)
```

### Session Timeout

```python
# Implement session expiry
SESSION_TIMEOUT = 3600  # 1 hour

def verify_session(token: str):
    # Check if session is still valid
    if session_expired(token):
        raise HTTPException(status_code=401)
```

## SMS/WhatsApp Security

### Twilio Best Practices

1. **Secure Credentials**
   - Never commit credentials to git
   - Use environment variables
   - Rotate credentials regularly

2. **Validate Phone Numbers**
   ```python
   from twilio.rest import Client

   def validate_phone(phone: str):
       client = Client(TWILIO_SID, TWILIO_TOKEN)
       try:
           number = client.lookups.phone_numbers(phone).fetch()
           return number.phone_number
       except:
           raise ValueError("Invalid phone number")
   ```

## Logging & Monitoring

### Security Logging

```python
import logging

logging.basicConfig(
    filename='security.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log security events
logging.info(f"Patient login attempt: {patient_id}")
logging.warning(f"Failed login: {patient_id}")
```

### Monitor for Attacks

- Track failed login attempts
- Alert on unusual patterns
- Log all API access

## Deployment Checklist

- [ ] Change default secret keys
- [ ] Enable HTTPS
- [ ] Set up firewall
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Encrypt sensitive data
- [ ] Set up automated backups
- [ ] Configure logging
- [ ] Update dependencies
- [ ] Remove debug mode
- [ ] Set secure cookie flags
- [ ] Implement CORS properly
- [ ] Add security headers
- [ ] Test for vulnerabilities

## Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourclinic.com", "*.yourclinic.com"]
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

## Regular Maintenance

1. **Update Dependencies**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Security Audits**
   ```bash
   pip install safety
   safety check
   ```

3. **Penetration Testing**
   - Test for common vulnerabilities
   - Use tools like OWASP ZAP

## Incident Response

1. **Have a plan** for security breaches
2. **Backup regularly** and test restores
3. **Document** all security incidents
4. **Update** security measures based on incidents

---

**Remember:** Security is an ongoing process, not a one-time setup!
