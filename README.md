
# Flashcard Master

Flashcard Master is a web-based flashcard application designed to help users review and memorize information using spaced repetition algorithms. Users can register, create flashcards, and track their progress.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Prerequisites

Ensure you have the following installed on your machine:

- Python (>= 3.8)
- pip (Python package installer)
- A virtual environment tool (e.g., `venv`, `virtualenv`)

### Step-by-Step Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/flashcard-master.git
   cd flashcard-master
   ```

2. Create and activate a virtual environment:

   - For Windows:
     ```bash
     python -m venv venv
     .env\Scriptsctivate
     ```

   - For macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables (you might want to create a `.env` file):

   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///yourdatabase.db
   ```

   You may also need to configure your database based on your preferred settings (e.g., SQLite, PostgreSQL).

5. Run database migrations to set up the database:

   ```bash
   flask db upgrade
   ```

---

## Usage

### Running the Application

To start the application locally, use the following command:

```bash
flask run
```

This will start the Flask server, typically available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Registering and Logging In

1. Open your browser and navigate to [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register).
2. Register a new user account with a username, email, and password.
3. After registration, you will be redirected to log in at [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login).
4. Once logged in, you can start creating, reviewing, and tracking your flashcards.

---

## Testing

### Running Tests

To run the tests, you need to install the testing dependencies:

```bash
pip install -r requirements-dev.txt
```

You can run the tests using `pytest`:

```bash
pytest
```

This will execute all the tests in your `tests/` directory and display the results in the terminal.

### Test Coverage

To check test coverage, you can use `pytest-cov`:

```bash
pytest --cov=app
```

This will give you a report on how much of your code is covered by the tests.

---

## Contributing

We welcome contributions! To get started:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with a descriptive message.
4. Push your branch to your fork.
5. Open a pull request with a clear description of the changes.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
