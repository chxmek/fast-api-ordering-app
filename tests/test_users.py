"""Test user endpoints."""


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_user(client):
    """Test creating a new user."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data


def test_create_duplicate_user(client):
    """Test creating a user with duplicate email."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    # Create first user
    client.post("/api/v1/users/", json=user_data)
    # Try to create duplicate
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_get_users(client):
    """Test getting all users."""
    # Create some users
    users = [
        {"name": "User 1", "email": "user1@example.com"},
        {"name": "User 2", "email": "user2@example.com"},
    ]
    for user in users:
        client.post("/api/v1/users/", json=user)
    
    # Get all users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_user_by_id(client):
    """Test getting a user by ID."""
    # Create a user
    user_data = {"name": "Test User", "email": "test@example.com"}
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Get user by ID
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]


def test_get_nonexistent_user(client):
    """Test getting a user that doesn't exist."""
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
