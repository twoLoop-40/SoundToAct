"""
Action handlers for detected keywords
"""
from typing import Dict, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class ActionRegistry:
    """Registry for managing actions"""

    def __init__(self):
        self.actions: Dict[str, Callable] = {}
        self._register_default_actions()

    def _register_default_actions(self):
        """Register default actions"""
        self.register("call", self.call_action)
        self.register("music", self.play_music_action)
        self.register("lights", self.lights_action)

    def register(self, action_type: str, handler: Callable):
        """Register an action handler"""
        self.actions[action_type] = handler
        logger.info(f"Registered action handler: {action_type}")

    def get_handler(self, action_type: str) -> Optional[Callable]:
        """Get action handler by type"""
        return self.actions.get(action_type)

    def create_action(
        self, action_type: str, action_params: Optional[dict] = None
    ) -> Callable:
        """Create an action callable with parameters"""
        handler = self.get_handler(action_type)
        if not handler:
            raise ValueError(f"Unknown action type: {action_type}")

        def action():
            return handler(action_params or {})

        return action

    # Default action implementations
    @staticmethod
    def call_action(params: dict):
        """Handle call action"""
        contact = params.get("contact", "엄마")
        number = params.get("number", "")
        message = f"🤙 {contact}에게 전화를 걸었습니다."
        logger.info(f"{message} ({number})")
        print(message)
        # TODO: Integrate with Twilio or other telephony service
        return {"status": "success", "action": "call", "contact": contact, "message": message}

    @staticmethod
    def play_music_action(params: dict):
        """Handle play music action"""
        song = params.get("song", "")
        playlist = params.get("playlist", "")
        music_name = song or playlist or "음악"
        message = f"🎵 {music_name}을 재생했습니다."
        logger.info(message)
        print(message)
        # TODO: Integrate with music player API
        return {"status": "success", "action": "music", "song": song, "message": message}

    @staticmethod
    def lights_action(params: dict):
        """Handle lights control action"""
        state = params.get("state", "off")
        room = params.get("room", "전체")
        state_text = "켰습니다" if state == "on" else "껐습니다"
        message = f"💡 {room} 불을 {state_text}."
        logger.info(message)
        print(message)
        # TODO: Integrate with smart home API
        return {"status": "success", "action": "lights", "state": state, "room": room, "message": message}


# Global action registry instance
action_registry = ActionRegistry()
