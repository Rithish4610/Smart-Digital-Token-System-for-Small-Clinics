import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

print("=" * 60)
print("SMS SENDING TEST")
print("=" * 60)
print(f"From Number: {TWILIO_PHONE}")
print()

# Get the phone number to test
test_phone = input("Enter the phone number to test (with country code, e.g., +919876543210): ").strip()

if not test_phone.startswith('+'):
    print("ERROR: Phone number must start with '+' and include country code")
    print("Examples:")
    print("  India: +919876543210")
    print("  US: +14155551234")
    exit(1)

print()
print(f"Attempting to send SMS to: {test_phone}")
print("=" * 60)

try:
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    
    message = client.messages.create(
        body="Test SMS from Clinic Token System. If you receive this, SMS is working!",
        from_=TWILIO_PHONE,
        to=test_phone
    )
    
    print()
    print("✅ SUCCESS!")
    print(f"Message SID: {message.sid}")
    print(f"Status: {message.status}")
    print(f"To: {message.to}")
    print(f"From: {message.from_}")
    print()
    print("Check the recipient's phone for the SMS message!")
    
except Exception as e:
    print()
    print("❌ FAILED!")
    print(f"Error: {str(e)}")
    print()
    
    error_str = str(e).lower()
    
    if "unverified" in error_str or "trial" in error_str or "21608" in error_str:
        print("ISSUE: Trial Account - Unverified Number")
        print("-" * 60)
        print("Your Twilio trial account can only send to VERIFIED numbers.")
        print()
        print("To fix this:")
        print("1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print("2. Click 'Add a new Caller ID'")
        print(f"3. Enter the phone number: {test_phone}")
        print("4. Twilio will call/SMS you with a verification code")
        print("5. Enter the code to verify")
        print("6. Run this test again")
        print()
        print("OR upgrade your Twilio account to send to any number")
        
    elif "21211" in error_str or "invalid" in error_str:
        print("ISSUE: Invalid Phone Number")
        print("-" * 60)
        print("The phone number format is incorrect.")
        print("Use E.164 format: +[country code][number]")
        print("Examples: +919876543210 (India), +14155551234 (US)")
        
    elif "21606" in error_str:
        print("ISSUE: Invalid From Number")
        print("-" * 60)
        print(f"The number {TWILIO_PHONE} is not registered in your Twilio account.")
        print("Check your Twilio console for the correct phone number.")
        
    elif "20003" in error_str or "authenticate" in error_str:
        print("ISSUE: Authentication Failed")
        print("-" * 60)
        print("Your Account SID or Auth Token is incorrect.")
        print("Check your .env file and Twilio console.")
        
    else:
        print("ISSUE: Unknown Error")
        print("-" * 60)
        print("Check the error message above and:")
        print("1. Verify your Twilio account status at console.twilio.com")
        print("2. Check if your account has sufficient balance")
        print("3. Verify the phone numbers are correct")

print()
print("=" * 60)
