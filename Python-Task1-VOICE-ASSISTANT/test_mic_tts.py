import speech_recognition as sr
import pyttsx3
import time

recognizer = sr.Recognizer()

print("Starting microphone...")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)

    print("Say hello...")
    audio = recognizer.listen(source)

print("Microphone released.")

# Give Windows audio a moment to release the device
time.sleep(1)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

except Exception as e:
    print("Recognition error:", e)
    text = ""

print("Starting TTS...")

engine = pyttsx3.init()
engine.setProperty("rate", 150)

engine.say("Hello!")
engine.runAndWait()

engine.say("How are you? How can I help you?")
engine.runAndWait()

engine.stop()

print("Finished.")