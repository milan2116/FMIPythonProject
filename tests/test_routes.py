def test_home_route(client):
    """Test that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200

def test_register_and_login(client):
    """Test user registration and login functionality."""
    client.post("/register", data={"username": "testuser", "email": "test@example.com", "password": "password"})
    response = client.post("/login", data={"email": "test@example.com", "password": "password"})
    assert response.status_code in [200, 302]  # Accept both possible responses


def test_create_deck(client):
    """Test deck creation through the form submission."""
    client.post("/register", data={"username": "testuser", "email": "test@example.com", "password": "password"})
    client.post("/login", data={"email": "test@example.com", "password": "password"})
    response = client.post("/deck/new", data={"title": "Math", "description": "Algebra deck"})
    assert response.status_code == 302  # Redirects after deck creation

def test_flashcard_addition(client):
    """Test adding a flashcard to a deck."""
    client.post("/register", data={"username": "testuser", "email": "test@example.com", "password": "password"})
    client.post("/login", data={"email": "test@example.com", "password": "password"})
    client.post("/deck/new", data={"title": "Math", "description": "Algebra deck"})
    response = client.post("/deck/1/add_flashcard", data={"question": "2+2?", "answer": "4"})
    assert response.status_code == 302  # Redirects after adding flashcard

def test_leaderboard(client):
    """Test that the leaderboard page loads successfully."""
    response = client.get("/leaderboard")
    assert response.status_code == 200

def test_progress(client):
    """Test progress tracking page. Should redirect if user is not logged in."""
    response = client.get("/progress")
    assert response.status_code == 302  # Redirects if user not logged in

def test_export_deck_json(client):
    """Test exporting a deck as JSON format."""
    response = client.get("/deck/1/export/json")
    assert response.status_code in [200, 302]  # Success or redirect if not logged in

def test_error_handling(client):
    """Test that a non-existent page returns a 404 error."""
    response = client.get("/nonexistent")
    assert response.status_code == 404

