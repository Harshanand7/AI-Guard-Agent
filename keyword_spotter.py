import os
import json
import queue
import time
import zipfile
import urllib.request
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ---------------------------------------------------------------------
#                 🔹 MODEL DOWNLOAD + SETUP
# ---------------------------------------------------------------------
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_ZIP = "vosk-model-small-en-us-0.15.zip"
MODEL_DIR = "vosk-model-small-en-us-0.15"

def ensure_model():
    """Downloads and extracts the Vosk model if not already available."""
    if os.path.exists(MODEL_DIR):
        return

    print("[KeywordSpotter] Downloading Vosk model (about 50 MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_ZIP)

    print("[KeywordSpotter] Extracting model files...")
    with zipfile.ZipFile(MODEL_ZIP, "r") as zip_ref:
        zip_ref.extractall(".")
    os.remove(MODEL_ZIP)
    print("[KeywordSpotter] Model ready!")

# Ensure model exists before using
ensure_model()

# Load the model safely
try:
    model = Model(MODEL_DIR)
except Exception as e:
    print("❌ Error loading Vosk model:", e)
    print(f"Make sure the extracted folder is named exactly '{MODEL_DIR}'")
    raise SystemExit

# ---------------------------------------------------------------------
#                 🔹 KEYWORD LISTENER
# ---------------------------------------------------------------------
def listen_for_keyword(keywords=None, timeout=5):
    """
    Listens for one of the specified keywords for up to `timeout` seconds.
    Returns the detected keyword (string) or None if nothing detected.
    """

    if keywords is None:
        keywords = ["stop"]

    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        q.put(bytes(indata))

    print(f"[KeywordSpotter] Listening for: {', '.join(keywords)} (timeout={timeout}s)")

    with sd.RawInputStream(
        samplerate=16000, blocksize=8000, dtype='int16',
        channels=1, callback=callback
    ):
        recognizer = KaldiRecognizer(model, 16000)
        start_time = time.time()

        while time.time() - start_time < timeout:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()
                if text:
                    print(f"[KeywordSpotter] Heard: {text}")

                for word in keywords:
                    if word in text:
                        print(f"[KeywordSpotter] Detected keyword: {word}")
                        return word
        return None


# ---------------------------------------------------------------------
#                 🔹 TEST MODE (run standalone)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("[KeywordSpotter] Starting microphone calibration...")
    print("Please be quiet for 2 seconds...")
    sd.sleep(2000)
    print("Microphone calibrated \n")

    while True:
        keyword = listen_for_keyword(keywords=["stop"], timeout=8)
        if keyword:
            print(f"[MAIN] Triggered keyword: {keyword}")
        else:
            print("[MAIN] No keyword detected.")
