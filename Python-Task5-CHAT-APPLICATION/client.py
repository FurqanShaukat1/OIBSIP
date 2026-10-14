
import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from plyer import notification

from database import (
    initialize_database,
    register_user,
    login_user,
)

HOST = "127.0.0.1"
PORT = 5555

EMOJI_SHORTCODES = {
    ":smile:": "😄",
    ":grin:": "😁",
    ":heart:": "❤️",
    ":thumbsup:": "👍",
    ":thumbsdown:": "👎",
    ":laugh:": "😂",
    ":sad:": "😢",
    ":angry:": "😠",
    ":fire:": "🔥",
    ":check:": "✅",
    ":star:": "⭐",
    ":wave:": "👋",
}


def convert_emoji_shortcodes(message):
    for shortcode, emoji in EMOJI_SHORTCODES.items():
        message = message.replace(shortcode, emoji)
    return message


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("850x550")
        self.root.minsize(650, 400)

        self.client = None
        self.reader = None
        self.username = ""
        self.current_room = "General"
        self.rooms = []
        self.connected = False

        initialize_database()
        self.show_login_screen()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()

        frame = tk.Frame(self.root, padx=35, pady=25)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Chat Application",
            font=("Arial", 22, "bold"),
        ).pack(pady=(0, 20))

        tk.Label(frame, text="Username").pack(anchor="w")
        self.username_entry = tk.Entry(frame, width=32)
        self.username_entry.pack(pady=(5, 12))

        tk.Label(frame, text="Password").pack(anchor="w")
        self.password_entry = tk.Entry(frame, width=32, show="*")
        self.password_entry.pack(pady=(5, 18))

        tk.Button(
            frame,
            text="Login",
            width=28,
            command=self.login,
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Register",
            width=28,
            command=self.register,
        ).pack(pady=5)

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login(),
        )

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Enter both username and password.",
            )
            return

        if any(char in username for char in ("\n", "\r", "|")):
            messagebox.showwarning(
                "Invalid Username",
                "Username cannot contain | or line breaks.",
            )
            return

        success, message = register_user(username, password)

        if success:
            messagebox.showinfo("Registration", message)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Registration Failed", message)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Enter both username and password.",
            )
            return

        if any(char in username for char in ("\n", "\r", "|")):
            messagebox.showerror(
                "Invalid Username",
                "Username cannot contain | or line breaks.",
            )
            return

        success, message = login_user(username, password)

        if not success:
            messagebox.showerror("Login Failed", message)
            return

        self.username = username

        try:
            self.client = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            self.client.connect((HOST, PORT))
            self.client.sendall(
                (username + "\n").encode("utf-8")
            )

            self.connected = True
            self.show_chat_screen()

            self.reader = self.client.makefile(
                "r",
                encoding="utf-8",
                newline="\n",
            )

            threading.Thread(
                target=self.receive_messages,
                daemon=True,
            ).start()

            self.send_command("/rooms")

        except OSError as error:
            self.connected = False

            if self.client:
                self.client.close()

            self.client = None

            messagebox.showerror(
                "Connection Error",
                f"Could not connect to the server.\n\n{error}\n\n"
                "Make sure server.py is running.",
            )

    def show_chat_screen(self):
        self.clear_window()

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)

        sidebar = tk.Frame(
            main,
            width=200,
            padx=10,
            pady=10,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Chat Rooms",
            font=("Arial", 14, "bold"),
        ).pack(pady=(0, 10))

        self.room_list = tk.Listbox(sidebar, height=18)
        self.room_list.pack(fill="both", expand=True)
        self.room_list.bind(
            "<<ListboxSelect>>",
            self.select_room,
        )

        tk.Button(
            sidebar,
            text="Create Room",
            command=self.create_room,
        ).pack(fill="x", pady=(10, 5))

        tk.Button(
            sidebar,
            text="Refresh Rooms",
            command=lambda: self.send_command("/rooms"),
        ).pack(fill="x", pady=5)

        chat = tk.Frame(main, padx=10, pady=10)
        chat.pack(side="right", fill="both", expand=True)

        self.room_label = tk.Label(
            chat,
            text="Room: General",
            font=("Arial", 15, "bold"),
            anchor="w",
        )
        self.room_label.pack(fill="x", pady=(0, 10))

        self.chat_display = tk.Text(
            chat,
            wrap="word",
            state="disabled",
            font=("Arial", 11),
        )
        self.chat_display.pack(fill="both", expand=True)

        bottom = tk.Frame(chat)
        bottom.pack(fill="x", pady=(10, 0))

        self.message_entry = tk.Entry(
            bottom,
            font=("Arial", 11),
        )
        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
        )
        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message(),
        )

        tk.Button(
            bottom,
            text="Send",
            command=self.send_message,
        ).pack(side="right")

    def send_command(self, command):
        if not self.connected or not self.client:
            return

        try:
            self.client.sendall(
                (command + "\n").encode("utf-8")
            )
        except OSError:
            self.connected = False
            self.root.after(
                0,
                self.show_system_message,
                "Connection to server was lost.",
            )

    def send_message(self):
        message = self.message_entry.get().strip()

        if not message:
            return

        if message.startswith("/"):
            messagebox.showinfo(
                "Command",
                "Use the room buttons to manage rooms.",
            )
            return

        message = convert_emoji_shortcodes(message)
        self.send_command(message)
        self.message_entry.delete(0, tk.END)

    def select_room(self, event=None):
        selection = self.room_list.curselection()

        if not selection:
            return

        room_name = self.room_list.get(selection[0])

        if room_name == self.current_room:
            return

        self.clear_chat()
        self.send_command("/join " + room_name)

    def create_room(self):
        room_name = simpledialog.askstring(
            "Create Room",
            "Enter a room name:",
            parent=self.root,
        )

        if room_name is None:
            return

        room_name = room_name.strip()

        if not room_name:
            messagebox.showwarning(
                "Invalid Room",
                "Room name cannot be empty.",
            )
            return

        if any(char in room_name for char in ("\n", "\r", "|")):
            messagebox.showwarning(
                "Invalid Room",
                "Room name cannot contain | or line breaks.",
            )
            return

        self.send_command("/create " + room_name)

    def receive_messages(self):
        try:
            for line in self.reader:
                message = line.rstrip("\r\n")

                if message:
                    self.root.after(
                        0,
                        self.process_server_message,
                        message,
                    )
        except (OSError, ValueError):
            pass
        finally:
            self.connected = False

            try:
                self.root.after(
                    0,
                    self.show_system_message,
                    "Disconnected from server.",
                )
            except (tk.TclError, RuntimeError):
                pass

    def process_server_message(self, message):
        if message == "ROOM_LIST":
            self.rooms = []

        elif message.startswith("ROOM|"):
            parts = message.split("|", 2)

            if len(parts) == 3:
                self.rooms.append(parts[2])

        elif message == "END_ROOM_LIST":
            self.room_list.delete(0, tk.END)

            for room_name in self.rooms:
                self.room_list.insert(tk.END, room_name)

        elif message.startswith("ROOM_JOINED|"):
            self.current_room = message.split("|", 1)[1]
            self.room_label.config(
                text=f"Room: {self.current_room}"
            )

        elif message.startswith("ROOM_CREATED|"):
            room_name = message.split("|", 1)[1]
            self.show_system_message(
                f"Room '{room_name}' created."
            )
            self.send_command("/rooms")
            self.send_command("/join " + room_name)

        elif message.startswith("CHAT|"):
            chat_message = message.split("|", 1)[1]
            self.show_chat_message(chat_message)

            try:
                window_is_focused = (
                    self.root.focus_displayof() is not None
                )
            except tk.TclError:
                window_is_focused = False

            if not window_is_focused:
                self.show_desktop_notification(
                    "New Chat Message",
                    chat_message,
                )

        elif message.startswith("SYSTEM|"):
            self.show_system_message(
                message.split("|", 1)[1]
            )

        elif message.startswith("ERROR|"):
            error = message.split("|", 1)[1]
            self.show_system_message("Error: " + error)

    def show_chat_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")

    def show_system_message(self, message):
        if not hasattr(self, "chat_display"):
            return

        try:
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, message + "\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state="disabled")
        except tk.TclError:
            pass

    def show_desktop_notification(self, title, message):
        try:
            notification.notify(
                title=title,
                message=message[:200],
                app_name="Chat Application",
                timeout=5,
            )
        except Exception as error:
            print(f"Notification error: {error}")

    def clear_chat(self):
        if not hasattr(self, "chat_display"):
            return

        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state="disabled")

    def close_app(self):
        self.connected = False

        if self.client:
            try:
                self.client.sendall(b"/quit\n")
            except OSError:
                pass

            try:
                self.client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                self.client.close()
            except OSError:
                pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
