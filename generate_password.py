#!/usr/bin/env python3
"""
Password Hash Generator for Wake Forest RAG App
Use this to generate bcrypt hashes for new passwords
"""

import bcrypt
import getpass

def generate_password_hash():
    """Generate a bcrypt hash for a password"""
    print("=" * 50)
    print("Wake Forest RAG App - Password Hash Generator")
    print("=" * 50)
    print()
    
    # Get password from user
    password = getpass.getpass("Enter new password: ")
    confirm = getpass.getpass("Confirm password: ")
    
    if password != confirm:
        print("\n❌ Passwords don't match! Please try again.")
        return
    
    if len(password) < 8:
        print("\n⚠️  Warning: Password is less than 8 characters. Consider using a stronger password.")
    
    # Generate hash
    print("\nGenerating hash...")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    print("\n✅ Password hash generated successfully!")
    print("\nCopy this hash and paste it into config.yaml:")
    print("-" * 50)
    print(hashed.decode('utf-8'))
    print("-" * 50)
    print("\nIn config.yaml, replace the password line with:")
    print(f"      password: {hashed.decode('utf-8')}")
    print()

if __name__ == "__main__":
    generate_password_hash()
