# Contributing to BlogSite-FLASK

Thank you for considering a contribution. This document explains how to work on the project in a way that keeps changes easy to review and merge.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a virtual environment and install dependencies (see [README.md](README.md#installation))
4. Copy `.env.example` to `.env` and configure your local settings
5. Run the app and confirm it works before making changes

## Development Workflow

1. Create a feature branch from `master`:
   ```bash
   git checkout -b fix/issue-description
   ```
2. Make focused changes — one logical change per pull request when possible
3. Test your changes locally:
   ```bash
   flask --app run.py run --debug
   ```
4. If you changed database models, create and apply a migration:
   ```bash
   flask --app run.py db migrate -m "Describe model change"
   flask --app run.py db upgrade
   ```
5. Commit with a descriptive message
6. Push to your fork and open a pull request

## Pull Request Guidelines

- **Target branch:** `master`
- **Title:** Short summary of the change (e.g. `Fix pagination on home page`)
- **Description:** Explain what changed and why; link related issues if applicable
- **Scope:** Avoid unrelated refactors in the same PR
- **Secrets:** Never commit `.env`, passwords, API keys, or personal data
- **Dependencies:** If you add or upgrade packages, update `requirements.txt` and note breaking changes in the PR description

## Code Style

Match the existing project conventions:

- Use the application factory pattern (`create_app` in `flaskblog/__init__.py`)
- Register routes through **Blueprints** (`main`, `users`, `posts`, `errors`)
- Keep configuration in `flaskblog/config.py` and load secrets from environment variables
- Use Flask-WTF forms for user input
- Follow existing naming and file layout under `flaskblog/`

## Reporting Bugs

Open a [GitHub Issue](https://github.com/mr-teslaa/BlogSite-FLASK/issues) with:

1. What you expected to happen
2. What actually happened
3. Steps to reproduce
4. Python version (`python --version`)
5. OS (Windows, macOS, Linux)
6. Full error traceback if available

## Feature Requests

Feature requests are welcome. Open an issue first to discuss the idea before investing significant effort, especially for large changes.

## Questions

If you are working through the Corey Schafer Flask tutorial and adapting it for Flask 3, check the [README](README.md#project-origin) for updated CLI commands and dependency notes before opening an issue.

Thank you for helping improve this project.
