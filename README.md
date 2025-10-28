# AI-Powered Book Management System

## Overview

A FastAPI-based REST API for managing books with AI-generated summaries (using Llama3 via Ollama), genre-based recommendations, JWT authentication, and PostgreSQL persistence. Fully containerized with Docker Compose.

## Features

- CRUD operations on books
- AI-generated summaries from book content (via ?content= query param)
- Genre-based recommendations
- JWT-based authentication (/token)
- Swagger UI at http://localhost:8000/docs
- Automated tests with pytest
- Dockerized (FastAPI + PostgreSQL + Ollama)

## Tech Stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| Backend          | FastAPI (Python)        |
| Database         | PostgreSQL + SQLAlchemy |
| AI Model         | Llama3:8b (via Ollama)  |
| Auth             | JWT (HS256)             |
| Containerization | Docker + Docker Compose |
| Testing          | pytest                  |

# Quick Start

## Clone & enter

git clone https://github.com/sxhxl/book_management_system
cd book_management_system

## Start (first time: downloads Llama3 ~4.7GB)

docker compose up --build

API: http://localhost:8000/docs

## API Endpoints

### Auth

#### POST /token

→ { "access_token": "...", "token_type": "bearer" }

- username: admin
- password: admin

#### Books

Add Book + AI Summary
POST /books/?content=<your book description>

{
"title": "Neural Dawn",
"author": "Grok AI",
"genre": "Sci-Fi",
"year_published": 2025
}
→ Returns book + AI-generated summary

List Books
GET /books/

Get Book
GET /books/{id}

Update Book
PUT /books/{id}

Delete Book
DELETE /books/{id}

### Get Recommendations

GET /recommendations/?genres=Sci-Fi,Thriller
→ Returns books matching any genre

## AI Summary Flow

1. Send content as query param in POST /books/
2. Ollama (Llama3) generates summary
3. Saved in DB and returned

## Testing

docker exec -it book_management_system-app-1 pytest tests/ -v

## Docker Tips

- First run: ~10 mins (downloads Llama3)
- Restart: Instant (docker compose down && docker compose up)
- Full reset: docker compose down -v

## Project Structure

.
├── app
│   ├── config.py
│   ├── dependencies.py
│   ├── **init**.py
│   ├── main.py
│   ├── models
│   │   ├── book.py
│   │   ├── **init**.py
│   │   └── review.py
│   ├── routers
│   │   ├── books.py
│   │   ├── **init**.py
│   │   └── recommendations.py
│   ├── schemas
│   │   ├── base.py
│   │   ├── book.py
│   │   ├── **init**.py
│   │   └── review.py
│   ├── services
│   │   ├── ai_service.py
│   │   ├── book_service.py
│   │   ├── **init**.py
│   │   └── review_service.py
│   └── utils
│   └── auth.py
├── docker-compose.yml
├── Dockerfile
├── init_db.py
├── migrations
├── README.md
├── requirements.txt
└── tests

9 directories, 24 files

## Troubleshooting

| Issue               | Fix                                     |
| ------------------- | --------------------------------------- |
| 401 Unauthorized    | Re-login, ensure JWT_SECRET_KEY matches |
| AI slow/no response | Wait for ollama pull llama3:8b          |
| DB errors           | docker compose down -v → rebuild        |
