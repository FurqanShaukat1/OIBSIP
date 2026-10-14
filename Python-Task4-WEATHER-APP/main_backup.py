import tkinter as tk

from io import BytesIO

from datetime import datetime

import requests

from PIL import Image, ImageTk

from weather_service import WeatherService

# ============================================================

# ROUNDED CARD

# ============================================================

class RoundedCard(tk.Canvas):

    def __init__(

        self,

        parent,

        width,

        height,

        bg="#12161C",

        border="#303640",

        radius=24,

        border_width=1

    ):

        super().__init__(

            parent,

            width=width,

            height=height,

            bg=parent.cget("bg"),

            highlightthickness=0,

            bd=0

        )

        self.card_bg = bg

        self.border = border

        self.radius = radius

        self.border_width = border_width

        self.draw_card()

        self.inner = tk.Frame(

            self,

            bg=bg

        )

        self.create_window(

            width / 2,

            height / 2,

            window=self.inner,

            width=width - (border_width * 2),

            height=height - (border_width * 2),

            anchor="center"

        )

    def draw_card(self):

        self.delete("card")

        self.create_round_rect(

            self.border_width,

            self.border_width,

            self.winfo_reqwidth() - self.border_width,

            self.winfo_reqheight() - self.border_width,

            self.radius,

            fill=self.card_bg,

            outline=self.border,

            width=self.border_width,

            tags="card"

        )

    def create_round_rect(

        self,

        x1,

        y1,

        x2,

        y2,

        radius,

        **kwargs

    ):

        points = [

            x1 + radius, y1,

            x2 - radius, y1,

            x2, y1,

            x2, y1 + radius,

            x2, y2 - radius,

            x2, y2,

            x2 - radius, y2,

            x1 + radius, y2,

            x1, y2,

            x1, y2 - radius,

            x1, y1 + radius,

            x1, y1

        ]

        return self.create_polygon(

            points,

            smooth=True,

            **kwargs

        )

# ============================================================

# ROUNDED BUTTON

# ============================================================

class RoundedButton(tk.Canvas):

    def __init__(

        self,

        parent,

        text,

        command,

        width=130,

        height=46,

        radius=22,

        bg="#FBBF55",

        fg="#17120A",

        hover_bg="#FFD978",

        font=("Segoe UI", 10, "bold")

    ):

        super().__init__(

            parent,

            width=width,

            height=height,

            bg=parent.cget("bg"),

            highlightthickness=0,

            bd=0

        )

        self.command = command

        self.normal_bg = bg

        self.hover_bg = hover_bg

        self.fg = fg

        self.radius = radius

        self.button_text = text

        self.font = font

        self.draw_button()

        self.bind(

            "<Enter>",

            self.on_enter

        )

        self.bind(

            "<Leave>",

            self.on_leave

        )

        self.bind(

            "<Button-1>",

            self.on_click

        )

    def draw_button(self):

        self.delete("all")

        self.create_round_rect(

            1,

            1,

            self.winfo_reqwidth() - 1,

            self.winfo_reqheight() - 1,

            self.radius,

            fill=self.normal_bg,

            outline=""

        )

        self.create_text(

            self.winfo_reqwidth() / 2,

            self.winfo_reqheight() / 2,

            text=self.button_text,

            fill=self.fg,

            font=self.font

        )

    def create_round_rect(

        self,

        x1,

        y1,

        x2,

        y2,

        radius,

        **kwargs

    ):

        points = [

            x1 + radius, y1,

            x2 - radius, y1,

            x2, y1,

            x2, y1 + radius,

            x2, y2 - radius,

            x2, y2,

            x2 - radius, y2,

            x1 + radius, y2,

            x1, y2,

            x1, y2 - radius,

            x1, y1 + radius,

            x1, y1

        ]

        return self.create_polygon(

            points,

            smooth=True,

            **kwargs

        )

    def on_enter(self, event):

        self.itemconfig(

            1,

            fill=self.hover_bg

        )

    def on_leave(self, event):

        self.itemconfig(

            1,

            fill=self.normal_bg

        )

    def on_click(self, event):

        self.command()

