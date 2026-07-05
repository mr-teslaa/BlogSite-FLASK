# BlogSite-FLASK

A full-featured Flask blogging web application with user authentication, post management, profile pictures, pagination, password reset via email, and custom error pages.

This project follows [Corey Schafer's Flask tutorial series](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) on YouTube, with personal adjustments and dependency updates to run on **Flask 3.x** and current stable packages.

[![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/mr-teslaa/BlogSite-FLASK?style=social)](https://github.com/mr-teslaa/BlogSite-FLASK/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/mr-teslaa/BlogSite-FLASK)](https://github.com/mr-teslaa/BlogSite-FLASK/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/mr-teslaa/BlogSite-FLASK)](https://github.com/mr-teslaa/BlogSite-FLASK/pulls)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Origin](#project-origin)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Migrations](#database-migrations)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- User registration, login, and logout
- User account page with profile picture upload
- Create, read, update, and delete blog posts
- Paginated home page
- Password reset flow via email
- Blueprint-based application structure
- Custom error pages (403, 404, 500)
- Application factory pattern (`create_app`)

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | [Flask 3.1.3](https://flask.palletsprojects.com/) |
| ORM | [Flask-SQLAlchemy 3.x](https://flask-sqlalchemy.palletsprojects.com/) |
| Migrations | [Flask-Migrate](https://flask-migrate.readthedocs.io/) / Alembic |
| Auth | [Flask-Login](https://flask-login.readthedocs.io/), [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/) |
| Forms | [Flask-WTF](https://flask-wtf.readthedocs.io/) / WTForms |
| Email | [Flask-Mail](https://pythonhosted.org/Flask-Mail/) |
| Frontend | Bootstrap, Jinja2 templates |

---

## Project Origin

This repository is a learning project built alongside Corey Schafer's **Flask Tutorials** YouTube playlist. The original tutorial targeted Flask 1.x; this fork has been updated for **Flask 3.x** and modern dependency versions while keeping the same overall application design.

| Resource | Link |
|----------|------|
| YouTube Playlist | [Flask Tutorials by Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) |
| Official Code Snippets | [CoreyMSchafer/code_snippets — Flask_Blog](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog) |

> **Note:** If you prefer a different playlist link or want to swap in your own course reference, replace the playlist URL in this README.

---

## Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Git**
- A Gmail account (or compatible SMTP provider) if you want password-reset emails to work

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mr-teslaa/BlogSite-FLASK.git
cd BlogSite-FLASK
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

See [Configuration](#configuration) for details on each variable.

### 5. Initialize the database

```bash
flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade
```

> If `migrations/` already exists in the repo, you can skip `db init` and run only `db upgrade`.

---

## Configuration

Create a `.env` file in the project root (never commit this file):

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions and tokens | `your-random-secret-key` |
| `SQLALCHEMY_DATABASE_URI` | Database connection string | `sqlite:///site.db` |
| `EMAIL_USERNAME` | SMTP email address | `you@gmail.com` |
| `EMAIL_PASSWORD` | SMTP password or app password | `your-app-password` |

Example `.env`:

```env
SECRET_KEY=replace-with-a-long-random-string
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
EMAIL_USERNAME=you@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) rather than your main account password.

---

## Running the Application

With your virtual environment activated:

```bash
flask --app run.py run --debug
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

Alternative (direct Python entry point):

```bash
python run.py
```

---

## Database Migrations

This project uses **Flask-Migrate** (Alembic). After changing models in `flaskblog/models.py`:

```bash
# Create a new migration
flask --app run.py db migrate -m "Describe your change"

# Apply migrations
flask --app run.py db upgrade
```

Other useful commands:

```bash
# Show migration history
flask --app run.py db history

# Roll back one migration
flask --app run.py db downgrade
```

> **Flask 3 note:** The tutorial originally used `python manage.py` or `flask run` without `--app`. With Flask 3, use `flask --app run.py` so the CLI finds your application instance.

---

## Project Structure

```
BlogSite-FLASK/
├── flaskblog/
│   ├── __init__.py          # Application factory and extension setup
│   ├── config.py            # Configuration (loads from .env)
│   ├── models.py            # User and Post models
│   ├── main/                # Home and about routes
│   ├── posts/               # Post CRUD routes and forms
│   ├── users/               # Auth, account, and reset routes
│   ├── errors/              # Error handlers
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, and uploaded images
├── migrations/              # Alembic migration scripts
├── instance/                # Local SQLite database (created at runtime)
├── run.py                   # Application entry point
├── requirements.txt         # Pinned Python dependencies
├── .env.example             # Environment variable template
└── README.md
```

---

## Contributing

Contributions are welcome. Whether you are fixing a bug, improving documentation, or adding a feature, please follow these steps:

1. **Fork** the repository
2. **Create a branch** from `master`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and test locally
4. **Commit** with a clear message:
   ```bash
   git commit -m "Add short description of what changed and why"
   ```
5. **Push** to your fork and open a **Pull Request** against `master`

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on code style, pull requests, and issue reporting.

### Reporting Issues

When opening an issue, include:

- A clear title and description
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Your OS and Python version
- Relevant error messages or screenshots

---

## Code of Conduct

Be respectful and constructive. Harassment, spam, and abusive behavior are not tolerated. By participating in this project, you agree to help maintain a welcoming environment for everyone.

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for the full text.

---

## Acknowledgements

- **[Corey Schafer](https://www.youtube.com/user/schafer5)** — Original Flask tutorial series that this project is based on
- **[Flask](https://flask.palletsprojects.com/)** and the Pallets ecosystem
- All contributors who report issues and submit pull requests

---

<p align="center">
  Built with Flask 3 · Updated from the Corey Schafer tutorial series
</p>
