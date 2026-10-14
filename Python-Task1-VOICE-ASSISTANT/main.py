from assistant.speech import SpeechEngine
from assistant.intents import IntentEngine
from assistant.commands import CommandHandler
from assistant.weather import WeatherService
from assistant.reminders import ReminderService
from assistant.email_service import EmailService


def main():
    speech = SpeechEngine()
    intent_engine = IntentEngine()
    commands = CommandHandler()
    weather = WeatherService()
    reminders = ReminderService(speech)
    email_service = EmailService()

    speech.speak("Hello! Voice assistant is starting.")

    while True:
        command = speech.listen()

        if not command:
            continue

        intent = intent_engine.detect(command)

        print(f"Detected intent: {intent.name}")

        if intent.name == "greeting":
            speech.speak(commands.greeting())

        elif intent.name == "time":
            speech.speak(commands.get_time())

        elif intent.name == "date":
            speech.speak(commands.get_date())

        elif intent.name == "search":
            speech.speak(commands.search_web(intent.value))

        elif intent.name == "weather":
            if intent.value:
                print(f"Weather city: {intent.value}")

                result = weather.get_weather(intent.value)

                speech.speak(result)

            else:
                speech.speak(
                    "Please tell me the city you want the weather for."
                )

        elif intent.name == "reminder":
            if intent.value:
                result = reminders.set_reminder(
                    intent.value["seconds"],
                    intent.value["message"]
                )

                speech.speak(result)

            else:
                speech.speak(
                    "I couldn't understand the reminder. "
                    "Try saying, remind me in 10 seconds "
                    "to check my email."
                )

        elif intent.name == "email":
            if intent.value:
                result = email_service.send_email(
                    intent.value["recipient"],
                    intent.value["subject"],
                    intent.value["body"]
                )

                speech.speak(result)

            else:
                speech.speak(
                    "I couldn't understand the email command. "
                    "Try saying, send an email to "
                    "test@example.com saying hello."
                )

        elif intent.name == "exit":
            speech.speak("Goodbye!")
            break

        else:
            speech.speak(
                "Sorry, I don't understand that command yet."
            )


if __name__ == "__main__":
    main()