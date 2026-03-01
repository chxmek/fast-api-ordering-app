# FastAPI Restaurant Ordering System Backend

A complete, production-ready REST API for a restaurant ordering system. Built with FastAPI, SQLAlchemy, and PostgreSQL.

## 📋 Overview

This backend provides comprehensive API endpoints for:
- ✅ Menu management (items, categories, options)
- ✅ Customizable menu options (sweetness, spiciness, etc.)
- ✅ Price modifiers for choices
- ✅ Order management with real-time status tracking
- ✅ Automatic stock management and inventory control
- ✅ RESTful API with full documentation
- ✅ CORS support for Flutter frontend
- ✅ Comprehensive error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL or SQLite
- pip

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 Documentation

### Main Guides
- [**API Setup Guide**](API_SETUP_GUIDE.md) - Comprehensive setup and usage guide
- [**Flutter Integration Guide**](FLUTTER_INTEGRATION.md) - How to integrate with Flutter app
- [**API Endpoints Reference**](API_ENDPOINTS.md) - Detailed endpoint documentation

### Quick Reference

#### Menu Items
```
GET    /api/v1/menu/items               # Get all items
GET    /api/v1/menu/items/{id}          # Get specific item
POST   /api/v1/menu/items               # Create item
PUT    /api/v1/menu/items/{id}          # Update item
DELETE /api/v1/menu/items/{id}          # Delete item
```

#### Orders
```
GET    /api/v1/orders                   # Get all orders
GET    /api/v1/orders/{id}              # Get specific order
POST   /api/v1/orders                   # Create order
PUT    /api/v1/orders/{id}              # Update order
DELETE /api/v1/orders/{id}              # Delete order (restore stock)
POST   /api/v1/orders/{id}/cancel       # Cancel order
POST   /api/v1/orders/{id}/complete     # Complete order
```

#### Menu Options
```
GET    /api/v1/menu/options             # Get all options
POST   /api/v1/menu/options             # Create option
PUT    /api/v1/menu/options/{id}        # Update option
DELETE /api/v1/menu/options/{id}        # Delete option
```

## 🏗️ Project Structure

```
fastapi-ordering/
├── app/
│   ├── api/                    # API routers
│   │   ├── __init__.py
│   │   ├── menu_router.py      # Menu management endpoints
│   │   ├── orders_router.py    # Order endpoints
│   │   └── user_router.py      # User endpoints
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── menu.py             # Menu items, options, choices
│   │   ├── order.py            # Orders and order items
│   │   └── user.py             # User model
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── menu.py             # Menu schemas
│   │   ├── order.py            # Order schemas
│   │   └── user.py             # User schemas
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── menu_service.py     # Menu operations
│   │   ├── order_service.py    # Order operations
│   │   └── user_service.py     # User operations
│   ├── db/                     # Database config
│   │   ├── __init__.py
│   │   └── database.py
│   └── core/                   # Core configurations
│       ├── __init__.py
│       ├── config.py           # Settings
│       ├── exceptions.py       # Exception handlers
│       ├── logging.py          # Logging setup
│       └── middleware.py       # Middleware
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   └── test_users.py
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables example
├── API_SETUP_GUIDE.md          # Setup guide
├── FLUTTER_INTEGRATION.md      # Flutter integration guide
├── API_ENDPOINTS.md            # Endpoints reference
└── seed_data.py                # Sample data seeder
```

## 🗄️ Database Schema

