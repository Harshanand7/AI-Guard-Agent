import cv2
import time
import subprocess
import sys
from vision import FaceRecognizer
from agent import AIAgent
import asr
import keyword_spotter   # <-- new import

def speak(text):
    # Launch tts.py as a separate process asynchronously
    subprocess.Popen([sys.executable, "tts.py", text])

def main():
    # Initialize components
    face_recognizer = FaceRecognizer(face_dir='data/faces')
    agent = AIAgent()
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return

    # Startup message
    speak("AI Guard is online. Say 'activate guard' to begin.")
    time.sleep(3)

    last_speech_time = 0
    speech_cooldown = 5  # seconds between TTS messages

    while True:
        current_time = time.time()

        # -------------------- Keyword Spotting / Command Mode --------------------
        if not agent.guard_mode:


            command = asr.listen_for_command()
            if command and "activate guard" in command:
                agent.guard_mode = True
                speak("Guard mode activated. I am now monitoring the room.")
                time.sleep(5)
            continue

        # -------------------- Guard Mode Active --------------------
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        detected_name = face_recognizer.recognize_faces(frame)
        response = agent.process_detection(detected_name)

        if response and (current_time - last_speech_time) > speech_cooldown:
            print(f"Speaking: {response}")
            speak(response)
            last_speech_time = current_time

        cv2.imshow('AI Guard Cam', frame)

        # Allow emergency keyword stop (real-time)
        emergency_keyword = keyword_spotter.listen_for_keyword(
            keywords=["stop"], timeout=8
        )
        if emergency_keyword in ["stop"] and detected_name[0] != "Unknown":
            speak("Deactivating guard mode. Standing down.")
            agent.guard_mode = False
            time.sleep(3)
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    # -------------------- Shutdown --------------------
    video_capture.release()
    cv2.destroyAllWindows()
    speak("AI Guard is shutting down. Goodbye!")
    time.sleep(3)
    print("AI Guard has shut down.")

if __name__ == "__main__":
    main()
