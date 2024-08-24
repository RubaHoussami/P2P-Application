# Peer-to-Peer Application

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Directory Structure](#directory-structure) 
4. [Installation](#installation)
5. [Testing](#testing)
6. [License](#license)

## Introduction

This Flask application is designed to facilitate Peer-to-Peer (P2P) transfers, providing users with secure account management and transaction handling. It supports user registration, login, account balance management, and transaction history tracking. The application also integrates JWT-based authentication to ensure secure user sessions. This application is built with Flask and PostgreSQL and will be deployed on AWS Elastic Beanstalk with AWS RDS.

## Features

- **User Authentication**: Secure login and registration using JWT tokens with protected routes.
- **Account Management**: Top-up balance and view account details.
- **P2P Transfers**: Seamless money transfers between user accounts.
- **Transaction History**: View past transactions.
- **Logging**: Integrated logging for monitoring and debugging.

## Directory Structure

The P2P Transfer Module is organized using the MVC (Model-View-Controller) architecture. This design ensures a clean separation of concerns, making the application more maintainable and scalable.

- **`/migrations`**: Database migrations managed by Flask-Migrate.
- **`/src`**: Core application code.
  - **`/api/v1/`**
      - **`/controllers`**: Flask routes for handling API requests.
      - **`/schemas`**: Marshmallow schemas for data serialization and validation.
  - **`/models`**: SQLAlchemy models for the database schema.
  - **`/services`**: Business logic handling P2P transfers, account management, and more.
  - **`/utils`**: Utility functions used by the entire application.
- **`/tests`**: Unit tests for the application.
- **`app.py`**: Main entry point of the application.
- **`config.py`**: Configuration settings for different environments.
- **`extensions.py`**: Extensions setup (e.g., database, JWT, Migrate).
- **`logger.py`**: Logger setup.
- **`requirements.txt`**: Python dependencies.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/RubaHoussami/Peer-to-Peer-Application.git
    cd Peer-to-Peer-Application
    ```

2. Set up a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Configure your environment variables in a `.env` file:
    ```bash
    FLAS_ENV=development
    SQLALCHEMY_DATABASE_URI=your_database_url
    ...
    ```

4. Initialize database and run database migrations:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Start the application:
    ```bash
    flask run
    ```

## Testing

To run the unit tests:
```bash
set FLASK_ENV=testing
pytest
```

To get a coverage report:
```bash
coverage run -m pytest
coverage report
```

## License

This project is licensed under the MIT License.
