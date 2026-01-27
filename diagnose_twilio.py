import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

print("=" * 70)
print("TWILIO ACCOUNT DIAGNOSTICS")
print("=" * 70)
print()

try:
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    
    # Check account details
    print("1. ACCOUNT STATUS:")
    print("-" * 70)
    account = client.api.accounts(TWILIO_SID).fetch()
    print(f"   Account Name: {account.friendly_name}")
    print(f"   Status: {account.status}")
    print(f"   Type: {account.type}")
    print()
    
    # Check if trial account
    if account.type == 'Trial':
        print("   ⚠️  TRIAL ACCOUNT DETECTED")
        print("   Trial accounts can ONLY send SMS to verified phone numbers!")
        print()
    
    # Check balance
    print("2. ACCOUNT BALANCE:")
    print("-" * 70)
    balance = client.api.balance.fetch()
    print(f"   Balance: {balance.balance} {balance.currency}")
    print()
    
    # Check phone number
    print("3. PHONE NUMBER CHECK:")
    print("-" * 70)
    print(f"   Configured Number: {TWILIO_PHONE}")
    try:
        phone_numbers = client.incoming_phone_numbers.list(phone_number=TWILIO_PHONE)
        if phone_numbers:
            phone = phone_numbers[0]
            print(f"   ✅ Number is valid and active")
            print(f"   Capabilities:")
            print(f"      - Voice: {phone.capabilities.get('voice', False)}")
            print(f"      - SMS: {phone.capabilities.get('sms', False)}")
            print(f"      - MMS: {phone.capabilities.get('mms', False)}")
        else:
            print(f"   ❌ Number NOT found in your account!")
            print()
            print("   Your available numbers:")
            all_numbers = client.incoming_phone_numbers.list(limit=10)
            for num in all_numbers:
                print(f"      - {num.phone_number}")
    except Exception as e:
        print(f"   ⚠️  Could not verify number: {e}")
    print()
    
    # List verified caller IDs (for trial accounts)
    print("4. VERIFIED PHONE NUMBERS (Trial Account):")
    print("-" * 70)
    try:
        verified_numbers = client.outgoing_caller_ids.list(limit=20)
        if verified_numbers:
            print("   SMS can be sent to these verified numbers:")
            for caller in verified_numbers:
                print(f"      ✅ {caller.phone_number}")
        else:
            print("   ❌ NO VERIFIED NUMBERS FOUND!")
            print()
            print("   You must verify phone numbers before sending SMS!")
            print("   Visit: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    except Exception as e:
        print(f"   Could not fetch verified numbers: {e}")
    print()
    
    # Check recent messages
    print("5. RECENT SMS ATTEMPTS:")
    print("-" * 70)
    try:
        messages = client.messages.list(limit=5)
        if messages:
            for msg in messages:
                status_icon = "✅" if msg.status == "delivered" else "❌" if msg.status == "failed" else "⏳"
                print(f"   {status_icon} To: {msg.to} | Status: {msg.status} | Sent: {msg.date_sent}")
                if msg.error_code:
                    print(f"      Error Code: {msg.error_code} - {msg.error_message}")
        else:
            print("   No recent messages found")
    except Exception as e:
        print(f"   Could not fetch messages: {e}")
    print()
    
    print("=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    
    if account.type == 'Trial':
        print("⚠️  YOUR ACCOUNT IS A TRIAL ACCOUNT")
        print()
        print("TO SEND SMS, YOU MUST:")
        print("1. Verify the recipient's phone number at:")
        print("   https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print()
        print("2. OR upgrade your account to send to any number:")
        print("   https://console.twilio.com/billing")
        print()
    else:
        print("✅ Your account is upgraded - you can send to any valid number")
        print()
    
    print("To test sending SMS, run: python test_send_sms.py")
    print("=" * 70)

except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    if "20003" in str(e):
        print("Authentication failed - check your credentials in .env file")
