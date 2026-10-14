from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Intent:
    name: str
    value: Optional[object] = None


class IntentEngine:

    def detect(self, text: str) -> Intent:
        text = text.lower().strip()

        # Greetings
        if text in [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]:
            return Intent("greeting")

        # Time
        if any(phrase in text for phrase in [
            "what time is it",
            "current time",
            "tell me the time",
            "time right now"
        ]):
            return Intent("time")

        # Date
        if any(phrase in text for phrase in [
            "what is today's date",
            "what's today's date",
            "today's date",
            "what date is it",
            "tell me the date"
        ]):
            return Intent("date")

        # Weather
        if any(word in text for word in [
            "weather",
            "temperature",
            "forecast"
        ]):
            city = self.extract_city(text)
            return Intent("weather", city)

        # Email
        if any(phrase in text for phrase in [
            "send an email",
            "send email",
            "send a mail",
            "send mail",
            "write an email",
            "write email",
            "email someone",
            "email my"
        ]):
            email_data = self.extract_email(text)
            return Intent("email", email_data)

        # Web search
        if any(phrase in text for phrase in [
            "search for",
            "search the web",
            "google",
            "look up"
        ]):
            return Intent("search", text)

        # Reminder
        if "remind me" in text:
            reminder_data = self.extract_reminder(text)
            return Intent("reminder", reminder_data)

        # Exit
        if any(phrase in text for phrase in [
            "goodbye",
            "bye",
            "exit",
            "quit",
            "stop"
        ]):
            return Intent("exit")

        # Unknown command
        return Intent("unknown", text)

    def extract_city(self, text: str):
        weather_phrases = [
            "what is the weather in",
            "what's the weather in",
            "what is the weather like in",
            "what's the weather like in",
            "weather in",
            "weather of",
            "temperature in",
            "temperature of",
            "forecast for",
            "weather for"
        ]

        for phrase in weather_phrases:
            if phrase in text:
                city = text.split(phrase, 1)[1].strip()

                if city:
                    return city

        return None

    def extract_reminder(self, text: str):
        pattern = (
            r"remind me in "
            r"(\d+)\s*"
            r"(second|seconds|minute|minutes|hour|hours)"
            r"\s+to\s+(.+)"
        )

        match = re.search(pattern, text)

        if not match:
            return None

        amount = int(match.group(1))
        unit = match.group(2)
        message = match.group(3).strip()

        if "second" in unit:
            seconds = amount
        elif "minute" in unit:
            seconds = amount * 60
        elif "hour" in unit:
            seconds = amount * 3600
        else:
            return None

        return {
            "seconds": seconds,
            "message": message
        }

    def extract_email(self, text: str):
        text = text.lower().strip()

        prefixes = [
            "send an email to ",
            "send a email to ",
            "send email to ",
            "send a mail to ",
            "send mail to "
        ]

        remaining = None

        for prefix in prefixes:
            if text.startswith(prefix):
                remaining = text[len(prefix):].strip()
                break

        if not remaining:
            return None

        # Find where the message starts.
        message_match = re.search(
            r"\s+(saying|that says|with message|with subject)\s+",
            remaining
        )

        if not message_match:
            return None

        email_part = remaining[:message_match.start()].strip()
        remainder = remaining[message_match.start():].strip()

        # Convert spoken email address into normal format.
        email_part = email_part.replace(
            " at the rate ",
            "@"
        )
        email_part = email_part.replace(
            " at rate ",
            "@"
        )
        email_part = email_part.replace(
            " at ",
            "@"
        )
        email_part = email_part.replace(
            " dot ",
            "."
        )
        email_part = email_part.replace(
            " underscore ",
            "_"
        )
        email_part = email_part.replace(
            " hyphen ",
            "-"
        )

        # Find the email address.
        email_match = re.fullmatch(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            email_part
        )

        if not email_match:
            return None

        recipient = email_match.group(0)

        subject = "Voice Assistant Message"
        body = None

        # Custom subject + body
        subject_match = re.match(
            r"with subject (.+?)\s+saying (.+)",
            remainder
        )

        if subject_match:
            subject = subject_match.group(1).strip()
            body = subject_match.group(2).strip()

        else:
            # Body only
            body_match = re.match(
                r"(?:saying|that says|with message)\s+(.+)",
                remainder
            )

            if body_match:
                body = body_match.group(1).strip()

        if not body:
            return None

        return {
            "recipient": recipient,
            "subject": subject,
            "body": body
        }