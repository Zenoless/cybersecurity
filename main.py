#!/usr/bin/env python3
import os, json, hashlib, uuid
import requests

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

def send_sms_textbelt():
    clear_screen()
    print("=== SMS Service (Textbelt) ===")
    phone_number = input("Enter recipient phone number with country code (e.g., +66812345678): ")
    message_text = input("Enter message: ")
    amount = int(input("Enter amount of messages to send: "))

    for i in range(amount):
        resp = requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': message_text,
            'key': 'textbelt',  # free trial key
        })
        result = resp.json()
        if result.get('success'):
            print(f"✅ Message {i+1} sent!")
        else:
            print(f"❌ Failed to send message {i+1}: {result.get('error')}")

    input("\nPress Enter to continue...")

def user_menu(username):
    while True:
        clear_screen()
        print(f"👋 Hello, {username}!")
        print("=== User Menu ===")
        print("[1] Profile Info")
        print("[2] Settings (change password)")
        print("[3] SMS Service")
        print("[4] Logout")

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
