"""
Tests for VoiceListener
"""
import pytest
from app.voice_listener import VoiceListener


def test_voice_listener_initialization():
    """Test VoiceListener can be initialized"""
    listener = VoiceListener()
    assert listener.recognizer is not None
    assert listener.microphone is None
    assert listener.keyword_actions == {}
    assert listener.is_listening is False


def test_register_action(voice_listener, mock_action):
    """Test registering an action"""
    voice_listener.register_action("test", mock_action)
    assert "test" in voice_listener.keyword_actions
    assert voice_listener.keyword_actions["test"] == mock_action


def test_register_action_case_insensitive(voice_listener, mock_action):
    """Test that keywords are stored in lowercase"""
    voice_listener.register_action("TEST", mock_action)
    assert "test" in voice_listener.keyword_actions
    assert "TEST" not in voice_listener.keyword_actions


def test_unregister_action(voice_listener, mock_action):
    """Test unregistering an action"""
    voice_listener.register_action("test", mock_action)
    assert voice_listener.unregister_action("test") is True
    assert "test" not in voice_listener.keyword_actions


def test_unregister_nonexistent_action(voice_listener):
    """Test unregistering a non-existent action"""
    assert voice_listener.unregister_action("nonexistent") is False


def test_get_registered_keywords(voice_listener, mock_action):
    """Test getting registered keywords"""
    voice_listener.register_action("keyword1", mock_action)
    voice_listener.register_action("keyword2", mock_action)

    keywords = voice_listener.get_registered_keywords()
    assert len(keywords) == 2
    assert "keyword1" in keywords
    assert "keyword2" in keywords


def test_check_keywords(voice_listener, mock_action):
    """Test keyword checking and action triggering"""
    voice_listener.register_action("엄마", mock_action)
    voice_listener.register_action("음악", mock_action)

    # Test single keyword
    triggered = voice_listener.check_keywords("엄마한테 전화해")
    assert len(triggered) == 1
    assert "엄마" in triggered
    assert len(mock_action.calls) == 1


def test_check_keywords_multiple(voice_listener):
    """Test multiple keywords in same text"""
    action1_calls = []
    action2_calls = []

    def action1():
        action1_calls.append(True)

    def action2():
        action2_calls.append(True)

    voice_listener.register_action("엄마", action1)
    voice_listener.register_action("전화", action2)

    triggered = voice_listener.check_keywords("엄마한테 전화해")
    assert len(triggered) == 2
    assert "엄마" in triggered
    assert "전화" in triggered
    assert len(action1_calls) == 1
    assert len(action2_calls) == 1


def test_check_keywords_no_match(voice_listener, mock_action):
    """Test keyword checking with no matches"""
    voice_listener.register_action("엄마", mock_action)

    triggered = voice_listener.check_keywords("안녕하세요")
    assert len(triggered) == 0
    assert len(mock_action.calls) == 0


def test_stop_listening(voice_listener):
    """Test stopping the listener"""
    voice_listener.is_listening = True
    voice_listener.stop_listening()
    assert voice_listener.is_listening is False