# ============================================================

# ROUNDED SEARCH ENTRY

# ============================================================

class RoundedEntry(tk.Frame):

    def __init__(

        self,

        parent,

        placeholder="Search for a city...",

        width=690,

        height=58

    ):

        super().__init__(

            parent,

            bg=parent.cget("bg"),

            width=width,

            height=height

        )

        self.placeholder = placeholder

        self.pack_propagate(False)

        self.canvas = tk.Canvas(

            self,

            bg=parent.cget("bg"),

            highlightthickness=0,

            bd=0

        )

        self.canvas.pack(

            fill="both",

            expand=True

        )

        self.create_round_rect(

            1,

            1,

            width - 1,

            height - 1,

            28,

            fill="#12161C",

            outline="#414752",

            width=1

        )

        # Search icon

        self.canvas.create_text(

            28,

            height / 2,

            text="⌕",

            font=("Segoe UI", 25),

            fill="#FBBF55"

        )

        # Entry

        self.entry = tk.Entry(

            self.canvas,

            font=("Segoe UI", 12),

            bg="#12161C",

            fg="#8B95A5",

            insertbackground="#FBBF55",

            relief="flat",

            bd=0

        )

        self.entry.insert(

            0,

            placeholder

        )

        self.canvas.create_window(

            62,

            height / 2,

            window=self.entry,

            anchor="w",

            width=width - 85,

            height=40

        )

        self.entry.bind(

            "<FocusIn>",

            self.focus_in

        )

        self.entry.bind(

            "<FocusOut>",

            self.focus_out

        )

    def create_round_rect(

        self,

        x1,

        y1,

        x2,

        y2,

        radius,

        **kwargs

    ):

        points = [

            x1 + radius, y1,

            x2 - radius, y1,

            x2, y1,

            x2, y1 + radius,

            x2, y2 - radius,

            x2, y2,

            x2 - radius, y2,

            x1 + radius, y2,

            x1, y2,

            x1, y2 - radius,

            x1, y1 + radius,

            x1, y1

        ]

        return self.canvas.create_polygon(

            points,

            smooth=True,

            **kwargs

        )

    def focus_in(self, event):

        if self.entry.get() == self.placeholder:

            self.entry.delete(

                0,

                tk.END

            )

            self.entry.config(

                fg="#F8FAFC"

            )

    def focus_out(self, event):

        if not self.entry.get():

            self.entry.insert(

                0,

                self.placeholder

            )

            self.entry.config(

                fg="#8B95A5"

            )

    def get(self):

        value = self.entry.get().strip()

        if value == self.placeholder:

            return ""

        return value

    def bind_return(self, command):

        self.entry.bind(

            "<Return>",

            lambda event: command()

        )

# ============================================================

# WEATHER APP

# ============================================================

