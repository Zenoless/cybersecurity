#!/usr/bin/env python3
import os

def clear_screen():
    # Linux, Termux, MacOS
    os.system('clear')

def main():
    clear_screen()  # clear the terminal at start
    username = input("Enter your username: ")
    clear_screen()  # optional: clear again after entering username
    print(f"Hello, {username}! Welcome to the cybersecurity project.")

if __name__ == "__main__":
    main()
