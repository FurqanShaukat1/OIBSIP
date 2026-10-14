import sqlite3
import hashlib


DATABASE = "chat.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# =========================
# DATABASE INITIALIZATION
# =========================

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # Chat rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)

    # Create default room
    cursor.execute("""
        INSERT OR IGNORE INTO rooms (name)
        VALUES ('General')
    """)

    connection.commit()
    connection.close()


# =========================
# PASSWORD HASHING
# =========================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================
# USER REGISTRATION
# =========================

def register_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    finally:
        connection.close()


# =========================
# USER LOGIN
# =========================

def login_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ? AND password_hash = ?
        """,
        (username, password_hash)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        return True, "Login successful."

    return False, "Invalid username or password."


# =========================
# ROOM FUNCTIONS
# =========================

def get_rooms():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name
        FROM rooms
        ORDER BY name
    """)

    rooms = cursor.fetchall()

    connection.close()

    return rooms


def create_room(room_name, username):
    room_name = room_name.strip()

    if not room_name:
        return False, "Room name cannot be empty."

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Find the user creating the room
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return False, "User not found."

        cursor.execute(
            """
            INSERT INTO rooms (name, created_by)
            VALUES (?, ?)
            """,
            (room_name, user[0])
        )

        connection.commit()

        return True, "Room created successfully."

    except sqlite3.IntegrityError:
        return False, "A room with that name already exists."

    finally:
        connection.close()


def get_room_id(room_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM rooms
        WHERE name = ?
        """,
        (room_name,)
    )

    room = cursor.fetchone()

    connection.close()

    if room:
        return room[0]

    return None


# =========================
# MESSAGE FUNCTIONS
# =========================

def save_message(room_name, username, message):
    room_id = get_room_id(room_name)

    if room_id is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            room_id,
            username,
            message
        )
        VALUES (?, ?, ?)
        """,
        (
            room_id,
            username,
            message
        )
    )

    connection.commit()
    connection.close()

    return True


def get_message_history(room_name, limit=50):
    room_id = get_room_id(room_name)

    if room_id is None:
        return []

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            username,
            message,
            created_at
        FROM messages
        WHERE room_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            room_id,
            limit
        )
    )

    messages = cursor.fetchall()

    connection.close()

    # Reverse so oldest appears first
    messages.reverse()

    return messages


# =========================
# TEST DATABASE
# =========================

if __name__ == "__main__":
    initialize_database()

    print("Database initialized successfully.")
    print()

    print("Available rooms:")

    for room_id, room_name in get_rooms():
        print(f"- {room_name} (ID: {room_id})")