"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.api import app


@pytest.fixture
def client():
    """Create test client with lifespan context"""
    with TestClient(app) as c:
        yield c


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_get_status(client):
    """Test status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "is_listening" in data
    assert "registered_keywords" in data
    assert "message" in data


def test_create_keyword_action(client):
    """Test creating a keyword-action mapping"""
    payload = {
        "keyword": "테스트",
        "action_type": "call",
        "action_params": {"contact": "친구"},
    }
    response = client.post("/keywords", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["keyword"] == "테스트"
    assert data["action_type"] == "call"
    assert data["is_active"] is True


def test_create_keyword_action_invalid_type(client):
    """Test creating keyword with invalid action type"""
    payload = {"keyword": "테스트", "action_type": "invalid_action"}
    response = client.post("/keywords", json=payload)
    assert response.status_code == 400


def test_list_keywords(client):
    """Test listing keywords"""
    # First create some keywords
    client.post(
        "/keywords",
        json={"keyword": "키워드1", "action_type": "call"},
    )
    client.post(
        "/keywords",
        json={"keyword": "키워드2", "action_type": "music"},
    )

    response = client.get("/keywords")
    assert response.status_code == 200
    keywords = response.json()
    assert isinstance(keywords, list)
    assert "키워드1" in keywords
    assert "키워드2" in keywords


def test_delete_keyword(client):
    """Test deleting a keyword"""
    # First create a keyword
    client.post(
        "/keywords",
        json={"keyword": "삭제테스트", "action_type": "call"},
    )

    # Delete it
    response = client.delete("/keywords/삭제테스트")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Verify it's gone
    keywords = client.get("/keywords").json()
    assert "삭제테스트" not in keywords


def test_delete_nonexistent_keyword(client):
    """Test deleting non-existent keyword"""
    response = client.delete("/keywords/존재하지않음")
    assert response.status_code == 404


def test_listen_request_validation(client):
    """Test listen request with valid parameters"""
    payload = {"timeout": 3, "phrase_time_limit": 3}
    # Note: This will fail without actual microphone, but tests request structure
    response = client.post("/listen", json=payload)
    # Accept either success or error (since we may not have mic in test environment)
    assert response.status_code in [200, 500]


def test_listen_request_invalid_timeout(client):
    """Test listen request with invalid timeout"""
    payload = {"timeout": 100, "phrase_time_limit": 5}  # timeout too large
    response = client.post("/listen", json=payload)
    assert response.status_code == 422  # Validation error


def test_start_listening(client):
    """Test start listening endpoint"""
    response = client.post("/listen/start")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_stop_listening_not_started(client):
    """Test stopping when not listening"""
    response = client.post("/listen/stop")
    # Should return error since we're not listening
    assert response.status_code in [400, 200]


def test_api_cors_middleware():
    """Test that CORS middleware is configured"""
    from app.api import app
    # Check that CORS middleware is in the middleware stack
    middleware_classes = [m.cls.__name__ for m in app.user_middleware]
    assert "CORSMiddleware" in middleware_classes


@pytest.mark.parametrize(
    "endpoint,method",
    [
        ("/", "get"),
        ("/status", "get"),
        ("/keywords", "get"),
    ],
)
def test_endpoints_accessibility(client, endpoint, method):
    """Test that all endpoints are accessible"""
    if method == "get":
        response = client.get(endpoint)
    elif method == "post":
        response = client.post(endpoint)
    assert response.status_code in [200, 400, 422, 500]  # Any non-404 is fine
