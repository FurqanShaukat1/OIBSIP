# Python Chat Application

A real-time chat application built with Python, Tkinter, sockets, threading, and SQLite. Users can register, log in, exchange messages, and communicate in different chat rooms through a graphical user interface.

## Features

- User registration and login
- Password hashing before storing credentials
- Real-time messaging using Python sockets
- Graphical user interface using Tkinter
- Multiple chat rooms
- Create and join chat rooms
- Message history stored in SQLite
- Desktop notifications for incoming messages
- Emoji shortcodes
- Support for multiple clients
- Separate server and client applications

## Technologies Used

- **Python 3** — Core programming language
- **Tkinter** — Graphical user interface
- **Socket** — Network communication
- **Threading** — Handling multiple clients and background tasks
- **SQLite** — Database storage
- **Plyer** — Desktop notifications

## Project Structure

```text
chat_application/
├── server.py
├── client.py
├── database.py
├── chat.db
├── requirements.txt
├── README.md
└── venv/
```

**Note:** The `venv/` directory contains the local virtual environment and should not normally be uploaded with the project. The `chat.db` file stores local application data and may contain test accounts and messages.

## Requirements

Before running the application, make sure you have:

- Python 3 installed
- pip package manager
- Windows, Linux, or macOS
- A terminal or command prompt

Tkinter and SQLite are generally included with standard Python installations. Desktop notification support requires the `plyer` package.

## Installation

### 1. Open the project folder

Open PowerShell or a terminal inside the project directory:

```powershell
cd "C:\Users\Hp\Desktop\Indian Internship\chat_application"
```

If your project is stored somewhere else, use its actual folder path.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment on Windows

For PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Command Prompt:

```cmd
venv\Scripts\activate.bat
```

After activation, the terminal should show `(venv)`.

### 4. Install dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Make sure `requirements.txt` includes:

```text
plyer
```

## Running the Application

The server must be running before clients can connect.

### 1. Start the server

Open a terminal in the project directory, activate the virtual environment, and run:

```powershell
python server.py
```

Keep this terminal open while using the application.

### 2. Start the first client

Open a second terminal in the same project directory. Activate the virtual environment and run:

```powershell
python client.py
```

The chat application's graphical interface should open.

### 3. Register or log in

- Register a new account if you do not already have one.
- Log in using your registered username and password.
- Select a chat room to start communicating.

### 4. Test multiple users

To test real-time communication:

1. Keep the server running.
2. Start `client.py` in a second terminal.
3. Log in using a different registered account.
4. Join the same chat room from both clients.
5. Send messages and verify that they appear on both clients.

For testing on the same computer, both clients can connect to the local server if the application is configured for local connections.

## Chat Rooms

The application supports communication through separate chat rooms.

- A default `General` room is available.
- Users can create additional chat rooms.
- Users can select and join available rooms.
- Messages are stored in the SQLite database.
- Recent message history is loaded when a user joins a room.

Messages belong to their respective rooms, allowing users to participate in different conversations.

## Emoji Shortcodes

The client supports the following emoji shortcodes:

| Shortcode | Emoji |
|---|---|
| `:smile:` | 😄 |
| `:grin:` | 😁 |
| `:heart:` | ❤️ |
| `:thumbsup:` | 👍 |
| `:thumbsdown:` | 👎 |
| `:laugh:` | 😂 |
| `:sad:` | 😢 |
| `:angry:` | 😠 |
| `:fire:` | 🔥 |
| `:check:` | ✅ |
| `:star:` | ⭐ |
| `:wave:` | 👋 |

Type a supported shortcode in a message to use its corresponding emoji.

**Note:** Emoji appearance depends on the operating system, installed fonts, and Tkinter's text-rendering support. Some emojis may appear differently or as boxes on certain systems.

## Database Storage

The application uses SQLite for local data storage. Its database file is named `chat.db`.

The database contains the following tables:

- **`users`** — Stores usernames and password hashes.
- **`rooms`** — Stores chat room information.
- **`messages`** — Stores chat messages, associated usernames or room information, and timestamps, according to the database schema.

The `database.py` module initializes the database and manages database-related operations.

Database initialization can be tested by running:

```powershell
python database.py
```

The exact initialization behavior depends on the implementation in `database.py`.

**Important:** Back up the database before deleting or resetting it if you want to preserve existing accounts, rooms, and messages.

## Desktop Notifications

The application uses the Plyer library to display desktop notifications for incoming messages when the chat window is not focused, as implemented in the client.

Notification behavior may depend on:

- Operating system support
- System notification permissions
- Notification settings
- Whether the application is running

If notifications do not appear, verify that Plyer is installed in the active virtual environment:

```powershell
python -c "import plyer; print('Plyer OK')"
```

Expected output:

```text
Plyer OK
```

## Testing Checklist

Use this checklist to verify the application's main features before submission.

- [ ] Register a new user.
- [ ] Log in with valid credentials.
- [ ] Verify that invalid login credentials are rejected.
- [ ] Open two clients simultaneously.
- [ ] Send messages between different users.
- [ ] Create a new chat room.
- [ ] Join an existing chat room.
- [ ] Verify that messages appear in the correct room.
- [ ] Verify that recent message history loads.
- [ ] Test the supported emoji shortcodes.
- [ ] Test desktop notifications.
- [ ] Verify behavior when the server is stopped.
- [ ] Restart the server and verify the application can reconnect or report connection errors appropriately.
- [ ] Verify that the database retains expected data after restarting the application.

## Security and Encryption Limitations

This project is intended for educational purposes and demonstration.

- Passwords are hashed before being stored in the database.
- If SHA-256 is used for password hashing, it should be replaced with a password-specific algorithm such as Argon2id, bcrypt, or PBKDF2 for production use.
- The current socket connection does not provide TLS encryption unless separately implemented.
- The application does not implement end-to-end encryption (E2EE).
- Messages stored in SQLite are readable from the database file.
- Network exposure, authentication, input validation, and error handling should be reviewed before deployment beyond a trusted local testing environment.

Do not use this educational application to exchange sensitive information without appropriate security improvements.

## Troubleshooting

### The `plyer` module is missing

Activate the virtual environment and run:

```powershell
python -m pip install plyer
```

Then verify the installation:

```powershell
python -c "import plyer; print('Plyer OK')"
```

### The client cannot connect to the server

- Make sure `server.py` is running.
- Verify the host and port settings in `server.py` and `client.py`.
- Confirm that the client is configured to connect to the correct server address.
- Check whether a firewall is blocking the connection.

### The database is not initialized

Run:

```powershell
python database.py
```

Check the terminal output for errors. Avoid deleting `chat.db` unless you are prepared to lose its stored data.

### Emojis do not display correctly

Emoji rendering depends on the system's fonts and text-rendering support. Try a supported font or replace unsupported emoji characters if necessary.

## Future Improvements

Possible improvements include:

- Stronger password hashing
- TLS-encrypted client-server communication
- End-to-end encryption
- Improved emoji rendering
- Better connection recovery and error handling
- User profile management
- Private messaging
- Message delivery indicators
- More comprehensive automated tests

These are potential future enhancements and are not necessarily implemented in the current version.

## Author

Developed as a Python internship project.
