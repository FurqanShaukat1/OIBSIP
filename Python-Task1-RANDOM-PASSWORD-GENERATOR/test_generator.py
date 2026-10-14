from password_generator import generate_password


password = generate_password(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
)

print("Generated password:", password)
print("Length:", len(password))