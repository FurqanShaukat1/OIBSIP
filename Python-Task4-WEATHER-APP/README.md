# 🌤️ Weather App — Internship Task 4

A modern, dark-themed weather application built with Python and Tkinter. It fetches real-time weather information and forecasts using the OpenWeatherMap API.

## 📌 Task Objective

Build a Python application that fetches and displays real-time weather data for a user-specified location using a weather API.

This project implements the **Advanced Tier** requirements, including a graphical interface, weather icons, hourly forecasts, 5-day forecasts, unit conversion, and automatic IP-based location detection.

---

## ✨ Features

### 🌡️ Current Weather

- Search weather by city name
- Current temperature in Celsius and Fahrenheit
- Feels-like temperature
- Humidity percentage
- Wind speed
- Atmospheric pressure
- Visibility
- Weather condition and description
- Weather icons from OpenWeatherMap

### 📅 Weather Forecast

- Next 6 hours forecast
- 5-day forecast
- Forecast temperature
- Weather condition
- Feels-like temperature
- Weather icons
- Horizontally scrollable forecast cards

### 📍 Automatic Location Detection

- "Use My Location" button
- Detects approximate location using the user's IP address
- Uses the IPinfo API
- Automatically loads weather for the detected city

> IP-based location detection is approximate and may not always represent the user's exact physical location.

### 🎨 Modern GUI

- Dark theme
- Modern dashboard-style layout
- Rounded search field
- Rounded buttons
- Curved weather and forecast cards
- High-contrast accent colors
- Clean typography
- Scrollable forecast section
- GUI-based error messages

### ⚠️ Error Handling

The application handles:

- Empty city input
- City not found
- Invalid API key
- Expired API key
- Network connection errors
- API timeout
- Location detection errors

Errors are displayed directly inside the application.

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** — Graphical User Interface
- **Requests** — API requests
- **Pillow (PIL)** — Weather icons
- **python-dotenv** — Environment variable management
- **OpenWeatherMap API** — Weather and forecast data
- **IPinfo API** — IP-based location detection

---

## 📁 Project Structure

```text
weather_app/
│
├── main.py
├── weather_service.py
├── config.py
├── test_forecast.py
├── .env
├── .gitignore
│
└── assets/
    └── weather icons/resources