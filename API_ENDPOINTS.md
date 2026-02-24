# API Endpoints Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Menu Items Endpoints

### GET /menu/items
Get all menu items with optional filtering

**Query Parameters:**
- `category` (optional): Filter by category name
- `skip` (optional): Number of items to skip (default: 0)
- `limit` (optional): Number of items to return (default: 100)

**Example:**
```bash
GET /menu/items?category=Curry&skip=0&limit=10
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Green Curry",
    "category": "Curry",
    "price": 150.0,
    "description": "...",
    "image_url": "...",
    "is_available": true,
    "stock_quantity": 50,
    "prep_time": 15,
    "is_recommended": true,
    "display_order": 1,
    "options": [...]
  }
]
```

---

### GET /menu/items/{item_id}
Get a specific menu item

**Path Parameters:**
- `item_id` (required): Integer

**Example:**
```bash
GET /menu/items/1
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Green Curry",
  ...
}
```

---

### POST /menu/items
Create a new menu item

**Request Body:**
```json
{
  "name": "Thai Green Curry",
  "category": "Curry",
  "price": 150.0,
  "description": "Spicy green curry",
  "image_url": "https://example.com/image.jpg",
  "is_available": true,
  "stock_quantity": 50,
  "prep_time": 15,
  "is_recommended": true,
  "display_order": 1,
  "option_ids": [1, 2]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Thai Green Curry",
  ...
}
```

---

### PUT /menu/items/{item_id}
Update a menu item

**Path Parameters:**
- `item_id` (required): Integer

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Name",
  "price": 160.0,
  "is_available": false,
  "stock_quantity": 30
}
```

**Response:** `200 OK`

---

### DELETE /menu/items/{item_id}
Delete a menu item

**Path Parameters:**
- `item_id` (required): Integer

**Response:** `204 No Content`

---

### GET /menu/categories
Get all menu categories

**Example:**
```bash
GET /menu/categories
```

**Response:** `200 OK`
```json
["Curry", "Noodles", "Soups", "Appetizers", "Salads"]
```

---

## Menu Options Endpoints

### GET /menu/options
Get all menu options

**Query Parameters:**
- `skip` (optional): Default: 0
- `limit` (optional): Default: 100

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Sweetness Level",
    "description": "...",
    "option_type": "single",
    "is_required": true,
    "min_selection": null,
    "max_selection": null,
    "display_order": 1,
    "choices": [...]
  }
]
```

---

### GET /menu/options/{option_id}
Get a specific menu option

**Path Parameters:**
- `option_id` (required): Integer

**Response:** `200 OK`

---

### POST /menu/options
Create a new menu option

**Request Body:**
```json
{
  "name": "Sweetness Level",
  "description": "Choose your sweetness",
  "option_type": "single",
  "is_required": true,
  "min_selection": null,
  "max_selection": null,
  "display_order": 1,
  "choices": [
    {
      "name": "Not Sweet",
      "price_modifier": 0,
      "is_default": false,
      "display_order": 0
    },
    {
      "name": "Normal",
      "price_modifier": 0,
      "is_default": true,
      "display_order": 1
    }
  ]
}
```

**Response:** `201 Created`

---

### PUT /menu/options/{option_id}
Update a menu option

**Path Parameters:**
- `option_id` (required): Integer

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Name",
  "is_required": false
}
```

**Response:** `200 OK`

---

### DELETE /menu/options/{option_id}
Delete a menu option

**Path Parameters:**
- `option_id` (required): Integer

**Response:** `204 No Content`

---

## Option Choices Endpoints

### POST /menu/options/{option_id}/choices
Add a choice to an option

**Path Parameters:**
- `option_id` (required): Integer

**Request Body:**
```json
{
  "name": "Extra Sweet",
  "price_modifier": 10,
  "is_default": false,
  "display_order": 3
}
```

**Response:** `201 Created`
```json
{
  "id": 4,
  "menu_option_id": 1,
  "name": "Extra Sweet",
  "price_modifier": 10,
  "is_default": false,
  "display_order": 3
}
```

---

### PUT /menu/choices/{choice_id}
Update an option choice

**Path Parameters:**
- `choice_id` (required): Integer

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Name",
  "price_modifier": 20
}
```

