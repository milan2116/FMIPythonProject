"""
Module for models
"""
# pylint: disable=trailing-whitespace
from datetime import datetime, timedelta
from flask_login import UserMixin
from argon2 import PasswordHasher
from app import db
from app import login_manager

ph = PasswordHasher()


class User(db.Model, UserMixin):
    """
    User Module
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) 
    decks = db.relationship('Deck', backref='author', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    streak = db.relationship('Streak', backref='user', uselist=False, lazy=True)

    @property
    def password(self):
        """
        password handling
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        password hashing
        """
        self.password_hash = ph.hash(password)

    def verify_password(self, password):
        """
        verifying password
        """
        try:
            return ph.verify(self.password_hash, password)
        except:
            return False
        
@login_manager.user_loader
def load_user(user_id):
    """
    loading user
    """
    return User.query.get(int(user_id))

class Deck(db.Model):
    """
    Deck Module
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', backref='deck', lazy=True)

class Flashcard(db.Model):
    """
    Flashcard Module
    """
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, default=1)
    next_review = db.Column(db.DateTime, default=datetime.utcnow)
    interval = db.Column(db.Integer, default=1)
    repetitions = db.Column(db.Integer, default=0)
    ease_factor = db.Column(db.Float, default=2.5)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    def update_review(self, difficulty):
        """
        update when reviewing
        """
        if difficulty < 1 or difficulty > 3:
            raise ValueError("Difficulty must be between 1 and 3.")
        self.ease_factor = max(1.3, self.ease_factor + (0.1 - (3 - difficulty) * 
                                                        (0.08 + (3 - difficulty) * 0.02)))
        if difficulty >= 2:
            self.repetitions += 1
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
        else:
            self.repetitions = 0
            self.interval = 1
        self.next_review = datetime.utcnow() + timedelta(days=self.interval)
        db.session.commit()

class Progress(db.Model):
    """
    Progress Module
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    cards_reviewed = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    """
    Notification Module
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Streak(db.Model):
    """
    Streak Module
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_studied = db.Column(db.DateTime, default=datetime.utcnow)
    streak_count = db.Column(db.Integer, default=0)

class Leaderboard(db.Model):
    """
    Leaderboard Module
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref='leaderboard_entry')
