# tts.py
import pyttsx3
import sys

def main():
    text = " ".join(sys.argv[1:])  # take all args as text
    engine = pyttsx3.init()
    print(f"AI GUARD: {text}")
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    main()
