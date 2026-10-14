import pyttsx3

engine = pyttsx3.init()

engine.say("Hello! This is a voice test.")
engine.runAndWait()

print("Voice test completed.")