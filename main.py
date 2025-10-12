"""
SoundToAct - Voice-triggered automation app
"""
import speech_recognition as sr
import time
from typing import Callable, Dict


class VoiceListener:
    """Listens to audio and triggers actions based on detected keywords"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.keyword_actions: Dict[str, Callable] = {}

        # Adjust for ambient noise
        print("Calibrating for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Calibration complete!")

    def register_action(self, keyword: str, action: Callable):
        """Register an action to be triggered when a keyword is detected"""
        self.keyword_actions[keyword.lower()] = action
        print(f"Registered action for keyword: '{keyword}'")

    def listen_once(self) -> str:
        """Listen for a single phrase and return the recognized text"""
        with self.microphone as source:
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            # Using Google Speech Recognition (free)
            text = self.recognizer.recognize_google(audio, language="ko-KR")
            print(f"Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return ""

    def check_keywords(self, text: str):
        """Check if any registered keywords are in the text and trigger actions"""
        for keyword, action in self.keyword_actions.items():
            if keyword in text:
                print(f"Keyword '{keyword}' detected! Triggering action...")
                action()

    def start_listening(self):
        """Start continuous listening loop"""
        print("Starting voice listener...")
        print(f"Registered keywords: {list(self.keyword_actions.keys())}")
        print("Press Ctrl+C to stop")

        try:
            while True:
                text = self.listen_once()
                if text:
                    self.check_keywords(text)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nStopping voice listener...")


# Example actions
def call_mom():
    """Example action: Call mom"""
    print("🤙 Calling mom...")
    # TODO: Implement actual phone call logic here
    # This could integrate with Twilio API or other telephony service


def play_music():
    """Example action: Play music"""
    print("🎵 Playing music...")
    # TODO: Implement music player logic here


def turn_off_lights():
    """Example action: Turn off lights"""
    print("💡 Turning off lights...")
    # TODO: Implement smart home integration here


if __name__ == '__main__':
    # Create listener
    listener = VoiceListener()

    # Register keyword-action pairs
    listener.register_action("엄마", call_mom)
    listener.register_action("음악", play_music)
    listener.register_action("불꺼", turn_off_lights)

    # Start listening
    listener.start_listening()
