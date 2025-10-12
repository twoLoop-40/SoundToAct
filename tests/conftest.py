"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.voice_listener import VoiceListener


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def voice_listener():
    """VoiceListener instance for testing"""
    return VoiceListener()


@pytest.fixture
def mock_action():
    """Mock action for testing"""
    calls = []

    def action():
        calls.append(True)
        return "action executed"

    action.calls = calls
    return action
