import time

from assistant.speech import SpeechEngine
from assistant.reminders import ReminderService


speech = SpeechEngine()
reminders = ReminderService(speech)

print(
    reminders.set_reminder(
        10,
        "check your email"
    )
)

time.sleep(15)