### Menu Items Table
```sql
CREATE TABLE menu_items (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL,
  price FLOAT NOT NULL,
  description TEXT,
  image_url VARCHAR(500),
  is_available BOOLEAN DEFAULT TRUE,
  stock_quantity INTEGER,  -- NULL = unlimited
  prep_time INTEGER,       -- minutes
  is_recommended BOOLEAN DEFAULT FALSE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Menu Options Table
```sql
CREATE TABLE menu_options (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  option_type VARCHAR(50) DEFAULT 'single',  -- 'single' or 'multiple'
  is_required BOOLEAN DEFAULT FALSE,
  min_selection INTEGER,
  max_selection INTEGER,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Option Choices Table
```sql
CREATE TABLE option_choices (
  id SERIAL PRIMARY KEY,
  menu_option_id INTEGER NOT NULL REFERENCES menu_options(id),
  name VARCHAR(255) NOT NULL,
  price_modifier FLOAT DEFAULT 0,
  is_default BOOLEAN DEFAULT FALSE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table
```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  total FLOAT NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'completed', 'cancelled'
  table_number INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Order Items Table
```sql
CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id),
  menu_item_id INTEGER NOT NULL REFERENCES menu_items(id),
  name VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  price FLOAT NOT NULL,
  options_text TEXT,    -- Text description of selected options
  remark TEXT,          -- Customer notes
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```env
# Application
APP_NAME=RestaurantHub API
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/restaurant_db
# or SQLite: sqlite:///./restaurant.db

# CORS
CORS_ORIGINS=["http://localhost:8081","http://localhost:3000","*"]

# API
API_V1_PREFIX=/api/v1
```

## 📦 Features

### Menu Management
- Create/read/update/delete menu items
- Categorize items
- Set availability and stock quantities
- Mark items as recommended
- Control display order
- Add multiple customization options to items

### Customization Options
- Create single-select options (e.g., Sweetness Level)
- Create multi-select options (e.g., Toppings)
- Set required vs optional options
- Add price modifiers for choices
- Set default choices

### Order Management
- Create orders with multiple items
- Automatic stock reduction
- Order status tracking (pending → completed)
- Cancel orders with stock restoration
- Track order creation and update times
- Store customer remarks and special requests

### Stock Management
- Track stock quantity per item
- Automatic reduction on order creation
- Validation before order acceptance
- Automatic restoration on order cancellation
- Support for unlimited stock items (NULL)

## 🧪 Testing

Run tests:
```bash
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_menu.py
```

## 📊 Sample Data

Load sample data:
```bash
python seed_data.py
```

This creates:
- 3 menu options (Sweetness, Spice, Protein)
- 7 menu items with full details
- 2 sample orders for testing

## 🐳 Docker

Build and run with Docker:
```bash
docker-compose up --build
```

Access at: http://localhost:8000

Stop containers:
```bash
docker-compose down
```

## 🔐 Security Considerations

- Add authentication (JWT tokens) for future enhancements
- Implement role-based access control (admin, staff, user)
- Add rate limiting
- Validate all inputs
- Use HTTPS in production
- Never commit `.env` with real credentials

## 📈 Performance

- Database indexes on frequently queried fields
- Connection pooling
- Pagination support for list endpoints
- Efficient query filtering

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in .env
- [ ] Use environment-appropriate database (PostgreSQL recommended)
- [ ] Set proper `CORS_ORIGINS`
- [ ] Use environment variables for secrets
- [ ] Run migrations
- [ ] Set up proper logging
- [ ] Configure backups
- [ ] Use reverse proxy (nginx)
- [ ] Set up SSL/TLS certificates

### Deployment Command
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## 🤝 Integration with Flutter

The Flutter app can communicate with this API by:

1. Setting base URL to API endpoint
2. Sending menu preferences as `options_text`
3. Including customer remarks in order items
4. Handling order status updates
5. Managing cart locally with synced API data

See [FLUTTER_INTEGRATION.md](FLUTTER_INTEGRATION.md) for detailed implementation.

## 📝 API Example

### Create Menu Item with Options
```bash
curl -X POST http://localhost:8000/api/v1/menu/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Thai Green Curry",
    "category": "Curry",
    "price": 150.0,
    "description": "Spicy green curry",
    "is_available": true,
    "stock_quantity": 50,
    "prep_time": 15,
    "is_recommended": true,
    "option_ids": [1, 2]
  }'
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 5,
    "total": 300.0,
    "items": [{
      "menu_item_id": 1,
      "name": "Pad Thai",
      "quantity": 2,
      "price": 120.0,
      "options_text": "Sweetness: Normal, Spice: Medium",
      "remark": "No peanuts"
    }]
  }'
```

## 🐛 Troubleshooting

### Database Connection Error
Check DATABASE_URL in .env and ensure server is running

### Port Already in Use
```bash
uvicorn main:app --port 8001
```

### CORS Errors
Add your client URL to CORS_ORIGINS in .env

### Import Errors
Make sure all requirements are installed:
```bash
pip install -r requirements.txt
```

## 📞 Support & Contributions

For issues, questions, or contributions, please refer to the documentation files.

## 📄 License

This project is part of the RestaurantHub ordering system.

## ✨ Future Enhancements

- [ ] User authentication and profiles
- [ ] Payment processing integration
- [ ] Real-time order updates with WebSocket
- [ ] Advanced analytics and reporting
- [ ] Admin dashboard
- [ ] Email/SMS notifications
- [ ] Kitchen display system
- [ ] Delivery tracking
- [ ] Loyalty program
- [ ] Multi-restaurant support
