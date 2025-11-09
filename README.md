# AI Guard: An Intelligent Room Monitoring System

An intelligent, voice-activated security agent that uses facial recognition and a Large Language Model (LLM) to monitor a room, identify individuals, and interact with potential intruders.

**Authors:**
* **Harsh Anand** (22B1249)
* **Medhansh Sharma** (22B1287)

---

## About The Project

AI Guard is a Python-based application that turns your computer's webcam and microphone into an autonomous monitoring system. The system remains idle until activated by a voice command. Once in "Guard Mode," it uses real-time facial recognition to distinguish between pre-enrolled, trusted users and unknown individuals.

When an unknown person is detected, the system's core AI agent, powered by the fast **Groq Llama 3.1 LLM**, initiates a conversation. The agent's response strategy dynamically escalates from a polite greeting to a firm warning if the individual remains in the area without authorization. The system can be deactivated at any time by a trusted user with a simple voice command.

### Key Features

* **Facial Recognition**: Enrolls and recognizes known users, and identifies unknown individuals.
* **Voice Activation**: Hands-free activation and deactivation using voice commands ("activate guard", "stop").
* **LLM-Powered Agent**: Utilizes the Groq API for real-time, intelligent, and context-aware responses.
* **Dynamic Escalation Protocol**: The agent's tone becomes progressively firmer if an intruder persists, from a friendly query to a final warning.
* **Real-time Audio Feedback**: Integrated Text-to-Speech (TTS) and Automatic Speech Recognition (ASR) for a complete interactive experience.
* **Offline Keyword Spotting**: Uses Vosk for efficient, low-latency detection of critical keywords like "stop".

---

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.10+
* A webcam connected to your computer
* A microphone connected to your computer

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone 
    cd your-repository-name
    ```

2.  **Create and Activate a Virtual Environment**
    This keeps the project's dependencies isolated.

    *On Windows (PowerShell):*
    ```powershell
    # The command you provided uses python 3.11, adjust if your version differs
    py -3.11 -m venv myvenv
    myvenv\Scripts\activate
    ```
    *On macOS/Linux:*
    ```bash
    python3 -m venv myvenv
    source myvenv/bin/activate
    ```

3.  **Install Dependencies**
    A `requirements.txt` file is included to install all necessary packages at once.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Your Groq API Key**
    The AI agent requires an API key from Groq to function.
    * Visit the [Groq Console](https://console.groq.com/) to create an account and get your free API key.
    * Set the API key as an environment variable in your terminal. **You must do this every time you open a new terminal session.**

    *On Windows (PowerShell):*
    ```powershell
    $env:GROQ_API_KEY="your_api_key_here"
    ```
    *On macOS/Linux:*
    ```bash
    export GROQ_API_KEY="your_api_key_here"
    ```

5.  **Enroll Trusted Faces**
    For the system to recognize you, you must add your pictures.
    * Navigate to the `data/faces/` directory.
    * Create a new folder with your name (e.g., `data/faces/Harsh/`).
    * Place several clear photos of your face inside this folder. The more images you add, the better the recognition accuracy.

---

## Usage

Once the setup is complete, you can run the application.

1.  Ensure your virtual environment is activated and the `GROQ_API_KEY` is set.
2.  Run the main script from the root directory of the project:
    ```bash
    python main.py
    ```
3.  The application will initialize. You will hear "AI Guard is online. Say 'activate guard' to begin."
4.  Say **"activate guard"** to put the system into monitoring mode.
5.  If you are a known user, you can say **"stop"** at any time to deactivate guard mode.
6.  Press `q` in the camera window to quit the application.

---
---

## Technologies Used

* **Python 3**
* **Groq API**: For fast LLM (Llama 3.1) inference.
* **OpenCV**: For camera access and image processing.
* **face_recognition**: For detecting and identifying faces.
* **Vosk**: For offline, real-time keyword spotting.
* **SpeechRecognition**: For general command recognition.
* **pyttsx3**: For text-to-speech output.
* **Sounddevice**: For audio input streaming.


## Project Structure

Here is an overview of the project's file structure and the role of each component.  
AI-Guard/<br>
├── data/<br>
│&nbsp;&nbsp;&nbsp;└── faces/<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── YourName/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Folder for enrolling trusted user images<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── image1.jpg<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>
├── myvenv/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Virtual environment folder<br>
├── agent.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# The AI brain: manages state, logic, and LLM calls via Groq.<br>
├── asr.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Handles general-purpose Automatic Speech Recognition for commands.<br>
├── keyword_spotter.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Uses Vosk for offline, real-time keyword detection (e.g., "stop").<br>
├── main.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# The main application entry point that integrates all modules.<br>
├── requirements.txt &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# A list of all Python dependencies for easy installation.<br>
├── tts.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# A simple script for Text-to-Speech synthesis.<br>
└── vision.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Manages the camera feed and facial recognition logic.<br>

