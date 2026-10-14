import sqlite3
from datetime import datetime


DATABASE_NAME = "bmi_records.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.commit()
        connection.close()

        print("Database initialized successfully.")

    except sqlite3.Error as error:
        print(f"Database initialization error: {error}")


def get_or_create_user(name):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE name = ?",
            (name,)
        )

        user = cursor.fetchone()

        if user:
            user_id = user[0]
        else:
            cursor.execute(
                "INSERT INTO users (name) VALUES (?)",
                (name,)
            )
            user_id = cursor.lastrowid
            connection.commit()

        connection.close()
        return user_id

    except sqlite3.Error as error:
        print(f"Database user error: {error}")
        return None


def save_bmi_record(user_id, weight, height, bmi, category):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO bmi_records
            (user_id, weight, height, bmi, category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            weight,
            height,
            bmi,
            category,
            recorded_at
        ))

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:
        print(f"Database save error: {error}")
        return False

def get_user_id(name):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE name = ?",
            (name,)
        )

        user = cursor.fetchone()

        connection.close()

        if user:
            return user[0]

        return None

    except sqlite3.Error as error:
        print(f"Database user lookup error: {error}")
        return None


def get_user_history(user_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT weight, height, bmi, category, recorded_at
            FROM bmi_records
            WHERE user_id = ?
            ORDER BY recorded_at ASC
        """, (user_id,))

        records = cursor.fetchall()

        connection.close()

        return records

    except sqlite3.Error as error:
        print(f"Database history error: {error}")
        return []





if __name__ == "__main__":
    initialize_database()

    user_id = get_or_create_user("Test User")

    save_bmi_record(
        user_id,
        70,
        1.75,
        22.86,
        "Normal"
    )

    history = get_user_history(user_id)

    print("\nBMI History:")

    for record in history:
        print(record)    