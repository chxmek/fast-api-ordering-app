# FastAPI Ordering System

A professional FastAPI application for ordering management with PostgreSQL database.

## Features

- ✅ FastAPI framework with async support
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Pydantic v2 for data validation
- ✅ CORS middleware configured
- ✅ Environment-based configuration
- ✅ Modular project structure
- ✅ RESTful API design
- ✅ Auto-generated API documentation (Swagger/ReDoc)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── user_router.py
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/                  # Database setup
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── user_service.py
├── tests/                   # Test files
│   └── __init__.py
├── main.py                  # Application entry point
├── .env.example             # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md

```

## Prerequisites

- Python 3.10+
- PostgreSQL 12+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-ordering
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from template:
```bash
cp .env.example .env
```

5. Update `.env` with your configuration:
```env
DATABASE_URL="postgresql://username:password@localhost/database_name"
```

6. Create PostgreSQL database:
```bash
createdb ordering_db
```

## Running the Application

### Development Mode
```bash
uvicorn main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Root
- `GET /` - Welcome message
- `GET /health` - Health check

### Users (prefix: /api/v1/users)
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID

## Development

### Adding a New Model

1. Create model file in `app/models/`
2. Create schema file in `app/schemas/`
3. Create service file in `app/services/`
4. Create router file in `app/api/`
5. Register router in `main.py`

### Code Style

This project follows:
- PEP 8 style guide
- Type hints for better code quality
- Docstrings for documentation

## Testing

```bash
pytest
```

## Environment Variables

See `.env.example` for all available configuration options.

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | FastAPI Ordering System |
| APP_VERSION | Application version | 1.0.0 |
| DEBUG | Debug mode | True |
| DATABASE_URL | PostgreSQL connection string | - |
| CORS_ORIGINS | Allowed CORS origins | ["http://localhost:3000"] |
| API_V1_PREFIX | API version 1 prefix | /api/v1 |

## License

MIT License

## Author

Mek Chawanwit
# fastapi-ordering
