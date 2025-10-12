"""
Tests for Action Registry
"""
import pytest
from app.actions import ActionRegistry


def test_action_registry_initialization():
    """Test ActionRegistry initializes with default actions"""
    registry = ActionRegistry()
    assert "call" in registry.actions
    assert "music" in registry.actions
    assert "lights" in registry.actions


def test_register_custom_action():
    """Test registering a custom action"""
    registry = ActionRegistry()

    def custom_action(params):
        return "custom"

    registry.register("custom", custom_action)
    assert "custom" in registry.actions
    assert registry.get_handler("custom") == custom_action


def test_get_handler():
    """Test getting action handler"""
    registry = ActionRegistry()
    handler = registry.get_handler("call")
    assert handler is not None
    assert callable(handler)


def test_get_handler_nonexistent():
    """Test getting non-existent handler"""
    registry = ActionRegistry()
    handler = registry.get_handler("nonexistent")
    assert handler is None


def test_create_action():
    """Test creating an action with parameters"""
    registry = ActionRegistry()
    action = registry.create_action("call", {"contact": "엄마", "number": "010-1234-5678"})
    assert callable(action)

    result = action()
    assert result["status"] == "success"
    assert result["action"] == "call"
    assert result["contact"] == "엄마"


def test_create_action_invalid_type():
    """Test creating action with invalid type"""
    registry = ActionRegistry()
    with pytest.raises(ValueError, match="Unknown action type"):
        registry.create_action("invalid_type")


def test_call_action():
    """Test call action"""
    registry = ActionRegistry()
    result = registry.call_action({"contact": "친구", "number": "010-9999-9999"})
    assert result["status"] == "success"
    assert result["action"] == "call"
    assert result["contact"] == "친구"


def test_play_music_action():
    """Test play music action"""
    registry = ActionRegistry()
    result = registry.play_music_action({"song": "My Favorite Song"})
    assert result["status"] == "success"
    assert result["action"] == "music"
    assert result["song"] == "My Favorite Song"


def test_lights_action():
    """Test lights control action"""
    registry = ActionRegistry()
    result = registry.lights_action({"state": "on", "room": "bedroom"})
    assert result["status"] == "success"
    assert result["action"] == "lights"
    assert result["state"] == "on"
    assert result["room"] == "bedroom"


def test_action_with_default_params():
    """Test actions with default parameters"""
    registry = ActionRegistry()

    # Test with empty params
    result = registry.call_action({})
    assert result["contact"] == "엄마"

    result = registry.lights_action({})
    assert result["state"] == "off"
    assert result["room"] == "all"