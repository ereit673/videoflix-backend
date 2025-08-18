# Videoflix Backend

A Django REST API backend for Videoflix, supporting user authentication, video management, background processing, and media streaming.

---

## Features

- User registration, activation, and JWT authentication
- Password reset with email links
- Video upload, conversion (480p/720p), and folder management
- Background tasks with Django RQ and Redis
- PostgreSQL database
- Dockerized for easy local development and deployment

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ereit673/videoflix-backend.git
cd videoflix-backend
```

### 2. Configure Environment Variables

Copy the provided `.env.template` to `.env` and fill in your secrets and configuration:

```bash
cp .env.template .env
```

Edit `.env` and set values for:

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `REDIS_HOST`, `REDIS_PORT`, etc.
- Email settings for activation and password reset

### 3. Build and Start Docker Containers

```bash
docker-compose up --build
```

This will start:

- PostgreSQL database
- Redis server
- Django backend (on port 8000)

### 4. Run Migrations

In a new terminal, run:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 5. Access the Application

- API: [http://localhost:8000/api/](http://localhost:8000/api/)
- Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Development Notes

- Media files are stored in `/media` and static files in `/static` (both are Docker volumes).
- Background jobs (video conversion, email) are handled by Django RQ and Redis.
- To run RQ workers:
  ```bash
  docker-compose exec web python manage.py rqworker
  ```
- To check the database, use:
  ```bash
  docker-compose exec db psql -U <DB_USER> <DB_NAME>
  ```

---

## Environment Variables

See `.env.template` for all required variables.  
**Never commit your real `.env` file to version control!**

---

## Useful Commands

- Collect static files:
  ```bash
  docker-compose exec web python manage.py collectstatic
  ```

---
