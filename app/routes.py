from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import app, db, mail
from app.models import User, Deck, Flashcard, Progress, Notification, Streak, Leaderboard
from app.forms import RegistrationForm, LoginForm, DeckForm, FlashcardForm
from flask_mail import Message
from threading import Thread
import csv
from io import StringIO
from app import login_manager
import json

@app.route('/')
def home():
    """
    home page
    """
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    handling registration
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    handling logging
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """
    Logging out
    """
    logout_user()
    return redirect(url_for('home'))

@app.route('/search')
def search():
    """
    Searching
    """
    query = request.args.get('query')  
    if query:
        decks = Deck.query.filter(Deck.title.contains(query) | 
                                  Deck.description.contains(query)).all()
        flashcards = Flashcard.query.filter(Flashcard.question.contains(query) | 
                                            Flashcard.answer.contains(query)).all()
        return render_template('search.html', decks=decks, flashcards=flashcards, query=query)
    return render_template('search.html')

@app.route('/deck/new', methods=['GET', 'POST'])
@login_required
def create_deck():
    """
    form for creating a deck
    """
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(deck)
        db.session.commit()
        flash('Deck created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_deck.html', form=form)

@app.route('/deck/<int:deck_id>')
@login_required
def view_deck(deck_id):
    """
    viewing deck
    """
    deck = Deck.query.get_or_404(deck_id)
    return render_template('deck.html', deck=deck)

@app.route('/deck/<int:deck_id>/review', methods=['GET', 'POST'])
@login_required
def review_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    due_flashcards = Flashcard.query.filter(
        Flashcard.deck_id == deck_id,
        Flashcard.next_review <= datetime.utcnow()
    ).all()

    if not due_flashcards:
        flash('No flashcards due for review today!', 'info')
        return redirect(url_for('view_deck', deck_id=deck_id))

    flashcard = due_flashcards[0]

    if request.method == 'POST':
        difficulty = int(request.form.get('difficulty'))
        flashcard.update_review(difficulty)

        leaderboard_entry = Leaderboard.query.filter_by(user_id=current_user.id).first()
        if not leaderboard_entry:
            leaderboard_entry = Leaderboard(user_id=current_user.id, score=0)
            db.session.add(leaderboard_entry)
        leaderboard_entry.score += 1
        db.session.commit()

        streak = Streak.query.filter_by(user_id=current_user.id).first()
        if not streak:
            streak = Streak(user_id=current_user.id, streak_count=0)
            db.session.add(streak)
        today = datetime.utcnow().date()
        if streak.last_studied:
            last_studied = streak.last_studied.date()
        else:
            last_studied = datetime.today().date() 
        if today > last_studied:
            if (today - last_studied).days == 1:
                streak.streak_count += 1
            else:
                streak.streak_count = 1
            streak.last_studied = datetime.utcnow()
        db.session.commit()

        flash('Flashcard reviewed!', 'success')
        return redirect(url_for('review_deck', deck_id=deck_id))

    return render_template('review.html', flashcard=flashcard)

from app.forms import FlashcardForm
from app.models import Flashcard, Deck

@app.route('/deck/<int:deck_id>/add_flashcard', methods=['GET', 'POST'])
@login_required
def add_flashcard(deck_id):
    deck = Deck.query.get_or_404(deck_id) 
    form = FlashcardForm()

    if form.validate_on_submit():
        flashcard = Flashcard(
            question=form.question.data,
            answer=form.answer.data,
            deck_id=deck.id
        )
        db.session.add(flashcard) 
        db.session.commit() 
        flash('Flashcard added successfully!', 'success')
        return redirect(url_for('view_deck', deck_id=deck.id)) 

    return render_template('add_flashcard.html', form=form, deck=deck)

@app.route('/progress')
@login_required
def progress():
    progress_data = Progress.query.filter_by(user_id=current_user.id).all()

    dates = [p.date.strftime('%Y-%m-%d') for p in progress_data] if progress_data else []
    counts = [p.cards_reviewed for p in progress_data] if progress_data else []

    return render_template('progress.html', progress_data=progress_data, dates=dates, counts=counts)

@app.route('/leaderboard')
def leaderboard():
    top_users = Leaderboard.query.order_by(Leaderboard.score.desc()).limit(10).all()
    return render_template('leaderboard.html', top_users=top_users)

@app.route('/notifications')
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=user_notifications)

@app.route('/notifications/mark_as_read/<int:notification_id>')
@login_required
def mark_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
        flash('Notification marked as read.', 'success')
    return redirect(url_for('notifications'))

@app.route('/deck/<int:deck_id>/export/json')
@login_required
def export_deck_json(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    flashcards = Flashcard.query.filter_by(deck_id=deck_id).all()
    deck_data = {
        'title': deck.title,
        'description': deck.description,
        'flashcards': [{'question': f.question, 'answer': f.answer} for f in flashcards]
    }
    json_data = json.dumps(deck_data, indent=4)
    file = StringIO()
    file.write(json_data)
    file.seek(0)
    return send_file(
        file,
        as_attachment=True,
        download_name=f'{deck.title}.json',
        mimetype='application/json'
    )

import csv
from io import StringIO

from io import StringIO, BytesIO

@app.route('/deck/<int:deck_id>/export/csv')
@login_required
def export_deck_csv(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    flashcards = Flashcard.query.filter_by(deck_id=deck_id).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Question', 'Answer'])
    for flashcard in flashcards:
        writer.writerow([flashcard.question, flashcard.answer])
    csv_bytes = BytesIO(output.getvalue().encode('utf-8'))
    output.close()
    csv_bytes.seek(0)
    return send_file(
        csv_bytes,
        as_attachment=True,
        download_name=f'{deck.title}.csv',
        mimetype='text/csv'
    )


from flask import request, flash
import json

@app.route('/deck/import/json', methods=['GET', 'POST'])
@login_required
def import_deck_json():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.json'):
            try:
                data = json.load(file)
                deck = Deck(
                    title=data['title'],
                    description=data.get('description', ''),
                    author=current_user
                )
                db.session.add(deck)
                db.session.commit()
                for card in data['flashcards']:
                    flashcard = Flashcard(
                        question=card['question'],
                        answer=card['answer'],
                        deck_id=deck.id
                    )
                    db.session.add(flashcard)
                db.session.commit()

                flash('Deck imported successfully!', 'success')
                return redirect(url_for('view_deck', deck_id=deck.id))
            except Exception as e:
                flash(f'Error importing deck: {str(e)}', 'danger')
        else:
            flash('Invalid file format. Please upload a JSON file.', 'danger')
    return render_template('import_deck_json.html')

@app.route('/deck/import/csv', methods=['GET', 'POST'])
@login_required
def import_deck_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            try:
                data = file.read().decode('utf-8').splitlines()
                reader = csv.reader(data)
                next(reader) 
                deck = Deck(
                    title=request.form.get('title', 'Imported Deck'),
                    description=request.form.get('description', ''),
                    author=current_user
                )
                db.session.add(deck)
                db.session.commit()
                for row in reader:
                    flashcard = Flashcard(
                        question=row[0],
                        answer=row[1],
                        deck_id=deck.id
                    )
                    db.session.add(flashcard)
                db.session.commit()

                flash('Deck imported successfully!', 'success')
                return redirect(url_for('view_deck', deck_id=deck.id))
            except Exception as e:
                flash(f'Error importing deck: {str(e)}', 'danger')
        else:
            flash('Invalid file format. Please upload a CSV file.', 'danger')
    return render_template('import_deck_csv.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500