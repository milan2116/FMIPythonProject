from app.models import User, Deck, Flashcard, Streak

def test_user_password_hashing():
    """Test that password hashing and verification work correctly."""
    user = User(username="testuser", email="test@example.com")
    user.password = "securepassword"
    assert user.verify_password("securepassword") is True
    assert user.verify_password("wrongpassword") is False

def test_create_deck(client):
    """Test that a deck object can be created successfully."""
    deck = Deck(title="Math", description="Algebra deck", user_id=1)
    assert deck.title == "Math"
    assert deck.description == "Algebra deck"

# def test_flashcard_review_logic(client, app):
#     """Test the spaced repetition logic for flashcards."""
#     with app.app_context():
#         flashcard = Flashcard(question="2+2?", answer="4", difficulty=2)
#         flashcard.ease_factor = 2.5
#         flashcard.repetitions = 0
#         flashcard.update_review(3) 
#         assert flashcard.repetitions > 0
#         assert flashcard.ease_factor >= 1.3

def test_streak_logic(client):
    """Test that streak tracking updates correctly."""
    streak = Streak(user_id=1, streak_count=5)
    assert streak.streak_count == 5

