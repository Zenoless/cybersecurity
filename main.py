#!/usr/bin/env python3
import os, json, hashlib

DATA_FILE = "users.json"

def clear_screen():
    os.system("clear")

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(users):
    clear_screen()
    username = input("Choose a username: ")
    if username in users:
        print("⚠️ Username already exists!")
        return users

    password = input("Choose a password: ")
    users[username] = hash_password(password)
    save_users(users)
    print("✅ Registration successful!")
    return users

def login(users):
    clear_screen()
    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username] == hash_password(password):
        print(f"🎉 Welcome back, {username}!")
    else:
        print("❌ Invalid username or password")

def main():
    users = load_users()

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
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("⚠️ Invalid choice")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
