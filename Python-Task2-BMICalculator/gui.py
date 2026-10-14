import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt

from bmi import calculate_bmi, classify_bmi

from database import (
    initialize_database,
    get_or_create_user,
    get_user_id,
    save_bmi_record,
    get_user_history
)


class BMICalculatorApp:

    def __init__(self, root):
        self.root = root

        self.root.title("BMI Calculator")
        self.root.geometry("500x680")
        self.root.resizable(False, False)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):

        style = ttk.Style()

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Result.TLabel",
            font=("Segoe UI", 18, "bold")
        )

        style.configure(
            "Calculate.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=10
        )

    def create_widgets(self):

        main_frame = ttk.Frame(
            self.root,
            padding=30
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # -----------------------------
        # TITLE
        # -----------------------------

        ttk.Label(
            main_frame,
            text="BMI Calculator",
            style="Title.TLabel"
        ).pack(
            pady=(10, 5)
        )

        ttk.Label(
            main_frame,
            text="Track your Body Mass Index",
            style="Subtitle.TLabel"
        ).pack(
            pady=(0, 25)
        )

        # -----------------------------
        # USER NAME
        # -----------------------------

        ttk.Label(
            main_frame,
            text="User Name"
        ).pack(
            anchor="w"
        )

        self.name_entry = ttk.Entry(
            main_frame
        )

        self.name_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        # -----------------------------
        # WEIGHT
        # -----------------------------

        ttk.Label(
            main_frame,
            text="Weight (kg)"
        ).pack(
            anchor="w"
        )

        self.weight_entry = ttk.Entry(
            main_frame
        )

        self.weight_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        # -----------------------------
        # HEIGHT
        # -----------------------------

        ttk.Label(
            main_frame,
            text="Height (m)"
        ).pack(
            anchor="w"
        )

        self.height_entry = ttk.Entry(
            main_frame
        )

        self.height_entry.pack(
            fill="x",
            pady=(5, 20)
        )

        # -----------------------------
        # BUTTONS
        # -----------------------------

        button_frame = ttk.Frame(
            main_frame
        )

        button_frame.pack(
            fill="x",
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Calculate BMI",
            style="Calculate.TButton",
            command=self.calculate
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields
        ).pack(
            side="right",
            expand=True,
            fill="x",
            padx=(5, 0)
        )

        # -----------------------------
        # HISTORY BUTTON
        # -----------------------------

        ttk.Button(
            main_frame,
            text="View BMI History & Trend",
            command=self.view_history
        ).pack(
            fill="x",
            pady=(10, 20)
        )

        # -----------------------------
        # BMI RESULT
        # -----------------------------

        self.result_label = ttk.Label(
            main_frame,
            text="BMI: --",
            style="Result.TLabel"
        )

        self.result_label.pack(
            pady=(15, 5)
        )

        # -----------------------------
        # CATEGORY RESULT
        # -----------------------------

        self.category_label = ttk.Label(
            main_frame,
            text="Category: --",
            style="Result.TLabel"
        )

        self.category_label.pack(
            pady=5
        )

    # ==================================================
    # CALCULATE BMI
    # ==================================================

    def calculate(self):

        name = self.name_entry.get().strip()

        weight_text = self.weight_entry.get().strip()

        height_text = self.height_entry.get().strip()

        # Validate user name

        if not name:

            messagebox.showerror(
                "Invalid Input",
                "Please enter a user name."
            )

            return

        # Validate empty fields

        if not weight_text or not height_text:

            messagebox.showerror(
                "Invalid Input",
                "Please enter both weight and height."
            )

            return

        # Convert values

        try:

            weight = float(weight_text)

            height = float(height_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be numeric values."
            )

            return

        # Calculate BMI

        try:

            bmi = calculate_bmi(
                weight,
                height
            )

            category = classify_bmi(
                bmi
            )

        except ValueError as error:

            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

            return

        # Get or create user

        user_id = get_or_create_user(
            name
        )

        if user_id is None:

            messagebox.showerror(
                "Database Error",
                "Unable to create or find the user."
            )

            return

        # Save BMI record

        saved = save_bmi_record(
            user_id,
            weight,
            height,
            bmi,
            category
        )

        if not saved:

            messagebox.showerror(
                "Database Error",
                "Unable to save BMI record."
            )

            return

        # Display BMI

        self.result_label.config(
            text=f"BMI: {bmi:.2f}"
        )

        # Display category

        self.category_label.config(
            text=f"Category: {category}"
        )

        # -----------------------------
        # COLOR-CODED FEEDBACK
        # -----------------------------

        if category == "Underweight":

            result_color = "#2196F3"

        elif category == "Normal":

            result_color = "#2E7D32"

        elif category == "Overweight":

            result_color = "#F57C00"

        else:

            result_color = "#D32F2F"

        self.result_label.config(
            foreground=result_color
        )

        self.category_label.config(
            foreground=result_color
        )

    # ==================================================
    # CLEAR FIELDS
    # ==================================================

    def clear_fields(self):

        self.name_entry.delete(
            0,
            tk.END
        )

        self.weight_entry.delete(
            0,
            tk.END
        )

        self.height_entry.delete(
            0,
            tk.END
        )

        self.result_label.config(
            text="BMI: --",
            foreground="black"
        )

        self.category_label.config(
            text="Category: --",
            foreground="black"
        )

    # ==================================================
    # VIEW HISTORY
    # ==================================================

    def view_history(self):

        name = self.name_entry.get().strip()

        if not name:

            messagebox.showerror(
                "User Required",
                "Please enter a user name first."
            )

            return

        # Find existing user

        user_id = get_user_id(
            name
        )

        if user_id is None:

            messagebox.showinfo(
                "No Records",
                f"No records found for '{name}'."
            )

            return

        # Get history

        records = get_user_history(
            user_id
        )

        if not records:

            messagebox.showinfo(
                "No Records",
                f"No BMI records found for '{name}'."
            )

            return

        # Show history

        self.show_history_window(
            name,
            records
        )

    # ==================================================
    # HISTORY WINDOW
    # ==================================================

    def show_history_window(
        self,
        name,
        records
    ):

        history_window = tk.Toplevel(
            self.root
        )

        history_window.title(
            f"{name} - BMI History"
        )

        history_window.geometry(
            "750x500"
        )

        history_window.resizable(
            False,
            False
        )

        # -----------------------------
        # TITLE
        # -----------------------------

        ttk.Label(
            history_window,
            text=f"{name}'s BMI History",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=15
        )

        # -----------------------------
        # TABLE
        # -----------------------------

        columns = (
            "weight",
            "height",
            "bmi",
            "category",
            "date"
        )

        table = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings",
            height=12
        )

        table.heading(
            "weight",
            text="Weight (kg)"
        )

        table.heading(
            "height",
            text="Height (m)"
        )

        table.heading(
            "bmi",
            text="BMI"
        )

        table.heading(
            "category",
            text="Category"
        )

        table.heading(
            "date",
            text="Date"
        )

        table.column(
            "weight",
            width=100
        )

        table.column(
            "height",
            width=100
        )

        table.column(
            "bmi",
            width=80
        )

        table.column(
            "category",
            width=120
        )

        table.column(
            "date",
            width=180
        )

        # Add records

        for record in records:

            weight = record[0]

            height = record[1]

            bmi = record[2]

            category = record[3]

            recorded_at = record[4]

            table.insert(
                "",
                tk.END,
                values=(
                    f"{weight:.2f}",
                    f"{height:.2f}",
                    f"{bmi:.2f}",
                    category,
                    recorded_at
                )
            )

        table.pack(
            padx=20,
            pady=10
        )

        # -----------------------------
        # GRAPH BUTTON
        # -----------------------------

        ttk.Button(
            history_window,
            text="View BMI Trend Graph",
            command=lambda: self.show_graph(
                name,
                records
            )
        ).pack(
            pady=15
        )

    # ==================================================
    # BMI TREND GRAPH
    # ==================================================

    def show_graph(
        self,
        name,
        records
    ):

        dates = []

        bmi_values = []

        for record in records:

            bmi_values.append(
                record[2]
            )

            dates.append(
                record[4]
            )

        # Create graph

        plt.figure(
            figsize=(10, 5)
        )

        plt.plot(
            dates,
            bmi_values,
            marker="o",
            linewidth=2
        )

        plt.title(
            f"BMI Trend - {name}"
        )

        plt.xlabel(
            "Date"
        )

        plt.ylabel(
            "BMI"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.grid(
            True,
            alpha=0.3
        )

        plt.tight_layout()

        plt.show()


# ======================================================
# START APPLICATION
# ======================================================

def start_app():

    initialize_database()

    root = tk.Tk()

    app = BMICalculatorApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    start_app()