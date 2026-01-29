"""
Twilio SMS Configuration Diagnostic Tool
========================================
This script helps diagnose Twilio SMS setup issues.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_status(label, status, details=""):
    """Print a status line"""
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {label}")
    if details:
        print(f"  → {details}")

def check_env_file():
    """Check if .env file exists"""
    print_header("1. Checking .env File")
    
    env_exists = os.path.exists(".env")
    print_status(".env file exists", env_exists)
    
    if not env_exists:
        print("\n⚠️  No .env file found!")
        print("   Create one by copying .env.example:")
        print("   copy .env.example .env")
        print("   Then edit .env with your Twilio credentials")
        return False
    
    return True

def check_credentials():
    """Check if Twilio credentials are loaded"""
    print_header("2. Checking Twilio Credentials")
    
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    phone = os.getenv("TWILIO_PHONE_NUMBER")
    
    # Check SID
    sid_valid = sid and sid != "your_account_sid_here" and sid.startswith("AC")
    print_status("TWILIO_ACCOUNT_SID loaded", bool(sid))
    if sid:
        if sid == "your_account_sid_here":
            print("  → Still using placeholder value")
        elif not sid.startswith("AC"):
            print("  → Invalid format (should start with 'AC')")
        else:
            print(f"  → {sid[:10]}...{sid[-4:]}")
    
    # Check Token
    token_valid = token and token != "your_auth_token_here" and len(token) == 32
    print_status("TWILIO_AUTH_TOKEN loaded", bool(token))
    if token:
        if token == "your_auth_token_here":
            print("  → Still using placeholder value")
        else:
            print(f"  → {'*' * 28}{token[-4:]}")
    
    # Check Phone
    phone_valid = phone and phone != "your_twilio_number_here" and phone.startswith("+")
    print_status("TWILIO_PHONE_NUMBER loaded", bool(phone))
    if phone:
        if phone == "your_twilio_number_here":
            print("  → Still using placeholder value")
        elif not phone.startswith("+"):
            print("  → Missing country code (should start with '+')")
        else:
            print(f"  → {phone}")
    
    all_valid = sid_valid and token_valid and phone_valid
    
    if not all_valid:
        print("\n⚠️  Credentials incomplete or invalid!")
        print("   Edit your .env file with real Twilio credentials")
        print("   See TWILIO_SETUP_GUIDE.md for instructions")
    
    return all_valid, sid, token, phone

def test_twilio_connection(sid, token, phone):
    """Test connection to Twilio API"""
    print_header("3. Testing Twilio Connection")
    
    try:
        from twilio.rest import Client
        print_status("Twilio library installed", True)
    except ImportError:
        print_status("Twilio library installed", False, "Run: pip install twilio")
        return False
    
    try:
        client = Client(sid, token)
        
        # Test API connection by fetching account details
        account = client.api.accounts(sid).fetch()
        
        print_status("Connected to Twilio API", True)
        print(f"  → Account Status: {account.status}")
        print(f"  → Account Type: {account.type}")
        
        # Get account balance
        balance = client.api.accounts(sid).balance.fetch()
        print(f"  → Balance: {balance.currency} {balance.balance}")
        
        return True
        
    except Exception as e:
        print_status("Connected to Twilio API", False, str(e))
        print("\n⚠️  Connection failed!")
        print("   Double-check your ACCOUNT_SID and AUTH_TOKEN")
        return False

def test_phone_number(client, phone):
    """Test if the phone number is valid and owned"""
    print_header("4. Verifying Phone Number")
    
    try:
        incoming_phone_numbers = client.incoming_phone_numbers.list(
            phone_number=phone,
            limit=1
        )
        
        if incoming_phone_numbers:
            number = incoming_phone_numbers[0]
            print_status("Phone number verified", True)
            print(f"  → Number: {number.phone_number}")
            print(f"  → SMS Enabled: {number.capabilities['sms']}")
            return True
        else:
            print_status("Phone number verified", False, 
                        "This number is not in your Twilio account")
            return False
            
    except Exception as e:
        print_status("Phone number verification", False, str(e))
        return False

def send_test_sms(client, from_phone):
    """Optionally send a test SMS"""
    print_header("5. Send Test SMS (Optional)")
    
    print("\nWould you like to send a test SMS?")
    print("Note: For trial accounts, recipient must be verified.")
    
    choice = input("Send test SMS? (y/n): ").lower().strip()
    
    if choice != 'y':
        print("Skipped test SMS")
        return
    
    to_phone = input("Enter recipient phone number (with country code, e.g., +919876543210): ").strip()
    
    if not to_phone.startswith('+'):
        print("❌ Phone number must start with + and country code")
        return
    
    try:
        message = client.messages.create(
            body="🏥 Test SMS from Smart Clinic Token System - Your Twilio SMS is working!",
            from_=from_phone,
            to=to_phone
        )
        
        print_status("Test SMS sent", True)
        print(f"  → Message SID: {message.sid}")
        print(f"  → Status: {message.status}")
        print(f"  → To: {message.to}")
        
    except Exception as e:
        print_status("Test SMS sent", False, str(e))
        
        if "not a verified phone number" in str(e).lower():
            print("\n⚠️  Phone number not verified!")
            print("   For trial accounts, verify numbers at:")
            print("   https://console.twilio.com/phone-numbers/verified")

def main():
    """Main diagnostic routine"""
    print("\n" + "🏥 " + "="*58)
    print("  Smart Clinic Token System - Twilio SMS Diagnostics")
    print("="*61 + "\n")
    
    # Step 1: Check .env file
    if not check_env_file():
        sys.exit(1)
    
    # Step 2: Check credentials
    creds_valid, sid, token, phone = check_credentials()
    if not creds_valid:
        sys.exit(1)
    
    # Step 3: Test connection
    try:
        from twilio.rest import Client
        client = Client(sid, token)
        
        if not test_twilio_connection(sid, token, phone):
            sys.exit(1)
        
        # Step 4: Test phone number
        test_phone_number(client, phone)
        
        # Step 5: Optional test SMS
        send_test_sms(client, phone)
        
    except ImportError:
        print("\n⚠️  Twilio library not installed!")
        print("   Run: pip install twilio")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Success summary
    print_header("✅ Diagnostic Complete")
    print("\nYour Twilio SMS configuration appears to be working!")
    print("\nNext steps:")
    print("  1. Restart the application: python main.py")
    print("  2. Go to: http://localhost:8000/reception")
    print("  3. Register a patient with a verified phone number")
    print("  4. Check if SMS is received")
    print("\n📚 For more help, see: TWILIO_SETUP_GUIDE.md\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnostic cancelled by user.")
        sys.exit(0)
