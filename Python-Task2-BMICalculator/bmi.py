def calculate_bmi(weight, height):
    if weight <= 0:
        raise ValueError("Weight must be greater than 0.")

    if height <= 0:
        raise ValueError("Height must be greater than 0.")

    bmi = weight / (height ** 2)
    return round(bmi, 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"

    if bmi < 25:
        return "Normal"

    if bmi < 30:
        return "Overweight"

    return "Obese"