#!/usr/bin/env python3
import os
import json
import hashlib
import uuid
import requests
import concurrent.futures
import socket
import subprocess

USERS_FILE = "users.json"
SESSION_FILE = "session.json"

# -------------------- Utility Functions --------------------
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("username")
    return None

def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------- Registration --------------------
def register(users):
    clear_screen()
    username = input("Choose a username: ")
    if username in users:
        print("⚠️ Username already exists!")
        return users

    password = input("Choose a password: ")
    user_id = str(uuid.uuid4())
    users[username] = {
        "id": user_id,
        "password": hash_password(password)
    }
    save_users(users)
    print("✅ Registration successful!")
    print(f"Assigned ID: {user_id}")
    return users

# -------------------- SMS Simulation --------------------
def send_message(phone_number, message):
    clear_screen()
    url = "https://httpbin.org/post"  # Safe test endpoint
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "PythonDemo/1.0",
    }
    data = {
        "phone_number": phone_number,
        "message": message,
        "deviceId": str(uuid.uuid4()),
    }
    try:
        r = requests.post(url, headers=headers, data=data, timeout=5)
        r.raise_for_status()
        print(f"✔ Sent test message to {phone_number}")
    except requests.RequestException as e:
        print(f"❌ Failed: {e}")

def send_sms_textbelt(): 
    phone_number = input("Enter phone number (e.g. +66XXXXXXXXX): ")
    message = input("Enter message: ")
    try:
        count = int(input("Enter number of submissions: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_message, phone_number, message) for _ in range(count)]
        concurrent.futures.wait(futures)

    print(f"Attempted {count} requests.")

# -------------------- FoundIP (CLI version) --------------------
def FoundIP():
    clear_screen()
    print("=== IP Information ===\n")
    
    # Get local/server IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        server_ip = s.getsockname()[0]
    except Exception:
        server_ip = "127.0.0.1"
    finally:
        s.close()
    
    # Get public/network IP
    try:
        visitor_ip = requests.get("https://api.ipify.org").text
    except Exception:
        visitor_ip = "Unable to get public IP"
    
    print(f"My (Server) IP: {server_ip}")
    print(f"Your (Public/Network) IP: {visitor_ip}")

    # Optional: show LAN devices (safe)
    try:
        print("\nScanning LAN for other devices...")
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        print(result.stdout)
    except Exception:
        print("Unable to scan LAN devices.")

    input("\nPress Enter to continue...")

# -------------------- User Menu --------------------
def user_menu(username):
    while True:
        clear_screen()
        print(f"👋 Hello, {username}!")
        print("=== User Menu ===")
        print("[1] Profile Info")
        print("[2] Settings (change password)")
        print("[3] SMS Service")
        print("[4] Logout")
        print("[5] IP Founded")

        choice = input("Select an option: ")

        if choice == "1":
            print(f"📌 Username: {username}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            new_pass = input("Enter new password: ")
            users = load_users()
            users[username]["password"] = hash_password(new_pass)
            save_users(users)
            print("✅ Password updated!")
            input("\nPress Enter to continue...")

        elif choice == "3":
            send_sms_textbelt()

        elif choice == "4":
            print("👋 Logged out.")
            clear_session()
            break

        elif choice == "5":
            FoundIP()
        else:
            print("⚠️ Invalid choice")
            input("\nPress Enter to continue...")

# -------------------- Login --------------------
def login(users):
    clear_screen()
    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username]["password"] == hash_password(password):
        print(f"🎉 Login successful! Welcome, {username}!")
        save_session(username)
        input("\nPress Enter to continue...")
        user_menu(username)
    else:
        print("❌ Invalid username or password")
        input("\nPress Enter to continue...")

# -------------------- Main --------------------
def main():
    users = load_users()
    session_user = load_session()
    if session_user and session_user in users:
        user_menu(session_user)
        return

    while True:
        clear_screen()
        print("=== Cybersecurity Login System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            users = register(users)
            input("\nPress Enter to continue...")
        elif choice == "2":
            login(users)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("⚠️ Invalid choice")
            input("\nPress Enter to continue...")

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    main()
