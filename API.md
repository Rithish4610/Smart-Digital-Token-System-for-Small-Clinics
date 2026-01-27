# API Documentation - Smart Token System

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Register Patient
**POST** `/api/register`

Register a new patient and generate token.

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "id": 1,
  "token": 12,
  "qr_code": "base64_encoded_image",
  "qr_url": "http://localhost:8000/patient/1"
}
```

---

### 2. Get Queue Status
**GET** `/api/queue`

Get current queue information.

**Response:**
```json
{
  "waiting": [
    {"id": 1, "name": "John Doe", "token": 12}
  ],
  "current": {"name": "Jane Smith", "token": 11},
  "count": 5,
  "completed_count": 20
}
```

---

### 3. Call Next Patient
**POST** `/api/next`

Mark current patient as complete and call next.

**Response:**
```json
{
  "success": true,
  "patient": {"name": "John Doe", "token": 12}
}
```

---

### 4. Get Patient Status
**GET** `/api/patient-status/{patient_id}`

Get specific patient's status.

**Response:**
```json
{
  "status": "waiting",
  "token": 12,
  "people_ahead": 3,
  "current_token": 9
}
```

---

### 5. Verify Patient
**POST** `/api/verify-patient`

Verify patient credentials for login.

**Request Body (Form Data):**
```
patient_id: 1
token_number: 12
last_4_digits: 7890
```

**Response:**
```json
{
  "success": true,
  "access_token": "verified_1"
}
```

---

### 6. Get Statistics
**GET** `/api/statistics`

Get comprehensive statistics.

**Response:**
```json
{
  "total": 45,
  "completed": 30,
  "waiting": 5,
  "avgWaitTime": 25,
  "hourlyFlow": [
    {"hour": "09:00", "count": 5},
    {"hour": "10:00", "count": 8}
  ],
  "peakHours": [
    {"time": "10:00", "count": 8}
  ]
}
```

---

## Status Codes

- `200` - Success
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

## Error Response Format

```json
{
  "message": "Error description"
}
```

## Rate Limiting

Currently no rate limiting implemented.

## Authentication

Patient routes require verification token in query parameter:
```
/patient/1/status?token=verified_1
```

## WebSocket Support

Not currently implemented. All updates via polling.

## CORS

Configured to allow all origins in development.

---

## Example Usage

### JavaScript (Fetch API)

```javascript
// Register patient
const response = await fetch('/api/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'John Doe',
    phone: '+1234567890'
  })
});
const data = await response.json();
console.log('Token:', data.token);

// Get queue
const queue = await fetch('/api/queue');
const queueData = await queue.json();
console.log('Waiting:', queueData.count);
```

### Python (requests)

```python
import requests

# Register patient
response = requests.post('http://localhost:8000/api/register', json={
    'name': 'John Doe',
    'phone': '+1234567890'
})
data = response.json()
print(f"Token: {data['token']}")

# Get queue
queue = requests.get('http://localhost:8000/api/queue')
queue_data = queue.json()
print(f"Waiting: {queue_data['count']}")
```

---

## Notes

- All timestamps are in UTC
- Phone numbers should include country code
- QR codes are base64 encoded PNG images
- Token numbers reset daily (configurable)
- SMS notifications require Twilio configuration
