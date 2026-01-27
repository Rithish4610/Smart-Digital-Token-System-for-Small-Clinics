import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

print("=== Twilio Configuration Test ===")
print(f"Account SID: {TWILIO_SID}")
print(f"Auth Token: {'*' * len(TWILIO_TOKEN) if TWILIO_TOKEN else 'NOT SET'}")
print(f"Phone Number: {TWILIO_PHONE}")
print()

if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_PHONE]):
    print("❌ ERROR: Missing Twilio credentials in .env file")
    exit(1)

try:
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    
    # Test 1: Verify account
    print("Testing Twilio account...")
    account = client.api.accounts(TWILIO_SID).fetch()
    print(f"✓ Account verified: {account.friendly_name}")
    print(f"  Status: {account.status}")
    print()
    
    # Test 2: Check phone number
    print("Checking phone number...")
    try:
        incoming_phone = client.incoming_phone_numbers.list(phone_number=TWILIO_PHONE)
        if incoming_phone:
            print(f"✓ Phone number verified: {TWILIO_PHONE}")
            print(f"  Capabilities: {incoming_phone[0].capabilities}")
        else:
            print(f"⚠ Warning: Phone number {TWILIO_PHONE} not found in your account")
            print("  Available numbers:")
            numbers = client.incoming_phone_numbers.list(limit=5)
            for num in numbers:
                print(f"    - {num.phone_number}")
    except Exception as e:
        print(f"⚠ Warning: Could not verify phone number: {e}")
    
    print()
    print("=== Configuration is valid! ===")
    print()
    print("To test sending an SMS, uncomment the code below and add your phone number:")
    print("# test_phone = '+1234567890'  # Your phone with country code")
    print("# message = client.messages.create(")
    print("#     body='Test message from clinic system',")
    print("#     from_=TWILIO_PHONE,")
    print("#     to=test_phone")
    print("# )")
    print("# print(f'Test SMS sent! Message SID: {message.sid}')")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print()
    print("Common issues:")
    print("1. Invalid credentials - check your Account SID and Auth Token")
    print("2. Account suspended - check your Twilio console")
    print("3. Phone number not verified - verify in Twilio console")
