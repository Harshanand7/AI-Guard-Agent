
from groq import Groq
import time
import os

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set!")

class AIAgent:
    """Manages system state and LLM interaction using Groq."""
    def __init__(self, api_key=API_KEY):
        self.client = Groq(api_key=api_key)
        
        self.guard_mode = False
        self.intruder_detected = False
        self.last_detection_time = 0
        self.escalation_level = 0
        print(" AI Agent initialized (using Groq).")
        
    def _get_llm_response(self, prompt):
        """Private method to get a response from the Groq LLM."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "I am having some trouble thinking right now."

    def process_detection(self, detected_names, intruder_spoken=False):
            """
            detected_names: list of names returned by FaceRecognizer (Unknown/known)
            intruder_spoken: boolean flag, True if ASR detected speech from intruder
            """
            is_unknown_present = "Unknown" in detected_names
            is_known_present = any(name != "Unknown" for name in detected_names)
            response_text = None

            # Trusted user detected
            if is_known_present:
                trusted_name = [name for name in detected_names if name != "Unknown"][0]
                response_text = f"Welcome back, {trusted_name}. Activating guard mode."
                self.guard_mode = True
                self.intruder_detected = False
                self.escalation_level = 0
                return response_text

            # Unknown intruder detected
            if is_unknown_present:
                # First detection
                if not self.intruder_detected:
                    self.intruder_detected = True
                    self.last_detection_time = time.time()
                    self.escalation_level = 1
                    prompt = (
                        "You are a friendly but firm AI room guard. "
                        "An unrecognized person has entered. Politely greet them and ask for their identity in a concise way. Keep it limited to 20 words."
                    )
                    response_text = self._get_llm_response(prompt)

                # Intruder already detected → escalate if silent or ignored
                elif self.intruder_detected:
                    # If intruder spoke, reset the timer but do not escalate yet
                    if intruder_spoken:
                        self.last_detection_time = time.time()
                    # Escalate if 15s passed without compliance
                    elif time.time() - self.last_detection_time > 15:
                        self.escalation_level += 1
                        self.last_detection_time = time.time()
                        if self.escalation_level == 2:
                            prompt = (
                                "As an AI room guard, the unrecognized person is still present. "
                                "Your tone is now more firm. State this is a private area and ask them to leave if unauthorized. Keep it limited to 20 words."
                            )
                            response_text = self._get_llm_response(prompt)
                        elif self.escalation_level >= 3:
                            prompt = (
                                "As an AI room guard, the intruder has ignored previous warnings. "
                                "Issue a final, stern warning. State that the owner is being notified and they must leave immediately. Keep it limited to 20 words." 
                            )
                            response_text = self._get_llm_response(prompt)

            # Unknown intruder has left
            # elif not is_unknown_present and self.intruder_detected:
            #     print("Intruder appears to have left. Resetting state.")
            #     self.intruder_detected = False
            #     self.escalation_level = 0

            return response_text

# --- Standalone Test ---
if __name__ == "__main__":
    print("Testing the AI agent (with Groq)...")
    agent = AIAgent()
    agent.guard_mode = True
    
    print("\n--- Test Case 1: Intruder Appears ---")
    names = ["Unknown"]
    response = agent.process_detection(names)
    print(f"AI Response: {response}")
    
    print("\n--- Test Case 2: Trusted User appears ---")
    names = ["harsh"]
    response = agent.process_detection(names)
    print(f"AI Response: {response}")
    print(f"Guard Mode is now: {agent.guard_mode}")