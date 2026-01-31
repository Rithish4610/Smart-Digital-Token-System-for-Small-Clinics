import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")
FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"

def send_sms(phone_number: str, message: str):
    """
    Send SMS using Fast2SMS API (MOCK MODE).
    """
    # ALWAYS MOCK FOR DEMO PURPOSES
    print(f"\n" + "="*50)
    print(f"📱 [MOCK SMS SENT]")
    print(f"To:      {phone_number}")
    print(f"Message: {message}")
    print("="*50 + "\n")
    
    return True, "Mock SMS Sent Successfully"

