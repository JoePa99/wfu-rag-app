#!/usr/bin/env python3
"""
Setup Verification Script for Wake Forest RAG App
Checks if all requirements are properly configured
"""

import os
from pathlib import Path
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: NOT FOUND")
        return False

def check_env_var(var_name):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value and value != f"your_{var_name.lower()}_here":
        print(f"✅ {var_name}: Set")
        return True
    else:
        print(f"❌ {var_name}: NOT SET or using placeholder")
        return False

def main():
    print("=" * 60)
    print("Wake Forest RAG App - Setup Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check files
    print("📁 Checking Required Files...")
    print("-" * 60)
    all_good &= check_file('.env', '.env file')
    all_good &= check_file('service-account.json', 'Google Service Account')
    all_good &= check_file('config.yaml', 'Authentication config')
    all_good &= check_file('assets/WFU_Univ_Shield_Black.png', 'Wake Forest logo')
    print()
    
    # Check environment variables
    print("🔑 Checking Environment Variables...")
    print("-" * 60)
    
    # Load .env file if it exists
    if Path('.env').exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    all_good &= check_env_var('ANTHROPIC_API_KEY')
    all_good &= check_env_var('OPENAI_API_KEY')
    all_good &= check_env_var('SUPABASE_URL')
    all_good &= check_env_var('SUPABASE_SERVICE_KEY')
    all_good &= check_env_var('GOOGLE_SERVICE_ACCOUNT_FILE')
    print()
    
    # Check Python packages
    print("📦 Checking Python Packages...")
    print("-" * 60)
    
    required_packages = [
        'streamlit',
        'anthropic',
        'openai',
        'supabase',
        'google.auth',
        'PyPDF2',
        'docx',
        'openpyxl',
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('.', '_').replace('-', '_'))
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: NOT INSTALLED")
            all_good = False
    
    print()
    print("=" * 60)
    
    if all_good:
        print("🎉 All checks passed! You're ready to run the app.")
        print()
        print("To start the application, run:")
        print("    streamlit run app.py")
        print()
        print("Default login:")
        print("    Username: admin")
        print("    Password: wfu_admin_2025")
        print()
        print("⚠️  Remember to change the default password!")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print()
        print("Common fixes:")
        print("  - Missing .env: Copy .env.example to .env and fill in values")
        print("  - Missing packages: Run 'pip install -r requirements.txt'")
        print("  - Missing service account: Download from Google Cloud Console")
        print()
        print("See README.md for detailed setup instructions.")
    
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
