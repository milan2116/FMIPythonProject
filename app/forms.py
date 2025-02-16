"""
Forms for user registration, login, deck creation, and flashcard management.

This module contains the form classes used in the application to handle user input 
for various operations, including user registration, login, deck creation, and 
flashcard addition. These forms are built using Flask-WTF and WTForms, which provide 
easy integration with Flask for handling web forms with validation.

Each form includes the necessary fields, as well as validators for ensuring that 
the user input is valid.

Classes:
    - `RegistrationForm`: A form for user registration with fields for username, email, 
      password, and password confirmation.
    - `LoginForm`: A form for user login with fields for email and password.
    - `DeckForm`: A form for creating a new deck with fields for title and description.
    - `FlashcardForm`: A form for adding a new flashcard with fields for question and answer.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    """
        Form for user registration.

        This form is used for creating a new user account. It includes fields for the user's 
        username, email, password, and password confirmation. Validation is performed to ensure 
        that the username is within a valid length range, the email is properly formatted, 
        and the password confirmation matches the original password.

        Fields:
            - `username`: A required field with a length restriction (2-20 characters).
            - `email`: A required field with email format validation.
            - `password`: A required field for the user's password.
            - `confirm_password`: A required field for confirming the password, 
            must match the password.
            - `submit`: A submit button for submitting the form.
     """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                      EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """
        Form for user login.

        This form is used for users to log into their accounts. It includes fields for the 
        user's email and password, both of which are required.

        Fields:
            - `email`: A required field with email format validation.
            - `password`: A required field for the user's password.
            - `submit`: A submit button for submitting the form.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DeckForm(FlaskForm):
    """
    Form for creating a new deck.

    This form is used for users to create a new deck of flashcards. It includes fields 
    for the deck title (which is required) and an optional description.

    Fields:
        - `title`: A required field for the deck's title.
        - `description`: An optional field for providing a description of the deck.
        - `submit`: A submit button for submitting the form.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Deck')

class FlashcardForm(FlaskForm):
    """
    Form for adding a new flashcard.

    This form is used for users to add a new flashcard to a deck. It includes fields 
    for the question and answer, both of which are required.

    Fields:
        - `question`: A required field for the flashcard's question.
        - `answer`: A required field for the flashcard's answer.
        - `submit`: A submit button for submitting the form.
    """
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Add Flashcard')
