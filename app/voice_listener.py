"""
Voice Listener Module
"""
import speech_recognition as sr
from typing import Callable, Dict, Optional


class VoiceListener:
    """Listens to audio and triggers actions based on detected keywords"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone: Optional[sr.Microphone] = None
        self.keyword_actions: Dict[str, Callable] = {}
        self.is_listening = False

    def initialize(self):
        """Initialize microphone and calibrate for ambient noise"""
        self.microphone = sr.Microphone()

        # Adjust recognizer sensitivity - VERY LOW for quiet environments
        self.recognizer.energy_threshold = 50  # Very low threshold
        self.recognizer.dynamic_energy_threshold = False  # Disable dynamic adjustment
        self.recognizer.pause_threshold = 0.8  # Shorter pause before considering phrase complete

        print("Calibrating for ambient noise... Please wait.")
        with self.microphone as source:
            # Don't adjust - keep our manual threshold
            source.SAMPLE_RATE = 48000  # Higher sample rate
        print("Calibration complete!")
        print(f"Energy threshold set to: {self.recognizer.energy_threshold}")

    def register_action(self, keyword: str, action: Callable):
        """Register an action to be triggered when a keyword is detected"""
        self.keyword_actions[keyword.lower()] = action
        print(f"Registered action for keyword: '{keyword}'")

    def unregister_action(self, keyword: str) -> bool:
        """Unregister an action by keyword"""
        keyword_lower = keyword.lower()
        if keyword_lower in self.keyword_actions:
            del self.keyword_actions[keyword_lower]
            return True
        return False

    def get_registered_keywords(self) -> list[str]:
        """Get list of registered keywords"""
        return list(self.keyword_actions.keys())

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 5) -> str:
        """Listen for a single phrase and return the recognized text"""
        if not self.microphone:
            raise RuntimeError("Microphone not initialized. Call initialize() first.")

        with self.microphone as source:
            print("🎤 Listening... Speak now!")
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
                print(f"✓ Audio captured, recognizing...")
            except Exception as e:
                print(f"❌ Failed to capture audio: {e}")
                return ""

        # Try Whisper first (more accurate)
        try:
            print("🔍 Using Whisper (OpenAI) for recognition...")
            text = self.recognizer.recognize_whisper(audio, language="korean")
            print(f"✅ Whisper recognized: '{text}'")
            return text.lower()
        except Exception as whisper_error:
            print(f"⚠️  Whisper failed: {whisper_error}")

            # Fallback to Google
            try:
                print("🔍 Falling back to Google Speech API...")
                text = self.recognizer.recognize_google(audio, language="ko-KR")
                print(f"✅ Google recognized: '{text}'")
                return text.lower()
            except sr.UnknownValueError:
                print("⚠️  Could not understand audio - try speaking louder and clearer")
                # Try without language specification as fallback
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"✅ Recognized (English): '{text}'")
                    return text.lower()
                except:
                    return ""
            except sr.RequestError as e:
                print(f"❌ Error with speech recognition service: {e}")
                return ""
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return ""

    def check_keywords(self, text: str) -> tuple[list[str], list[str]]:
        """Check if any registered keywords are in the text and trigger actions

        Returns:
            Tuple of (triggered keywords, action messages)
        """
        triggered = []
        messages = []
        for keyword, action in self.keyword_actions.items():
            if keyword in text:
                print(f"Keyword '{keyword}' detected! Triggering action...")
                try:
                    result = action()
                    triggered.append(keyword)
                    if result and isinstance(result, dict) and "message" in result:
                        messages.append(result["message"])
                except Exception as e:
                    print(f"Error executing action for '{keyword}': {e}")
        return triggered, messages

    def start_listening(self):
        """Start continuous listening loop"""
        import time

        if not self.microphone:
            self.initialize()

        print("Starting voice listener...")
        print(f"Registered keywords: {self.get_registered_keywords()}")
        print("Press Ctrl+C to stop")

        self.is_listening = True
        try:
            while self.is_listening:
                text = self.listen_once()
                if text:
                    self.check_keywords(text)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nStopping voice listener...")
        finally:
            self.is_listening = False

    def stop_listening(self):
        """Stop the listening loop"""
        self.is_listening = False