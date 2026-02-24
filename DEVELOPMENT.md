# Development Guide

## Project Structure Explained

### `app/` - Main Application Directory
Main application code organized by functionality.

### `app/api/` - API Routes
Contains all API endpoint definitions (routers).
- Each module represents a resource (users, orders, etc.)
- Uses FastAPI's APIRouter for modular routing

### `app/core/` - Core Configuration
Application configuration and settings.
- `config.py` - Environment-based configuration using pydantic-settings
- `exceptions.py` - Custom exception classes and handlers
- `logging.py` - Logging setup and configuration
- `middleware.py` - Custom middleware functions

### `app/db/` - Database Layer
Database connection and session management.
- `database.py` - SQLAlchemy engine and session setup

### `app/models/` - Database Models
SQLAlchemy ORM models representing database tables.
- Each file represents a table/entity
- Uses SQLAlchemy declarative base

### `app/schemas/` - Pydantic Schemas
Request/response validation and serialization.
- Input validation schemas (e.g., `UserCreate`)
- Output response schemas (e.g., `UserResponse`)

### `app/services/` - Business Logic
Service layer containing business logic.
- Separates business logic from API routes
- Handles data processing and database operations

### `tests/` - Test Suite
Test files using pytest.
- `conftest.py` - Test configuration and fixtures
- Test files follow naming convention `test_*.py`

## Development Workflow

### 1. Adding a New Feature

Example: Adding a "Products" feature

#### Step 1: Create the Model
```python
# app/models/product.py
from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
```

#### Step 2: Create the Schemas
```python
# app/schemas/product.py
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True
```

#### Step 3: Create the Service
```python
# app/services/product_service.py
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
```

#### Step 4: Create the Router
```python
# app/api/product_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)
```

#### Step 5: Register the Router
```python
# main.py
from app.api import product_router

app.include_router(product_router.router, prefix=settings.API_V1_PREFIX)
```

### 2. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py

# Run with verbose output
pytest -v
```

### 3. Database Migrations

For production, use Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add products table"

# Apply migration
alembic upgrade head
```

### 4. Code Style

Follow PEP 8 and use these tools:

```bash
# Format code
black app/

# Sort imports
isort app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Application
APP_NAME="FastAPI Ordering System"
APP_VERSION="1.0.0"
DEBUG=True

# Database
DATABASE_URL="postgresql://username:password@localhost/database_name"

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# API
API_V1_PREFIX="/api/v1"
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Manual Docker Build

```bash
# Build image
docker build -t fastapi-ordering .

# Run container
docker run -p 8000:8000 --env-file .env fastapi-ordering
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Best Practices

1. **Separation of Concerns**
   - Keep routes thin - delegate to services
   - Services handle business logic
   - Models represent database tables only

2. **Error Handling**
   - Use custom exceptions from `app/core/exceptions.py`
   - Let exception handlers format responses

3. **Type Hints**
   - Always use type hints for better IDE support
   - Helps catch errors early

4. **Documentation**
   - Add docstrings to all functions and classes
   - Keep README up to date

5. **Testing**
   - Write tests for all new features
   - Aim for >80% code coverage

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Test connection
psql -U username -d database_name
```

### Import Errors
- Ensure virtual environment is activated
- Check PYTHONPATH includes project root

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
