import threading
import time


class ReminderService:

    def __init__(self, speech_engine):
        self.speech = speech_engine

    def set_reminder(self, seconds: int, message: str):
        timer = threading.Timer(
            seconds,
            self._trigger_reminder,
            args=[message]
        )

        timer.daemon = False
        timer.start()

        return (
            f"Okay. I will remind you in "
            f"{seconds} seconds to {message}."
        )

    def _trigger_reminder(self, message: str):
        self.speech.speak(
            f"Reminder. {message}"
        )