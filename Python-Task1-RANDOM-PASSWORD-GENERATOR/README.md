# Random Password Generator

A secure and user-friendly Python GUI application that generates strong random passwords based on user-defined criteria.

This project was developed as **Task 3 of the UI/UX Internship**.

## Features

- Generate secure random passwords
- Password length control from 8 to 64 characters
- Select character types:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Symbols (!@#$...)
- Minimum of two character types required
- Automatically guarantees at least one character from every selected type
- Uses Python's `secrets` module for secure password generation
- Password strength indicator:
  - Weak
  - Medium
  - Strong
- Copy password to clipboard
- Automatically copies newly generated passwords to the clipboard
- Option to exclude ambiguous characters such as:
  - `0`
  - `O`
  - `o`
  - `I`
  - `l`
  - `1`
- Displays the last 5 generated passwords during the current session
- Password history is not saved to disk
- Scrollable GUI for smaller screens
- Input validation and error messages
- Modern and simple graphical interface

## Technologies Used

- Python
- Tkinter
- `secrets`
- `string`
- Pyperclip

## Project Structure

```text
task3_password_generator/
│
├── main.py
├── password_generator.py
├── test_generator.py
├── requirements.txt
├── README.md
└── .gitignore