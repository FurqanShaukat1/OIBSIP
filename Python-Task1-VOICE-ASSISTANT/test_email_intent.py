from assistant.intents import IntentEngine


engine = IntentEngine()


tests = [
    "send an email to test at the rate example.com saying hello from my voice assistant",
    "send an email to john dot smith at gmail dot com saying hello",
    "send an email to test@example.com with subject meeting saying the meeting is at 5 pm",
]


for command in tests:

    intent = engine.detect(command)

    print(f"\nCommand: {command}")
    print(f"Intent: {intent.name}")
    print(f"Value: {intent.value}")