"""
CLI Example - Voice-triggered automation app
Run this for a simple command-line interface demonstration
"""
from app.voice_listener import VoiceListener
from app.actions import action_registry


# Example actions
def call_mom():
    """Example action: Call mom"""
    print("🤙 Calling mom...")
    return action_registry.call_action({"contact": "엄마", "number": "010-1234-5678"})


def play_music():
    """Example action: Play music"""
    print("🎵 Playing music...")
    return action_registry.play_music_action({"song": "favorite"})


def turn_off_lights():
    """Example action: Turn off lights"""
    print("💡 Turning off lights...")
    return action_registry.lights_action({"state": "off", "room": "all"})


if __name__ == "__main__":
    # Create listener
    listener = VoiceListener()
    listener.initialize()

    # Register keyword-action pairs
    listener.register_action("엄마", call_mom)
    listener.register_action("음악", play_music)
    listener.register_action("불꺼", turn_off_lights)

    # Start listening
    listener.start_listening()