**Response:** `200 OK`

---

### DELETE /menu/choices/{choice_id}
Delete an option choice

**Path Parameters:**
- `choice_id` (required): Integer

**Response:** `204 No Content`

---

## Orders Endpoints

### GET /orders
Get all orders with optional filtering

**Query Parameters:**
- `status` (optional): "pending", "completed", "cancelled"
- `skip` (optional): Default: 0
- `limit` (optional): Default: 100

**Example:**
```bash
GET /orders?status=pending&skip=0&limit=10
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "total": 300.0,
    "status": "pending",
    "table_number": 5,
    "created_at": "2024-02-23T10:30:00",
    "updated_at": "2024-02-23T10:30:00",
    "items": [...]
  }
]
```

---

### GET /orders/{order_id}
Get a specific order

**Path Parameters:**
- `order_id` (required): Integer

**Response:** `200 OK`

---

### POST /orders
Create a new order

**Request Body:**
```json
{
  "table_number": 5,
  "total": 300.0,
  "items": [
    {
      "menu_item_id": 1,
      "name": "Pad Thai",
      "quantity": 2,
      "price": 120.0,
      "options_text": "Sweetness: Normal, Spice: Medium",
      "remark": "No peanuts"
    },
    {
      "menu_item_id": 2,
      "name": "Tom Yum",
      "quantity": 1,
      "price": 100.0,
      "options_text": "Spice: Hot",
      "remark": ""
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "total": 300.0,
  "status": "pending",
  ...
}
```

**Error Cases:**
- `400`: Menu item not found
- `400`: Menu item not available
- `400`: Insufficient stock

---

### PUT /orders/{order_id}
Update an order

**Path Parameters:**
- `order_id` (required): Integer

**Request Body:** (all fields optional)
```json
{
  "status": "completed",
  "table_number": 6
}
```

**Response:** `200 OK`

---

### DELETE /orders/{order_id}
Delete an order (stock is restored)

**Path Parameters:**
- `order_id` (required): Integer

**Response:** `204 No Content`

---

### POST /orders/{order_id}/cancel
Cancel an order (stock is restored)

**Path Parameters:**
- `order_id` (required): Integer

**Request Body:** Empty

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "cancelled",
  ...
}
```

**Error Cases:**
- `400`: Order already cancelled
- `400`: Order already completed

---

### POST /orders/{order_id}/complete
Mark an order as completed

**Path Parameters:**
- `order_id` (required): Integer

**Request Body:** Empty

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "completed",
  ...
}
```

**Error Cases:**
- `400`: Order already completed
- `400`: Order is cancelled

---

### GET /orders/summary/statistics
Get order statistics

**Example:**
```bash
GET /orders/summary/statistics
```

**Response:** `200 OK`
```json
{
  "total_orders": 25,
  "completed_orders": 20,
  "pending_orders": 3,
  "cancelled_orders": 2
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Successful GET/PUT |
| 201 | Created - Successful POST |
| 204 | No Content - Successful DELETE |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Error Response Format

```json
{
  "detail": "Error message here"
}
```

---

## Example cURL Commands

### Create menu item
```bash
curl -X POST http://localhost:8000/api/v1/menu/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pad Thai",
    "category": "Noodles",
    "price": 120.0
  }'
```

### Create order
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 5,
    "total": 120.0,
    "items": [{
      "menu_item_id": 1,
      "name": "Pad Thai",
      "quantity": 1,
      "price": 120.0
    }]
  }'
```

### Get pending orders
```bash
curl "http://localhost:8000/api/v1/orders?status=pending"
```

### Complete an order
```bash
curl -X POST http://localhost:8000/api/v1/orders/1/complete
```

### Cancel an order
```bash
curl -X POST http://localhost:8000/api/v1/orders/1/cancel
```
