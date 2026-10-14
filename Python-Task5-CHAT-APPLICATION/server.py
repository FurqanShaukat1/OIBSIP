
import socket
import threading
from datetime import datetime

from database import (
    initialize_database,
    get_rooms,
    get_room_id,
    create_room as create_database_room,
    save_message,
    get_message_history,
)

HOST = "127.0.0.1"
PORT = 5555

clients = {}
clients_lock = threading.Lock()


def timestamp():
    return datetime.now().strftime("%H:%M")


def send_message(client, message):
    try:
        client.sendall((message + "\n").encode("utf-8"))
        return True
    except OSError:
        return False


def broadcast(room_name, message, exclude=None):
    with clients_lock:
        recipients = [
            client
            for client, info in clients.items()
            if info["room"] == room_name and client != exclude
        ]

    for client in recipients:
        if not send_message(client, message):
            remove_client(client)


def send_history(client, room_name):
    history = get_message_history(room_name)

    send_message(client, f"SYSTEM|History for {room_name}")

    for username, message, created_at in history:
        try:
            time_text = created_at.split(" ")[1][:5]
        except (AttributeError, IndexError):
            time_text = timestamp()

        send_message(
            client,
            f"CHAT|[{time_text}] {username}: {message}"
        )

    send_message(client, "SYSTEM|End of history")


def send_room_list(client):
    send_message(client, "ROOM_LIST")

    for room_id, room_name in get_rooms():
        send_message(client, f"ROOM|{room_id}|{room_name}")

    send_message(client, "END_ROOM_LIST")


def join_room(client, room_name):
    room_name = room_name.strip()

    if not room_name or get_room_id(room_name) is None:
        send_message(client, "ERROR|Room does not exist.")
        return

    with clients_lock:
        if client not in clients:
            return

        old_room = clients[client]["room"]
        username = clients[client]["username"]
        clients[client]["room"] = room_name

    if old_room != room_name:
        broadcast(
            old_room,
            f"SYSTEM|{username} left {old_room}"
        )

    send_message(client, f"ROOM_JOINED|{room_name}")
    send_history(client, room_name)

    if old_room != room_name:
        broadcast(
            room_name,
            f"SYSTEM|{username} joined {room_name}",
            exclude=client
        )


def handle_command(client, message):
    if message == "/rooms":
        send_room_list(client)

    elif message.startswith("/join "):
        join_room(client, message[6:])

    elif message.startswith("/create "):
        room_name = message[8:].strip()

        with clients_lock:
            username = clients.get(client, {}).get("username")

        if not username:
            return

        success, result = create_database_room(room_name, username)

        if success:
            send_message(client, f"ROOM_CREATED|{room_name}")
            send_room_list(client)
        else:
            send_message(client, f"ERROR|{result}")

    elif message == "/quit":
        remove_client(client)

    else:
        with clients_lock:
            info = clients.get(client)

            if not info:
                return

            username = info["username"]
            room_name = info["room"]

        if not message.strip():
            return

        save_message(room_name, username, message)

        formatted = f"CHAT|[{timestamp()}] {username}: {message}"
        print(f"[{room_name}] {formatted[5:]}")

        broadcast(room_name, formatted)


def remove_client(client):
    with clients_lock:
        info = clients.pop(client, None)

    if info is None:
        return

    try:
        client.close()
    except OSError:
        pass

    username = info["username"]
    room_name = info["room"]

    broadcast(
        room_name,
        f"SYSTEM|{username} disconnected"
    )

    print(f"{username} disconnected from {room_name}")


def handle_client(client, address):
    print(f"Connection from {address}")

    try:
        reader = client.makefile("r", encoding="utf-8", newline="\n")

        username = reader.readline().strip()

        if not username:
            return

        with clients_lock:
            clients[client] = {
                "username": username,
                "room": "General",
            }

        print(f"{username} connected")

        send_message(client, "ROOM_JOINED|General")
        send_history(client, "General")
        send_room_list(client)

        broadcast(
            "General",
            f"SYSTEM|{username} joined General",
            exclude=client
        )

        for line in reader:
            message = line.rstrip("\r\n")

            if message == "/quit":
                break

            handle_command(client, message)

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        pass

    finally:
        remove_client(client)


def start_server():
    initialize_database()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print("=" * 40)
    print("          CHAT SERVER")
    print("=" * 40)
    print(f"Running on {HOST}:{PORT}")
    print("Default room: General")
    print("Waiting for clients...")

    try:
        while True:
            client, address = server.accept()

            threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            ).start()

    except KeyboardInterrupt:
        print("\nShutting down server...")

    finally:
        with clients_lock:
            connected_clients = list(clients.keys())

        for client in connected_clients:
            try:
                client.close()
            except OSError:
                pass

        server.close()


if __name__ == "__main__":
    start_server()
