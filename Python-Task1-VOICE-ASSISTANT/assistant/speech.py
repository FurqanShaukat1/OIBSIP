import speech_recognition as sr
import pyttsx3
import time
import threading


class SpeechEngine:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speak_lock = threading.Lock()

    def speak(self, text: str):
        with self.speak_lock:
            print(f"Assistant: {text}")

            time.sleep(0.5)

            engine = pyttsx3.init()
            engine.setProperty("rate", 150)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = self.recognizer.listen(source)

        print("Processing...")

        try:
            text = self.recognizer.recognize_google(audio)

            print(f"You said: {text}")

            return text.lower()

        except sr.UnknownValueError:
            self.speak(
                "Sorry, I couldn't understand you. "
                "Please try again."
            )
            return None

        except sr.RequestError:
            self.speak(
                "I'm having trouble connecting to "
                "the speech recognition service."
            )
            return None