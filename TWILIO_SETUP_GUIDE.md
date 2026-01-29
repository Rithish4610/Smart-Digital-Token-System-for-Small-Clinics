# Twilio SMS Setup Guide

## 📱 Complete Guide to Enable Real SMS Notifications

This guide will help you set up Twilio to send real SMS messages to patients when they register.

---

## Step 1: Create Twilio Account

1. **Visit Twilio Sign-Up Page**
   - Go to: https://www.twilio.com/try-twilio
   - Click "Sign up and start building"

2. **Fill in Your Details**
   - First Name & Last Name
   - Email Address
   - Password
   - Click "Start your free trial"

3. **Verify Your Email**
   - Check your email inbox
   - Click the verification link from Twilio

4. **Verify Your Phone Number**
   - Enter your phone number
   - Enter the verification code sent to you
   - This becomes your first "Verified Caller ID"

---

## Step 2: Get Your Twilio Credentials

After signing in to your Twilio Console (https://console.twilio.com):

### A. Account SID and Auth Token

1. On your Dashboard, you'll see:
   ```
   Account Info
   ├── ACCOUNT SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   └── AUTH TOKEN: ********************************
   ```

2. **Copy these values** - you'll need them for the `.env` file

### B. Get a Phone Number

1. In the left sidebar, click **"Phone Numbers"** → **"Manage"** → **"Buy a number"**

2. **For Trial Account:**
   - Select your country (e.g., United States, India)
   - Check "SMS" capability
   - Click "Search"
   - Click "Buy" on any available number
   - Confirm purchase (FREE for trial)

3. **Copy your new phone number** (e.g., `+1234567890`)

---

## Step 3: Configure the Application

### Create/Update `.env` File

1. Open or create the file `.env` in your project root
2. Add these lines with YOUR credentials:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

**Important Notes:**
- Replace the values with your actual credentials from Step 2
- Phone number MUST include country code (e.g., `+91` for India, `+1` for US)
- No spaces in the phone number
- Keep this file SECRET (it's in `.gitignore` for security)

### Example `.env` File:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=AC_YOUR_ACCOUNT_SID_HERE
TWILIO_AUTH_TOKEN=YOUR_AUTH_TOKEN_HERE
TWILIO_PHONE_NUMBER=+15550000000
```

---

## Step 4: Understanding Trial Account Limitations

### ⚠️ Twilio Trial Account Restrictions:

1. **Verified Numbers Only**
   - You can ONLY send SMS to phone numbers you've verified in Twilio
   - To verify additional numbers: Console → Phone Numbers → Verified Caller IDs

2. **Trial Message Prefix**
   - All SMS will start with: "Sent from your Twilio trial account - "
   - This prefix is removed when you upgrade

3. **Credit Limit**
   - Free $15.50 trial credit (approx. 200-600 SMS depending on country)
   - Check balance: Console → Billing

### To Remove Limitations (Upgrade Account):

1. Go to: https://console.twilio.com/billing/upgrade
2. Add payment information
3. Upgrade to paid account
4. You can now send to ANY phone number
5. No more trial message prefix

---

## Step 5: Test Your Configuration

### Option A: Use the Test Script

Run the Twilio diagnostic script:

```bash
python diagnose_twilio.py
```

This will:
- ✓ Check if credentials are loaded
- ✓ Validate Account SID format
- ✓ Test connection to Twilio
- ✓ Show your account status

### Option B: Test in the Application

1. **Restart the application** (to reload `.env`):
   - Stop the server (Ctrl+C)
   - Run: `python main.py`

2. **Register a test patient**:
   - Go to: http://localhost:8000/reception
   - Enter patient name
   - Enter a VERIFIED phone number (with country code)
   - Click Register

3. **Check the terminal** for SMS status:
   - Success: `SMS SENT: To +1234567890`
   - Failure: Error message with details

---

## Step 6: Verify Number for Testing

To add more verified numbers (for trial account):

1. Go to: https://console.twilio.com/phone-numbers/verified
2. Click "Add a new Caller ID"
3. Enter the phone number (with country code)
4. Click "Call Me" or "Text Me"
5. Enter the verification code
6. Now you can send SMS to this number!

---

## Phone Number Format Guide

### ✅ Correct Formats:

| Country | Format | Example |
|---------|--------|---------|
| India | +91XXXXXXXXXX | +919876543210 |
| USA | +1XXXXXXXXXX | +15551234567 |
| UK | +44XXXXXXXXXXX | +447911123456 |
| Australia | +61XXXXXXXXX | +61412345678 |

### ❌ Incorrect Formats:

- ❌ `9876543210` (missing country code)
- ❌ `+91 98765 43210` (has spaces)
- ❌ `+91-9876543210` (has dashes)
- ❌ `919876543210` (missing + sign)

---

## Troubleshooting

### "SMS FAILED: Unable to create record"

**Solution:** Phone number not verified (for trial accounts)
- Verify the number in Twilio Console
- Or upgrade to a paid account

### "SMS FAILED: Authenticate"

**Solution:** Invalid credentials
- Double-check ACCOUNT_SID and AUTH_TOKEN in `.env`
- Make sure there are no extra spaces
- Restart the application

### "SMS FAILED: Invalid 'From' phone number"

**Solution:** Wrong phone number format
- Ensure it starts with `+` and country code
- No spaces or special characters
- Must be a Twilio number you own

### "MOCK SMS" appears in terminal

**Solution:** Credentials not loaded
- Check if `.env` file exists
- Verify the values are not placeholders
- Restart the application to reload `.env`

---

## Pricing Information

### Trial Account:
- **Free credit:** $15.50 USD
- **Cost per SMS:** ~$0.0075 - $0.05 (varies by country)
- **Estimated SMS:** 200-600 messages

### Paid Account (India):
- **SMS cost:** ~$0.0067 per message (₹0.55)
- **Monthly cost (100 patients/day):** ~$20 (~₹1,650)
- **Phone number:** ~$1.15/month

### Pay-as-you-go (Recommended):
- No monthly fees
- Only pay for SMS sent
- Keep balance topped up

---

## Security Best Practices

1. **Never commit `.env` to Git**
   - It's already in `.gitignore`
   - But double-check before pushing code

2. **Rotate credentials** if exposed
   - Go to Console → Account → API Keys
   - Create new Auth Token
   - Update `.env`

3. **Use environment variables** in production
   - Don't hardcode credentials
   - Use platform-specific secret management

---

## Quick Reference Commands

```bash
# Test Twilio configuration
python diagnose_twilio.py

# Run the application
python main.py

# Check if .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('TWILIO_ACCOUNT_SID'))"
```

---

## Support Resources

- **Twilio Console:** https://console.twilio.com
- **Twilio Docs:** https://www.twilio.com/docs/sms
- **Pricing:** https://www.twilio.com/sms/pricing
- **Support:** https://support.twilio.com

---

## Summary Checklist

- [ ] Created Twilio account
- [ ] Verified email and phone number
- [ ] Got Account SID and Auth Token
- [ ] Purchased/got a Twilio phone number
- [ ] Created `.env` file with credentials
- [ ] Restarted the application
- [ ] Tested with verified phone number
- [ ] SMS working successfully! 🎉

---

**Need Help?** Check the Troubleshooting section or run `python diagnose_twilio.py`
