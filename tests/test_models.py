"""
Tests for Pydantic Models
"""
import pytest
from pydantic import ValidationError
from app.models import (
    KeywordActionCreate,
    KeywordActionResponse,
    ListenRequest,
    ListenResponse,
    StatusResponse,
)


def test_keyword_action_create_valid():
    """Test creating valid KeywordActionCreate"""
    model = KeywordActionCreate(
        keyword="테스트", action_type="call", action_params={"contact": "친구"}
    )
    assert model.keyword == "테스트"
    assert model.action_type == "call"
    assert model.action_params["contact"] == "친구"


def test_keyword_action_create_minimal():
    """Test creating KeywordActionCreate with minimal data"""
    model = KeywordActionCreate(keyword="테스트", action_type="call")
    assert model.keyword == "테스트"
    assert model.action_type == "call"
    assert model.action_params is None


def test_keyword_action_create_empty_keyword():
    """Test that empty keyword is invalid"""
    with pytest.raises(ValidationError):
        KeywordActionCreate(keyword="", action_type="call")


def test_keyword_action_response():
    """Test KeywordActionResponse model"""
    model = KeywordActionResponse(
        keyword="테스트", action_type="call", action_params={"contact": "친구"}
    )
    assert model.keyword == "테스트"
    assert model.action_type == "call"
    assert model.is_active is True


def test_listen_request_defaults():
    """Test ListenRequest with default values"""
    model = ListenRequest()
    assert model.timeout == 5
    assert model.phrase_time_limit == 5


def test_listen_request_custom_values():
    """Test ListenRequest with custom values"""
    model = ListenRequest(timeout=10, phrase_time_limit=15)
    assert model.timeout == 10
    assert model.phrase_time_limit == 15


def test_listen_request_validation_min():
    """Test ListenRequest validation for minimum values"""
    with pytest.raises(ValidationError):
        ListenRequest(timeout=0)

    with pytest.raises(ValidationError):
        ListenRequest(phrase_time_limit=0)


def test_listen_request_validation_max():
    """Test ListenRequest validation for maximum values"""
    with pytest.raises(ValidationError):
        ListenRequest(timeout=31)

    with pytest.raises(ValidationError):
        ListenRequest(phrase_time_limit=31)


def test_listen_response():
    """Test ListenResponse model"""
    model = ListenResponse(
        recognized_text="엄마한테 전화해", triggered_keywords=["엄마", "전화"], success=True
    )
    assert model.recognized_text == "엄마한테 전화해"
    assert len(model.triggered_keywords) == 2
    assert model.success is True


def test_status_response():
    """Test StatusResponse model"""
    model = StatusResponse(
        is_listening=True,
        registered_keywords=["엄마", "음악"],
        message="Status retrieved",
    )
    assert model.is_listening is True
    assert len(model.registered_keywords) == 2
    assert "엄마" in model.registered_keywords


def test_models_json_serialization():
    """Test that models can be serialized to JSON"""
    model = KeywordActionCreate(keyword="테스트", action_type="call")
    json_data = model.model_dump()
    assert json_data["keyword"] == "테스트"
    assert json_data["action_type"] == "call"


def test_models_json_deserialization():
    """Test that models can be created from JSON"""
    json_data = {"keyword": "테스트", "action_type": "call"}
    model = KeywordActionCreate(**json_data)
    assert model.keyword == "테스트"
    assert model.action_type == "call"
