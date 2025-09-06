#!/usr/bin/env python3

def main():
    try:
        username = input("Enter your username: ")
        print(f"Hello, {username}! Welcome to the cybersecurity project.")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

if __name__ == "__main__":
    main()
