import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

from password_generator import generate_password


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Random Password Generator")
        self.root.geometry("700x750")
        self.root.minsize(600, 600)

        self.setup_variables()
        self.create_widgets()

    # ==========================================================
    # VARIABLES
    # ==========================================================

    def setup_variables(self):
        self.length_var = tk.IntVar(value=16)

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        self.password_var = tk.StringVar()
        self.strength_var = tk.StringVar(value="Strength: -")

        # Store only the latest 5 passwords
        self.password_history = []

    # ==========================================================
    # MAIN UI
    # ==========================================================

    def create_widgets(self):

        # ------------------------------------------------------
        # Scrollable container
        # ------------------------------------------------------

        outer_frame = ttk.Frame(self.root)
        outer_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            outer_frame,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Make inner frame follow canvas width
        self.canvas.bind(
            "<Configure>",
            self.resize_scrollable_frame
        )

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        # ------------------------------------------------------
        # Main content
        # ------------------------------------------------------

        content = self.scrollable_frame

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        title = ttk.Label(
            content,
            text="Random Password Generator",
            font=("Arial", 22, "bold")
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ttk.Label(
            content,
            text="Create a strong and secure password",
            font=("Arial", 11)
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # Generated Password
        # ------------------------------------------------------

        password_frame = ttk.LabelFrame(
            content,
            text="Generated Password",
            padding=15
        )

        password_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Arial", 16),
            justify="center"
        )

        self.password_entry.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # ------------------------------------------------------
        # Password Length
        # ------------------------------------------------------

        length_frame = ttk.LabelFrame(
            content,
            text="Password Length",
            padding=15
        )

        length_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        self.length_label = ttk.Label(
            length_frame,
            text="16",
            font=("Arial", 10)
        )

        self.length_label.pack(
            pady=(0, 5)
        )

        self.length_scale = ttk.Scale(
            length_frame,
            from_=8,
            to=64,
            orient="horizontal",
            command=self.update_length
        )

        self.length_scale.set(16)

        self.length_scale.pack(
            fill="x",
            padx=10,
            pady=5
        )

        # ------------------------------------------------------
        # Character Types
        # ------------------------------------------------------

        types_frame = ttk.LabelFrame(
            content,
            text="Character Types",
            padding=15
        )

        types_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ttk.Checkbutton(
            types_frame,
            text="Uppercase Letters (A-Z)",
            variable=self.uppercase_var
        ).pack(
            anchor="w",
            pady=3
        )

        ttk.Checkbutton(
            types_frame,
            text="Lowercase Letters (a-z)",
            variable=self.lowercase_var
        ).pack(
            anchor="w",
            pady=3
        )

        ttk.Checkbutton(
            types_frame,
            text="Numbers (0-9)",
            variable=self.numbers_var
        ).pack(
            anchor="w",
            pady=3
        )

        ttk.Checkbutton(
            types_frame,
            text="Symbols (!@#$...)",
            variable=self.symbols_var
        ).pack(
            anchor="w",
            pady=3
        )

        ttk.Checkbutton(
            types_frame,
            text="Exclude ambiguous characters (0, O, o, I, l, 1)",
            variable=self.exclude_ambiguous_var
        ).pack(
            anchor="w",
            pady=3
        )

        # ------------------------------------------------------
        # Strength
        # ------------------------------------------------------

        self.strength_label = ttk.Label(
            content,
            textvariable=self.strength_var,
            font=("Arial", 12, "bold")
        )

        self.strength_label.pack(
            pady=15
        )

        # ------------------------------------------------------
        # Buttons - SAME LINE
        # ------------------------------------------------------

        button_frame = ttk.Frame(content)

        button_frame.pack(
            pady=10
        )

        generate_button = ttk.Button(
            button_frame,
            text="Generate Password",
            command=self.generate
        )

        generate_button.pack(
            side="left",
            padx=5,
            ipadx=20,
            ipady=8
        )

        copy_button = ttk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.copy_password
        )

        copy_button.pack(
            side="left",
            padx=5,
            ipadx=20,
            ipady=8
        )

        # ------------------------------------------------------
        # Recent Passwords
        # ------------------------------------------------------

        history_frame = ttk.LabelFrame(
            content,
            text="Recent Passwords",
            padding=10
        )

        history_frame.pack(
            fill="x",
            padx=40,
            pady=(15, 10)
        )

        self.history_listbox = tk.Listbox(
            history_frame,
            height=6,
            font=("Consolas", 10)
        )

        self.history_listbox.pack(
            fill="x",
            expand=True
        )

        history_note = ttk.Label(
            history_frame,
            text="Only the last 5 passwords are kept during this session.",
            font=("Arial", 9)
        )

        history_note.pack(
            pady=(8, 0)
        )

        # ------------------------------------------------------
        # Bottom spacing
        # ------------------------------------------------------

        ttk.Label(
            content,
            text=""
        ).pack(
            pady=15
        )

    # ==========================================================
    # SCROLLING
    # ==========================================================

    def resize_scrollable_frame(self, event):
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================================
    # LENGTH
    # ==========================================================

    def update_length(self, value):
        length = int(float(value))

        self.length_var.set(length)

        self.length_label.config(
            text=str(length)
        )

    # ==========================================================
    # GENERATE PASSWORD
    # ==========================================================

    def generate(self):
        try:
            password = generate_password(
                length=self.length_var.get(),
                use_uppercase=self.uppercase_var.get(),
                use_lowercase=self.lowercase_var.get(),
                use_numbers=self.numbers_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.exclude_ambiguous_var.get()
            )

            self.password_var.set(password)

            # Calculate strength
            strength = self.calculate_strength(password)

            self.strength_var.set(
                f"Strength: {strength}"
            )

            # Add password to history
            self.add_to_history(password)

        except TypeError:
            # Fallback in case password_generator.py
            # does not yet support exclude_ambiguous
            try:
                password = generate_password(
                    length=self.length_var.get(),
                    use_uppercase=self.uppercase_var.get(),
                    use_lowercase=self.lowercase_var.get(),
                    use_numbers=self.numbers_var.get(),
                    use_symbols=self.symbols_var.get()
                )

                # Apply ambiguous filtering if enabled
                if self.exclude_ambiguous_var.get():
                    ambiguous = "0OoIl1"

                    if any(char in ambiguous for char in password):
                        messagebox.showwarning(
                            "Ambiguous Character",
                            "The generated password contains an ambiguous character."
                        )

                self.password_var.set(password)

                strength = self.calculate_strength(password)

                self.strength_var.set(
                    f"Strength: {strength}"
                )

                self.add_to_history(password)

            except ValueError as error:
                messagebox.showerror(
                    "Invalid Selection",
                    str(error)
                )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Selection",
                str(error)
            )

    # ==========================================================
    # PASSWORD STRENGTH
    # ==========================================================

    def calculate_strength(self, password):
        length = len(password)

        has_uppercase = any(
            char.isupper()
            for char in password
        )

        has_lowercase = any(
            char.islower()
            for char in password
        )

        has_number = any(
            char.isdigit()
            for char in password
        )

        has_symbol = any(
            not char.isalnum()
            for char in password
        )

        diversity = sum([
            has_uppercase,
            has_lowercase,
            has_number,
            has_symbol
        ])

        if length >= 16 and diversity >= 3:
            return "Strong"

        elif length >= 12 and diversity >= 2:
            return "Medium"

        else:
            return "Weak"

    # ==========================================================
    # PASSWORD HISTORY
    # ==========================================================

    def add_to_history(self, password):

        self.password_history.insert(
            0,
            password
        )

        # Keep only latest 5
        self.password_history = self.password_history[:5]

        # Update listbox
        self.history_listbox.delete(
            0,
            tk.END
        )

        for index, item in enumerate(
            self.password_history,
            start=1
        ):
            self.history_listbox.insert(
                tk.END,
                f"{index}. {item}"
            )

    # ==========================================================
    # COPY TO CLIPBOARD
    # ==========================================================

    def copy_password(self):
        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )

            return

        try:
            pyperclip.copy(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard."
            )

        except Exception as error:
            messagebox.showerror(
                "Clipboard Error",
                f"Could not copy password:\n{error}"
            )


# ==============================================================
# APPLICATION START
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordGeneratorApp(root)

    root.mainloop()