# 🎙️ Python Voice Assistant

A Python-based voice assistant that listens to spoken commands, understands user intent, and performs useful actions such as checking the time and date, searching the web, fetching live weather, setting reminders, answering knowledge questions, and sending emails.

## 📌 Internship Task

**Task:** Task 1 — Voice Assistant  
**Track:** Python Programming  
**Level:** Advanced

## 🎯 Objective

The objective of this project is to build a Python voice assistant that can capture spoken commands, process natural-language input, identify the user's intent, and perform useful actions using Python libraries and external APIs.

---

## ✨ Features

### 🎤 Voice Recognition

- Captures voice input using the microphone.
- Converts spoken commands into text using `speech_recognition`.
- Handles commands that are not understood gracefully.

### 🔊 Text-to-Speech

- Uses `pyttsx3` to provide spoken responses.
- The assistant responds audibly to commands and events.

### 🧠 Natural Language Intent Detection

The assistant can recognize different types of commands, including:

- Greetings
- Time requests
- Date requests
- Weather requests
- Web searches
- Reminders
- Email commands
- Knowledge questions
- Exit commands

The intent engine also extracts useful information from natural-language commands.

### 🌤️ Live Weather

The assistant can retrieve current weather information for a specified city using a weather API.

Example:

> "What is the weather in Lahore?"

The assistant provides:

- Weather condition
- Temperature
- Feels-like temperature
- Humidity

### 📧 Voice Email

The assistant can send emails using SMTP.

Example:

> "Send an email to test@example.com saying hello from my voice assistant."

It supports:

- Recipient extraction
- Spoken email addresses
- Default email subjects
- Custom subjects
- Email message/body extraction

Spoken email formats such as:

> "test at the rate example dot com"

can be converted into:

```text
test@example.com