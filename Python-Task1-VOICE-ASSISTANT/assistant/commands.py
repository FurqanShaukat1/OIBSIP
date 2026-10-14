from datetime import datetime
import webbrowser
from urllib.parse import quote_plus


class CommandHandler:

    def get_time(self):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    def get_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."

    def search_web(self, query):
        search_url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        webbrowser.open(search_url)

        return f"I've opened {query}."

    def greeting(self):
        return "Hello! How are you? How can I help you?"