#!/usr/bin/env python3
import os, json, hashlib, uuid
import requests
import uuid
import concurrent.futures
from flask import Flask, request
import socket

USERS_FILE = "users.json"
SESSION_FILE = "session.json"

def clear_screen():
    os.system("clear")

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
    phone_number = input("Enter iPhone number (e.g. +66XXXXXXXXX): ")
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

def FoundIP():
    app = Flask(__name__)

    def get_server_ip():
        """Get the local IP of the server."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))  # doesn't have to be reachable
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    @app.route('/')
    def index():
        visitor_ip = request.remote_addr
        server_ip = get_server_ip()

        html_content = f"""
        <html>
        <head>
            <title>Welcome</title>
            <style>
                body {{
                    background: linear-gradient(135deg, #4eff4e, #9cff9c);
                    color: white;
                    height: 100vh;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                }}
                .BIG {{
                    font-size: 2em;
                }}
            </style>
        </head>
        <body>
            <div>
                <h1>Welcome back,</h1>
                <h2>My Name is Leo. If you see this text you cannot hide anymore.</h2>
                <h2>I have your IP already. Your network IP is: <strong>{visitor_ip}</strong></h2>
                <h2>Server (self) IP is: <strong>{server_ip}</strong></h2>
                <h2>Thanks for reading, have fun! <span class="BIG">Hacked!</span></h2>
            </div>
        </body>
        </html>
        """
        print(f"Visitor IP: {visitor_ip} | Server IP: {server_ip}")  # log to console
        return html_content

    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=True)

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
            send_sms_textbelt()  # send SMS using Textbelt

        elif choice == "4":
            print("👋 Logged out.")
            clear_session()
            break
        elif choice == "5": 
            clear_screen()
            FoundIP()
        else:
            print("⚠️ Invalid choice")
            input("\nPress Enter to continue...")

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

def main():
    users = load_users()

    # Check session at startup
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

if __name__ == "__main__":
    main()
