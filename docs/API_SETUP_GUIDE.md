# FastAPI Restaurant Ordering System - Setup & Usage Guide

## Overview

This is a complete backend API for a Flutter-based restaurant ordering system. It provides comprehensive endpoints for managing menu items, options, choices, and orders with stock management.

## Features

- **Menu Management**: Create, read, update, delete menu items with categories
- **Menu Options**: Manage customizable options (e.g., Sweetness Level, Spiciness)
- **Option Choices**: Add choices for each option with price modifiers
- **Order Management**: Create orders, track status, manage inventory
- **Stock Management**: Automatic stock reduction on order creation and restoration on cancellation
- **RESTful API**: Full REST API with proper error handling and validation

## Prerequisites

- Python 3.9+
- PostgreSQL (or SQLite for development)
- pip

## Installation

### 1. Clone the repository and navigate to backend directory

```bash
cd back-end/fastapi-ordering
```

### 2. Create a virtual environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Application
APP_NAME=RestaurantHub API
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/restaurant_db
# For SQLite (development):
# DATABASE_URL=sqlite:///./restaurant.db

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8081","*"]

# API
API_V1_PREFIX=/api/v1
```

### 5. Initialize the database

The database tables will be created automatically when the application starts.

## Running the Application

### Development

```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using make if available
make run
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: **http://localhost:8000**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Menu Items

```
GET    /api/v1/menu/items               - Get all menu items
GET    /api/v1/menu/items/{item_id}     - Get specific menu item
POST   /api/v1/menu/items               - Create menu item
PUT    /api/v1/menu/items/{item_id}     - Update menu item
DELETE /api/v1/menu/items/{item_id}     - Delete menu item
GET    /api/v1/menu/categories          - Get all categories
```

#### Create Menu Item Example

```json
POST /api/v1/menu/items
{
  "name": "Thai Green Curry",
  "category": "Curry",
  "price": 150.00,
  "description": "Spicy green curry with chicken",
  "image_url": "https://...",
  "is_available": true,
  "stock_quantity": 50,
  "prep_time": 15,
  "is_recommended": true,
  "display_order": 1,
  "option_ids": [1, 2]
}
```

#### Response

```json
{
  "id": 1,
  "name": "Thai Green Curry",
  "category": "Curry",
  "price": 150.0,
  "description": "Spicy green curry with chicken",
  "image_url": "https://...",
  "is_available": true,
  "stock_quantity": 50,
  "prep_time": 15,
  "is_recommended": true,
  "display_order": 1,
  "options": [...]
}
```

### Menu Options

```
GET    /api/v1/menu/options                          - Get all options
GET    /api/v1/menu/options/{option_id}              - Get specific option
POST   /api/v1/menu/options                          - Create option
PUT    /api/v1/menu/options/{option_id}              - Update option
DELETE /api/v1/menu/options/{option_id}              - Delete option
POST   /api/v1/menu/options/{option_id}/choices      - Add choice to option
PUT    /api/v1/menu/choices/{choice_id}              - Update choice
DELETE /api/v1/menu/choices/{choice_id}              - Delete choice
```

#### Create Menu Option Example

```json
POST /api/v1/menu/options
{
  "name": "Sweetness Level",
  "description": "Choose your preferred sweetness",
  "option_type": "single",
  "is_required": true,
  "display_order": 1,
  "choices": [
    {
      "name": "ไม่หวาน (Not Sweet)",
      "price_modifier": 0,
      "is_default": false,
      "display_order": 0
    },
    {
      "name": "หวานน้อย (Less Sweet)",
      "price_modifier": 0,
      "is_default": true,
      "display_order": 1
    },
    {
      "name": "หวานกำลังดี (Normal)",
      "price_modifier": 0,
      "is_default": false,
      "display_order": 2
    },
    {
      "name": "หวานมาก (Extra Sweet)",
      "price_modifier": 0,
      "is_default": false,
      "display_order": 3
    }
  ]
}
```

### Orders

