# com.diegoenriquezserrano.api

[![Django CI](https://github.com/DiegoEnriquezSerrano/com.diegoenriquezserrano.api/actions/workflows/ci.yml/badge.svg)](https://github.com/DiegoEnriquezSerrano/com.diegoenriquezserrano.api/actions/workflows/ci.yml)

A RESTful API built with Django and Django REST Framework that allows multiple users to create, manage, and subscribe to newsletters via a separate authorized client application. Users can manage their newsletters and subscribers. Includes support for registered user subscriptions as well as unregistered subscribers. User registrations and unregistered subscriptions require confirmed receipt of emailed timestamped signed tokens for activation. The API supports token-based authentication.

---

## Index

- [Features](#features)
- [Stack](#tech-stack)
- [Requirements](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database](#database-migrations)
- [Running the Application](#running-the-application)
- [Authentication](#authentication)
- [Testing](#testing)
- [License](#license)

---

## Features

- User registration, confirmation and token-based authentication
- User and non-user subscriptions
- User profiles
- Post categories, comments, likes and bookmarks
- Post notifications

---

## Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- Django REST Framework Simple JWT
- PostgreSQL 17+
- Docker & Docker Compose

---

## Requirements

- Python 3.10 or higher
- pip
- Docker & Docker Compose

---

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/DiegoEnriquezSerrano/com.diegoenriquezserrano.api.git
   cd ./com.diegoenriquezserrano.api
   ```

2. Create and activate a virtual environment

   ```bash
   python3 -m venv .
   source bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Build docker environment
   ```bash
   docker compose build
   ```

---

## Configuration

1. Copy `example.env` to `.env`

   ```bash
   cp example.env .env
   ```

2. Update environment variables in `.env`, refer to comments for directions on setting values.

---

## Database

Run the following commands to initialize your database:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Running the Application

1. Start your services using docker compose
   ```bash
   docker compose up -d
   ```

Your API will be accessible at `http://localhost:8000/`.

---

## Authentication

This API uses JWT for authentication. Include the token in the `Authorization` header for protected endpoints:

```text
Authorization: Bearer <your-access-token>
```

the token is also sent as an Http cookie upon successful login attempt.

---

## Testing

Run tests with:

```bash
python manage.py test
```

---

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the COPYING file for details.
