# BMI Calculator — Advanced

A Python-based BMI Calculator with a graphical user interface, SQLite data persistence, multi-user support, BMI history, and trend visualization.

## Features

### BMI Calculation
- Accepts weight in kilograms (kg)
- Accepts height in meters (m)
- Calculates BMI using:

  BMI = weight / (height²)

- Displays BMI rounded to 2 decimal places
- Classifies BMI into standard categories:
  - Underweight: BMI < 18.5
  - Normal: BMI 18.5–24.9
  - Overweight: BMI 25–29.9
  - Obese: BMI ≥ 30

### Graphical User Interface
- Built with Python Tkinter
- Simple and user-friendly interface
- Input fields for user name, weight, and height
- Calculate BMI button
- Clear button
- Color-coded BMI results

### Multi-User Support
- Allows different users to save their BMI records
- Each user has a unique record in the database
- Previous records can be retrieved by entering the user's name

### BMI History
- BMI records are stored in an SQLite database
- History displays:
  - Weight
  - Height
  - BMI
  - Category
  - Date and time of measurement

### BMI Trend Visualization
- Uses Matplotlib to visualize BMI history
- Displays BMI values over time
- Provides a line chart for each user's BMI trend

### Error Handling
- Rejects empty inputs
- Rejects non-numeric weight and height values
- Rejects invalid weight and height values
- Handles SQLite database errors
- Displays helpful error messages through the GUI

## Technologies Used

- Python
- Tkinter
- SQLite3
- Matplotlib

## Project Structure

```text
bmi_calculator/
│
├── bmi.py
│   └── BMI calculation and classification logic
│
├── database.py
│   └── SQLite database operations
│
├── gui.py
│   └── Tkinter graphical user interface
│
├── main.py
│   └── Application entry point
│
├── requirements.txt
│   └── Project dependencies
│
├── bmi_records.db
│   └── SQLite database created by the application
│
└── README.md
    └── Project documentation