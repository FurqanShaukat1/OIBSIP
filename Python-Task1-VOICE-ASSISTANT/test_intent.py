from assistant.intents import IntentEngine


engine = IntentEngine()

tests = [
    "remind me in 10 seconds to check my email",
    "remind me in 2 minutes to drink water",
    "remind me in 1 hour to call my friend"
]

for text in tests:
    intent = engine.detect(text)

    print(f"\nCommand: {text}")
    print(f"Intent: {intent.name}")
    print(f"Value: {intent.value}")


email_commands = [
    "send an email",
    "send an email to my friend",
    "send a mail",
    "write an email",
    "email my friend"
]

for command in email_commands:
    intent = engine.detect(command)

    print(f"\nCommand: {command}")
    print(f"Intent: {intent.name}")
    print(f"Value: {intent.value}")

email_detail_tests = [
    "send an email to test@example.com saying hello from my voice assistant",
    "send an email to test@example.com with subject meeting saying the meeting is at 5 pm",
    "send a mail to test@example.com saying this is a test"
]

for command in email_detail_tests:
    intent = engine.detect(command)

    print(f"\nCommand: {command}")
    print(f"Intent: {intent.name}")
    print(f"Value: {intent.value}")   