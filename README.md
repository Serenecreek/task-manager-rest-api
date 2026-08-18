# Task Manager REST API

A backend REST API built with Flask, SQLAlchemy, SQLite, JWT authentication, and pytest.

This project demonstrates practical backend development concepts including RESTful API design, authentication, authorization, CRUD operations, relational database modeling, password hashing, JWT-based authentication, error handling, and automated testing.

## Features

- User registration
- Secure password hashing
- JWT authentication
- Login and token generation
- Current-user endpoint
- Create tasks
- Read tasks
- Update tasks
- Delete tasks
- User-specific task authorization
- SQLite database
- SQLAlchemy ORM
- Automated API testing with pytest
- HTTP status code handling
- PostgreSQL migration support through configuration

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate
- SQLAlchemy
- SQLite
- PostgreSQL-compatible configuration
- pytest
- Git/GitHub

## Architecture

```text
Client
   |
   | HTTP Request
   v
Flask API
   |
   +---- Authentication
   |         |
   |         +---- Password Hashing
   |         |
   |         +---- JWT
   |
   +---- Authorization
   |
   +---- SQLAlchemy ORM
             |
             v
        SQLite Database