class WeatherApp:

    # ========================================================

    # COLORS

    # ========================================================

    BG = "#080A0D"

    CARD = "#12161C"

    CARD_LIGHT = "#181D25"

    BORDER = "#303640"

    WARM_BORDER = "#4A3927"

    WHITE = "#F8FAFC"

    TEXT = "#E5E7EB"

    MUTED = "#8B95A5"

    GOLD = "#FBBF55"

    GOLD_LIGHT = "#FFD978"

    BLUE = "#38BDF8"

    PURPLE = "#A78BFA"

    GREEN = "#6EE7B7"

    ERROR = "#FB7185"

    # ========================================================

    # INIT

    # ========================================================

    def __init__(self, root):

        self.root = root

        self.root.title("Weather")

        self.root.geometry(

            "1000x950"

        )

        self.root.minsize(

            900,

            850

        )

        self.root.configure(

            bg=self.BG

        )

        self.weather_service = WeatherService()

        self.current_weather = None

        self.unit = "C"

        self.weather_icon = None
        self.forecast_data = []

        self.create_background()

        self.create_ui()

    # ========================================================

    # BACKGROUND

    # ========================================================

    def create_background(self):

        self.background = tk.Canvas(

            self.root,

            bg=self.BG,

            highlightthickness=0

        )

        self.background.pack(

            fill="both",

            expand=True

        )

        # Top warm glow

        self.background.create_oval(

            700,

            -180,

            1200,

            320,

            fill="#24170B",

            outline=""

        )

        # Bottom warm glow

        self.background.create_oval(

            -250,

            700,

            350,

            1150,

            fill="#1C130B",

            outline=""

        )

        self.content = tk.Frame(

            self.root,

            bg=self.BG

        )

        self.background.configure(
            yscrollcommand=self._on_background_scroll
        )

        self.content_window = self.background.create_window(
            450,
            0,
            window=self.content,
            width=900,
            anchor="n"
        )

        self.content.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self.background.bind(
            "<MouseWheel>",
            self._mousewheel_scroll
        )
        self.content.bind(
            "<MouseWheel>",
            self._mousewheel_scroll
        )

        self.v_scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.background.yview,
            troughcolor="#0D1014",
            bg="#3A414B",
            activebackground=self.GOLD,
            width=12
        )
        self.v_scrollbar.place(
            relx=1.0,
            rely=0,
            relheight=1.0,
            anchor="ne"
        )

    # ========================================================

    # UI

    # ========================================================

    def _update_scroll_region(self, event=None):
        self.background.configure(
            scrollregion=self.background.bbox("all")
        )

    def _on_background_scroll(self, first, last):
        self.v_scrollbar.set(first, last)

    def _mousewheel_scroll(self, event):
        self.background.yview_scroll(
            int(-event.delta / 120),
            "units"
        )

    def create_ui(self):

        # ====================================================

        # HEADER

        # ====================================================

        header = tk.Frame(

            self.content,

            bg=self.BG

        )

        header.pack(

            fill="x",

            pady=(38, 22)

        )

        title_frame = tk.Frame(

            header,

            bg=self.BG

        )

        title_frame.pack(

            side="left"

        )

        tk.Label(

            title_frame,

            text="Weather",

            font=("Segoe UI", 38, "bold"),

            bg=self.BG,

            fg=self.WHITE

        ).pack(

            anchor="w"

        )

        tk.Label(

            title_frame,

            text="Real-time weather intelligence",

            font=("Segoe UI", 12),

            bg=self.BG,

            fg=self.MUTED

        ).pack(

            anchor="w",

            pady=(3, 0)

        )

        # LIVE badge

        live = tk.Frame(

            header,

            bg="#141A17",

            highlightbackground="#33453A",

            highlightthickness=1,

            width=100,

            height=36

        )

        live.pack(

            side="right",

            pady=12

        )

        live.pack_propagate(False)

        tk.Label(

            live,

            text="●  LIVE",

            font=("Segoe UI", 9, "bold"),

            bg="#141A17",

            fg=self.GREEN

        ).pack(

            expand=True

        )

        # ====================================================

        # SEARCH

        # ====================================================

        search_row = tk.Frame(

            self.content,

            bg=self.BG

        )

        search_row.pack(

            fill="x",

            pady=(0, 28)

        )

        self.search_entry = RoundedEntry(

            search_row,

            placeholder="Search for a city...",

            width=690,

            height=58

        )

        self.search_entry.pack(

            side="left"

        )

        self.search_button = RoundedButton(

            search_row,

            text="Search  →",

            command=self.get_weather,

            width=145,

            height=58,

            radius=29,

            bg=self.GOLD,

            fg="#17120A",

            hover_bg=self.GOLD_LIGHT

        )

        self.search_button.pack(

            side="left",

            padx=(12, 0)

        )

        self.search_entry.bind_return(

            self.get_weather

        )

        # ====================================================

        # ERROR

        # ====================================================

        self.error_label = tk.Label(

            self.content,

            text="",

            font=("Segoe UI", 10),

            bg=self.BG,

            fg=self.ERROR

        )

        self.error_label.pack(

            pady=(0, 8)

        )

        # ====================================================

        # MAIN WEATHER CARD

        # ====================================================

        weather_card_widget = RoundedCard(

            self.content,

            width=900,

            height=465,

            bg=self.CARD,

            border=self.WARM_BORDER,

            radius=28

        )

        weather_card_widget.pack(

            fill="x",

            pady=(0, 5)

        )

        weather_card = weather_card_widget.inner

        # ====================================================

        # WEATHER CARD HEADER

        # ====================================================

        top = tk.Frame(

            weather_card,

            bg=self.CARD

        )

        top.pack(

            fill="x",

            padx=30,

            pady=(26, 0)

        )

        self.city_label = tk.Label(

            top,

            text="Your Location",

            font=("Segoe UI", 24, "bold"),

            bg=self.CARD,

            fg=self.WHITE

        )

        self.city_label.pack(

            side="left"

        )

        self.date_label = tk.Label(

            top,

            text=datetime.now().strftime("%d %b %Y"),

            font=("Segoe UI", 10),

            bg=self.CARD,

            fg=self.MUTED

        )

        self.date_label.pack(

            side="right"

        )

        self.location_status = tk.Label(

            weather_card,

            text="⌖  Search for a city",

            font=("Segoe UI", 11),

            bg=self.CARD,

            fg=self.MUTED

        )

        self.location_status.pack(

            anchor="w",

            padx=30,

            pady=(5, 18)

        )

        # ====================================================

        # MAIN WEATHER

        # ====================================================

        weather_main = tk.Frame(

            weather_card,

            bg=self.CARD

        )

        weather_main.pack(

            fill="x",

            padx=30

        )

        # Weather icon

        self.icon_label = tk.Label(

            weather_main,

            text="☁",

            font=("Segoe UI", 72),

            bg=self.CARD,

            fg=self.GOLD

        )

        self.icon_label.pack(

            side="left",

            padx=(15, 35)

        )

        # Temperature

        temperature_frame = tk.Frame(

            weather_main,

            bg=self.CARD

        )

        temperature_frame.pack(

            side="left"

        )

        self.temperature_label = tk.Label(

            temperature_frame,

            text="--°",

            font=("Segoe UI", 70, "bold"),

            bg=self.CARD,

            fg=self.WHITE

        )

        self.temperature_label.pack(

            anchor="w"

        )

        self.condition_label = tk.Label(

            temperature_frame,

            text="Waiting for weather",

            font=("Segoe UI", 17, "bold"),

            bg=self.CARD,

            fg=self.GOLD

        )

        self.condition_label.pack(

            anchor="w"

        )

        self.feels_like_label = tk.Label(

            temperature_frame,

            text="Feels like --°",

            font=("Segoe UI", 11),

            bg=self.CARD,

            fg=self.MUTED

        )

        self.feels_like_label.pack(

            anchor="w",

            pady=(3, 0)

        )

        # ====================================================

        # STAT CARDS

        # ====================================================

        stats = tk.Frame(

            weather_card,

            bg=self.CARD

        )

        stats.pack(

            pady=(30, 25)

        )

        # Humidity

        self.humidity_box = self.create_stat(

            stats,

            "💧",

            "HUMIDITY",

            "--%",

            self.BLUE

        )

        self.humidity_box.pack(

            side="left",

            padx=(0, 7)

        )

        # Wind

        self.wind_box = self.create_stat(

            stats,

            "≋",

            "WIND SPEED",

            "-- m/s",

            self.PURPLE

        )

        self.wind_box.pack(

            side="left",

            padx=7

        )

        # Pressure

        self.pressure_box = self.create_stat(

            stats,

            "♨",

            "PRESSURE",

            "-- hPa",

            self.GOLD

        )

        self.pressure_box.pack(

            side="left",

            padx=7

        )

        # Visibility

        self.visibility_box = self.create_stat(

            stats,

            "◉",

            "VISIBILITY",

            "-- km",

            self.GREEN

        )

        self.visibility_box.pack(

            side="left",

            padx=7

        )

        # ====================================================

        # UNIT SELECTOR

        # ====================================================

        unit_row = tk.Frame(

            self.content,

            bg=self.BG

        )

        unit_row.pack(

            fill="x",

            pady=(22, 15)

        )

        tk.Label(

            unit_row,

            text="Temperature unit",

            font=("Segoe UI", 10),

            bg=self.BG,

            fg=self.MUTED

        ).pack(

            side="left"

        )

        unit_buttons = tk.Frame(

            unit_row,

            bg=self.BG

        )

        unit_buttons.pack(

            side="right"

        )

        self.celsius_button = RoundedButton(

            unit_buttons,

            text="°C",

            command=lambda: self.change_unit("C"),

            width=62,

            height=38,

            radius=19,

            bg=self.GOLD,

            fg="#17120A",

            hover_bg=self.GOLD_LIGHT

        )

        self.celsius_button.pack(

            side="left",

            padx=3

        )

        self.fahrenheit_button = RoundedButton(

            unit_buttons,

            text="°F",

            command=lambda: self.change_unit("F"),

            width=62,

            height=38,

            radius=19,

            bg="#181C22",

            fg=self.MUTED,

            hover_bg="#272D35"

        )

        self.fahrenheit_button.pack(

            side="left",

            padx=3

        )

        # ====================================================

        # FORECAST HEADER

        # ====================================================

        forecast_header = tk.Frame(

            self.content,

            bg=self.BG

        )

        forecast_header.pack(

            fill="x",

            pady=(18, 10)

        )

        tk.Label(

            forecast_header,

            text="Forecast",

            font=("Segoe UI", 22, "bold"),

            bg=self.BG,

            fg=self.WHITE

        ).pack(

            side="left"

        )

        tk.Label(

            forecast_header,

            text="Hourly & 5-day forecast",

            font=("Segoe UI", 10),

            bg=self.BG,

            fg=self.MUTED

        ).pack(

            side="left",

            padx=15,

            pady=(7, 0)

        )

        # ====================================================

        # ====================================================
        # FORECAST CARD
        # ====================================================

        forecast_widget = RoundedCard(
            self.content,
            width=900,
            height=650,
            bg=self.CARD,
            border=self.BORDER,
            radius=26
        )

        forecast_widget.pack(
            fill="x",
            pady=(0, 40)
        )

        self.forecast_content = forecast_widget.inner

        tk.Label(
            self.forecast_content,
            text="◷  Forecast",
            font=("Segoe UI", 18, "bold"),
            bg=self.CARD,
            fg=self.WHITE
        ).pack(anchor="w", padx=28, pady=(24, 2))

        tk.Label(
            self.forecast_content,
            text="Next 6 hours",
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(anchor="w", padx=28, pady=(0, 12))

        hourly_wrap = tk.Frame(self.forecast_content, bg=self.CARD)
        hourly_wrap.pack(fill="x", padx=28)

        self.hourly_canvas = tk.Canvas(
            hourly_wrap, height=145, bg=self.CARD,
            highlightthickness=0, bd=0
        )
        self.hourly_canvas.pack(fill="x", expand=True)

        self.hourly_scrollbar = tk.Scrollbar(
            hourly_wrap, orient="horizontal",
            command=self.hourly_canvas.xview,
            troughcolor="#0D1014", bg="#3A414B",
            activebackground=self.GOLD
        )
        self.hourly_scrollbar.pack(fill="x", pady=(8, 0))
        self.hourly_canvas.configure(
            xscrollcommand=self.hourly_scrollbar.set
        )

        self.hourly_frame = tk.Frame(
            self.hourly_canvas, bg=self.CARD
        )
        self.hourly_canvas.create_window(
            (0, 0), window=self.hourly_frame, anchor="nw"
        )
        self.hourly_frame.bind(
            "<Configure>",
            lambda e: self.hourly_canvas.configure(
                scrollregion=self.hourly_canvas.bbox("all")
            )
        )

        tk.Label(
            self.forecast_content,
            text="5-Day Forecast",
            font=("Segoe UI", 13, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w", padx=28, pady=(24, 10))

        daily_wrap = tk.Frame(self.forecast_content, bg=self.CARD)
        daily_wrap.pack(fill="x", padx=28)

        self.daily_canvas = tk.Canvas(
            daily_wrap, height=175, bg=self.CARD,
            highlightthickness=0, bd=0
        )
        self.daily_canvas.pack(fill="x", expand=True)

        self.daily_scrollbar = tk.Scrollbar(
            daily_wrap, orient="horizontal",
            command=self.daily_canvas.xview,
            troughcolor="#0D1014", bg="#3A414B",
            activebackground=self.GOLD
        )
        self.daily_scrollbar.pack(fill="x", pady=(8, 0))
        self.daily_canvas.configure(
            xscrollcommand=self.daily_scrollbar.set
        )

        self.daily_frame = tk.Frame(
            self.daily_canvas, bg=self.CARD
        )
        self.daily_canvas.create_window(
            (0, 0), window=self.daily_frame, anchor="nw"
        )
        self.daily_frame.bind(
            "<Configure>",
            lambda e: self.daily_canvas.configure(
                scrollregion=self.daily_canvas.bbox("all")
            )
        )

        self.hourly_canvas.bind(
            "<MouseWheel>",
            lambda e: self.hourly_canvas.xview_scroll(
                int(-e.delta / 120), "units"
            )
        )
        self.hourly_canvas.bind(
            "<Shift-MouseWheel>",
            lambda e: self.hourly_canvas.xview_scroll(
                int(-e.delta / 120), "units"
            )
        )
        self.daily_canvas.bind(
            "<MouseWheel>",
            lambda e: self.daily_canvas.xview_scroll(
                int(-e.delta / 120), "units"
            )
        )
        self.daily_canvas.bind(
            "<Shift-MouseWheel>",
            lambda e: self.daily_canvas.xview_scroll(
                int(-e.delta / 120), "units"
            )
        )

        self.show_forecast_placeholder()



    # GET WEATHER

    # ========================================================

    def get_weather(self):

        city = self.search_entry.get()

        if not city:

            self.show_error(

                "Please enter a city name."

            )

            return

        self.error_label.config(

            text=""

        )

        self.search_button.normal_bg = "#D99F35"

        self.search_button.draw_button()

        self.root.update_idletasks()

        try:

            weather = self.weather_service.get_weather(

                city

            )

            self.current_weather = weather

            # City

            self.city_label.config(

                text=f"{weather['city']}, {weather['country']}"

            )

            # Status

            self.location_status.config(

                text="⌖  Current weather"

            )

            # Condition

            self.condition_label.config(

                text=weather["condition"].title()

            )

            # Humidity

            self.humidity_box.value_label.config(

                text=f"{weather['humidity']}%"

            )

            # Wind

            self.wind_box.value_label.config(

                text=f"{weather['wind_speed']} m/s"

            )

            # Pressure

            if "pressure" in weather:

                self.pressure_box.value_label.config(

                    text=f"{weather['pressure']} hPa"

                )

            # Visibility

            if "visibility" in weather:

                self.visibility_box.value_label.config(

                    text=f"{weather['visibility']} km"

                )

            # Temperature

            self.update_temperature()

            # Icon

            if "icon" in weather:

                self.load_icon(

                    weather["icon"]

                )

            forecast = self.weather_service.get_forecast(city)
            self.forecast_data = forecast
            self.update_forecast(forecast)

        except ValueError as error:

            self.show_error(

                str(error)

            )

        except ConnectionError as error:

            self.show_error(

                str(error)

            )

        except requests.exceptions.RequestException:

            self.show_error(

                "Unable to connect to the weather service."

            )

        except Exception as error:

            print(error)

            self.show_error(

                "Something went wrong. Please try again."

            )

        finally:

            self.search_button.normal_bg = self.GOLD

            self.search_button.draw_button()

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat(self, parent, icon, title, value, color):
        card = RoundedCard(
            parent,
            width=190,
            height=105,
            bg=self.CARD_LIGHT,
            border=self.BORDER,
            radius=20
        )

        content = card.inner

        tk.Label(
            content,
            text=f"{icon}  {title}",
            font=("Segoe UI", 8, "bold"),
            bg=self.CARD_LIGHT,
            fg=self.MUTED
        ).pack(anchor="w", padx=16, pady=(14, 3))

        value_label = tk.Label(
            content,
            text=value,
            font=("Segoe UI", 15, "bold"),
            bg=self.CARD_LIGHT,
            fg=color
        )
        value_label.pack(anchor="w", padx=16, pady=(0, 10))

        card.value_label = value_label
        return card

    # ========================================================

    # UNIT

    # ========================================================

    def change_unit(self, unit):

        self.unit = unit

        if unit == "C":

            self.celsius_button.normal_bg = self.GOLD

            self.celsius_button.fg = "#17120A"

            self.celsius_button.hover_bg = self.GOLD_LIGHT

            self.fahrenheit_button.normal_bg = "#181C22"

            self.fahrenheit_button.fg = self.MUTED

            self.fahrenheit_button.hover_bg = "#272D35"

        else:

            self.fahrenheit_button.normal_bg = self.GOLD

            self.fahrenheit_button.fg = "#17120A"

            self.fahrenheit_button.hover_bg = self.GOLD_LIGHT

            self.celsius_button.normal_bg = "#181C22"

            self.celsius_button.fg = self.MUTED

            self.celsius_button.hover_bg = "#272D35"

        self.celsius_button.draw_button()

        self.fahrenheit_button.draw_button()

        if self.current_weather:

            self.update_temperature()

            if self.forecast_data:
                self.update_forecast(self.forecast_data)

    # ========================================================

    # TEMPERATURE

    # ========================================================

    def update_temperature(self):

        if not self.current_weather:

            return

        temperature = self.current_weather["temperature"]

        feels_like = self.current_weather["feels_like"]

        if self.unit == "F":

            temperature = (

                temperature * 9 / 5

            ) + 32

            feels_like = (

                feels_like * 9 / 5

            ) + 32

        self.temperature_label.config(

            text=f"{temperature:.1f}°"

        )

        self.feels_like_label.config(

            text=f"Feels like {feels_like:.1f}°"

        )

    # ========================================================

    # WEATHER ICON

    # ========================================================

    def load_icon(self, icon_code):

        try:

            url = (

                "https://openweathermap.org/img/wn/"

                f"{icon_code}@2x.png"

            )

            response = requests.get(

                url,

                timeout=10

            )

            response.raise_for_status()

            image = Image.open(

                BytesIO(response.content)

            )

            image = image.resize(

                (120, 120),

                Image.Resampling.LANCZOS

            )

            self.weather_icon = ImageTk.PhotoImage(

                image

            )

            self.icon_label.config(

                image=self.weather_icon,

                text=""

            )

        except Exception:

            self.icon_label.config(

                image="",

                text="☁"

            )

    # ========================================================

    # ERROR

    # ========================================================

    # ========================================================
    # FORECAST
    # ========================================================

    def show_forecast_placeholder(self):
        for frame in (self.hourly_frame, self.daily_frame):
            for widget in frame.winfo_children():
                widget.destroy()

        tk.Label(
            self.hourly_frame,
            text="Search for a city to load the forecast",
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(padx=20, pady=48)

        tk.Label(
            self.daily_frame,
            text="5-day forecast will appear here",
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(padx=20, pady=62)

    def update_forecast(self, forecast):
        for frame in (self.hourly_frame, self.daily_frame):
            for widget in frame.winfo_children():
                widget.destroy()

        if not forecast:
            self.show_forecast_placeholder()
            return

        # OpenWeather's free forecast endpoint provides 3-hour intervals.
        # The first two entries represent roughly the next 6 hours.
        for item in forecast[:6]:
            self.create_hourly_card(self.hourly_frame, item)

        daily = {}
        for item in forecast:
            date_text = item.get("dt_txt", "").split(" ")[0]
            if date_text and date_text not in daily:
                daily[date_text] = item

        for item in list(daily.values())[:5]:
            self.create_daily_card(self.daily_frame, item)

        self.hourly_frame.update_idletasks()
        self.daily_frame.update_idletasks()
        self.hourly_canvas.configure(
            scrollregion=self.hourly_canvas.bbox("all")
        )
        self.daily_canvas.configure(
            scrollregion=self.daily_canvas.bbox("all")
        )

    def create_forecast_card(self, parent, width, height):
        card = RoundedCard(
            parent,
            width=width,
            height=height,
            bg=self.CARD_LIGHT,
            border=self.BORDER,
            radius=20
        )
        card.pack(side="left", padx=6, pady=5)
        return card

    def create_hourly_card(self, parent, item):
        card = self.create_forecast_card(parent, 185, 125)
        content = card.inner

        dt = datetime.strptime(
            item["dt_txt"], "%Y-%m-%d %H:%M:%S"
        )
        temp = item["main"]["temp"]
        if self.unit == "F":
            temp = temp * 9 / 5 + 32

        tk.Label(
            content,
            text=dt.strftime("%I:%M %p").lstrip("0"),
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_LIGHT,
            fg=self.WHITE
        ).pack(pady=(14, 3))

        tk.Label(
            content,
            text=f"{temp:.1f}°",
            font=("Segoe UI", 24, "bold"),
            bg=self.CARD_LIGHT,
            fg=self.GOLD
        ).pack()

        tk.Label(
            content,
            text=item["weather"][0]["description"].title(),
            font=("Segoe UI", 9),
            bg=self.CARD_LIGHT,
            fg=self.MUTED
        ).pack(pady=(2, 0))

    def create_daily_card(self, parent, item):
        card = self.create_forecast_card(parent, 155, 155)
        content = card.inner

        dt = datetime.strptime(
            item["dt_txt"], "%Y-%m-%d %H:%M:%S"
        )
        temp = item["main"]["temp"]
        feels = item["main"]["feels_like"]

        if self.unit == "F":
            temp = temp * 9 / 5 + 32
            feels = feels * 9 / 5 + 32

        tk.Label(
            content,
            text=dt.strftime("%a, %d %b"),
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_LIGHT,
            fg=self.WHITE
        ).pack(pady=(15, 5))

        tk.Label(
            content,
            text=f"{temp:.1f}°",
            font=("Segoe UI", 25, "bold"),
            bg=self.CARD_LIGHT,
            fg=self.GOLD
        ).pack()

        tk.Label(
            content,
            text=item["weather"][0]["description"].title(),
            font=("Segoe UI", 8),
            bg=self.CARD_LIGHT,
            fg=self.MUTED,
            wraplength=130
        ).pack(pady=(2, 2))

        tk.Label(
            content,
            text=f"Feels {feels:.1f}°",
            font=("Segoe UI", 8),
            bg=self.CARD_LIGHT,
            fg=self.MUTED
        ).pack()

    # ========================================================
    # ERROR
    # ========================================================

    def show_error(self, message):

        self.error_label.config(

            text=message

        )

# ============================================================

# RUN APPLICATION

# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WeatherApp(root)

    root.mainloop()
