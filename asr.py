import speech_recognition as sr
recognizer=sr.Recognizer()
microphone=sr.Microphone()
with microphone as source:
    print("Callibrating microphone... PLease be quiet for a moment")
    recognizer.adjust_for_ambient_noise(source,duration=1)
    print("Microphone calibrated")
def listen_for_command():
    try: 
        with microphone as source:
            print("Listening for command...")
            audio=recognizer.listen(source,timeout=5, phrase_time_limit=4)
        text=recognizer.recognize_google(audio).lower()
        print(f"Recognized command: {text}")
        return text
    except (sr.UnknownValueError,sr.WaitTimeoutError):
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        