```
GET    /api/v1/orders                  - Get all orders
GET    /api/v1/orders/{order_id}       - Get specific order
POST   /api/v1/orders                  - Create order
PUT    /api/v1/orders/{order_id}       - Update order
DELETE /api/v1/orders/{order_id}       - Delete order (restore stock)
POST   /api/v1/orders/{order_id}/cancel   - Cancel order
POST   /api/v1/orders/{order_id}/complete - Complete order
GET    /api/v1/orders/summary/statistics  - Get order statistics
```

#### Create Order Example

```json
POST /api/v1/orders
{
  "table_number": 5,
  "total": 300.00,
  "items": [
    {
      "menu_item_id": 1,
      "name": "Thai Green Curry",
      "quantity": 2,
      "price": 150.00,
      "options_text": "Sweetness: Not Sweet, Spice: Medium",
      "remark": "Less oil please"
    },
    {
      "menu_item_id": 2,
      "name": "Pad Thai",
      "quantity": 1,
      "price": 120.00,
      "options_text": "Protein: Shrimp",
      "remark": ""
    }
  ]
}
```

#### Response

```json
{
  "id": 1,
  "total": 300.0,
  "status": "pending",
  "table_number": 5,
  "created_at": "2024-02-23T10:30:00",
  "updated_at": "2024-02-23T10:30:00",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "menu_item_id": 1,
      "name": "Thai Green Curry",
      "quantity": 2,
      "price": 150.0,
      "options_text": "Sweetness: Not Sweet, Spice: Medium",
      "remark": "Less oil please"
    }
  ]
}
```

#### Order Status Flow

- **pending**: Initial state when order is created
- **completed**: Order has been prepared and served
- **cancelled**: Order has been cancelled

## Stock Management

### Automatic Stock Reduction

When an order is created, the stock for each menu item is automatically reduced by the order quantity. If an item doesn't have enough stock, the order creation will be rejected.

### Stock Restoration

Stock is automatically restored when:
1. An order is deleted (DELETE endpoint)
2. An order is cancelled (POST /cancel endpoint)

### Manual Stock Update

You can update stock quantity for menu items using the PUT endpoint.

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: OK - Successful GET/PUT/POST request
- **201**: Created - Successful POST request
- **204**: No Content - Successful DELETE request
- **400**: Bad Request - Invalid data or insufficient stock
- **404**: Not Found - Resource doesn't exist
- **500**: Internal Server Error

### Error Response Example

```json
{
  "detail": "Menu item not found"
}
```

## Testing

Run the test suite:

```bash
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_users.py
```

## Docker Setup

### Build and run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at: http://localhost:8000

### Stop the containers

```bash
docker-compose down
```

## Database Schema

The database includes the following tables:

- **users**: User accounts (for future authentication)
- **menu_items**: Restaurant menu items
- **menu_options**: Customizable options for menu items
- **option_choices**: Choices for each option
- **menu_item_options**: Relationship between menu items and options
- **orders**: Customer orders
- **order_items**: Items within each order

## Integration with Flutter Frontend

The Flutter app communicates with this API by:

1. Making HTTP requests to the endpoints
2. Sending menu preferences as order items with `options_text`
3. Handling customer remarks in the `remark` field
4. Tracking order status from the response

## Environment Configuration

Key configuration options in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | False |
| `DATABASE_URL` | Database connection string | Required |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] |
| `API_V1_PREFIX` | API version 1 prefix | /api/v1 |

## Troubleshooting

### Port 8000 Already in Use

```bash
# Change port
uvicorn main:app --port 8001
```

### Database Connection Error

Check your `DATABASE_URL` in `.env` file and ensure the database server is running.

### CORS Errors

Add the frontend URL to `CORS_ORIGINS` in `.env`:

```env
CORS_ORIGINS=["http://localhost:8081","http://your-app-url.com"]
```

## Future Enhancements

- User authentication and authorization
- Payment processing integration
- Real-time order updates with WebSocket
- Analytics and reporting
- Admin dashboard
- Email notifications

## Support

For issues or questions, please refer to the documentation or create an issue in the repository.
