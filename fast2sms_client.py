import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")
FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"

def send_sms(phone_number: str, message: str):
    """
    Send SMS using Fast2SMS API.
    
    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message content.
        
    Returns:
        tuple: (success (bool), status_message (str))
    """
    if not FAST2SMS_API_KEY or FAST2SMS_API_KEY == "your_fast2sms_api_key_here":
        print(f"------------ MOCK SMS (No Valid API Key) ------------")
        print(f"To: {phone_number}")
        print(f"Message: {message}")
        print(f"-----------------------------------------------------")
        return False, "Mock SMS (API Key not configured)"

    # Fast2SMS requires numbers without + for India, usually just 10 digits
    # If the number has +91, we might need to strip it or check Fast2SMS requirements.
    # Documentation says "numbers" parameter takes comma separated numbers.
    
    # Clean phone number (remove +91 or + if present, assuming Indian numbers for Fast2SMS default)
    clean_phone = phone_number
    if clean_phone.startswith("+91"):
        clean_phone = clean_phone[3:]
    elif clean_phone.startswith("+"):
         clean_phone = clean_phone[1:]
         
    payload = {
        "route": "q",  # 'q' for Quick SMS (Promotional/Transactional depending on account)
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": clean_phone,
    }

    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(FAST2SMS_URL, json=payload, headers=headers)
        data = response.json()
        
        if data.get("return") == True:
            print(f"SMS SENT: To {phone_number} (ID: {data.get('request_id')})")
            return True, "Sent successfully"
        else:
            error_msg = data.get("message", "Unknown error")
            print(f"SMS FAILED: {error_msg}")
            return False, f"Failed: {error_msg}"
            
    except Exception as e:
        print(f"SMS FAILED: {str(e)}")
        return False, f"Failed: {str(e)}"
