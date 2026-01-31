"""
Fast2SMS Quick Setup Script
===========================
Interactive script to help you configure Fast2SMS credentials.
"""

import os
import sys

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def create_env_file(api_key):
    env_content = f"""# Fast2SMS Configuration
FAST2SMS_API_KEY={api_key}

# Application Settings
SECRET_KEY=dev_secret_key_change_in_production
"""
    try:
        with open("config.env", "w") as f:
            f.write(env_content)
        print("\n✅ config.env file created successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error creating config.env file: {e}")
        return False

def main():
    print_header("Fast2SMS Quick Setup")
    print("This script will help you configure your Fast2SMS API Key.")
    print("You can get your key from: https://www.fast2sms.com/dashboard/dev-api")
    print("-" * 60)
    
    api_key = input("\nEnter your Fast2SMS API Authorization Key: ").strip()
    
    if not api_key:
        print("❌ API Key cannot be empty.")
        return

    if len(api_key) < 20:
         print("⚠️  Warning: That looks a bit short for an API key. Double check it.")
    
    confirm = input(f"\nYou entered: {api_key[:5]}...{api_key[-5:]}\nIs this correct? (y/n): ").lower().strip()
    
    if confirm == 'y':
        if create_env_file(api_key):
            print("\n🎉 Setup Complete! You can now run 'python main.py' to start the application.")
    else:
        print("\nSetup cancelled.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
