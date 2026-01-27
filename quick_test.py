import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

print("Credentials loaded:")
print(f"SID: {TWILIO_SID}")
print(f"Token: {TWILIO_TOKEN[:10]}...")
print(f"Phone: {TWILIO_PHONE}")
print()

try:
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    account = client.api.accounts(TWILIO_SID).fetch()
    print(f"SUCCESS - Account Status: {account.status}")
    print(f"Account Name: {account.friendly_name}")
except Exception as e:
    print(f"ERROR: {e}")
