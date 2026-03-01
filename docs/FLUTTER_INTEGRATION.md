# Flutter to FastAPI Integration Guide

## Quick Start

This guide shows how to integrate your Flutter application with the FastAPI backend.

## 1. API Base URL Configuration

In your Flutter app, update the API base URL to point to the backend:

```dart
// lib/constants/api_constants.dart (or similar)
const String API_BASE_URL = 'http://localhost:8000/api/v1';

// For different environments:
const String API_BASE_URL_DEV = 'http://localhost:8000/api/v1';
const String API_BASE_URL_PROD = 'https://your-api-domain.com/api/v1';
```

## 2. Update Menu Repository

Update your `MenuRepository` to call the FastAPI backend:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class MenuRepository {
  final String baseUrl = 'http://localhost:8000/api/v1';

  Future<List<MenuItemModel>> fetchMenuItems() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/menu/items'));
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data
            .map((item) => MenuItemModel.fromJson(item))
            .toList();
      } else {
        throw Exception('Failed to load menu items');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<int> createOrder(List<CartItem> cartItems) async {
    try {
      final orderData = {
        'table_number': null, // Set as needed
        'total': _calculateTotal(cartItems),
        'items': cartItems.map((item) => {
          'menu_item_id': item.menuItem.id,
          'name': item.menuItem.name,
          'quantity': 1, // Update quantity logic as needed
          'price': item.menuItem.price,
          'options_text': item.optionsText,
          'remark': item.remark,
        }).toList(),
      };

      final response = await http.post(
        Uri.parse('$baseUrl/orders'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(orderData),
      );

      if (response.statusCode == 201) {
        final order = json.decode(response.body);
        return order['id'] as int;
      } else {
        throw Exception('Failed to create order');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<List<OrderModel>> fetchOrders() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/orders'));
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data
            .map((order) => OrderModel.fromJson(order))
            .toList();
      } else {
        throw Exception('Failed to load orders');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<void> deleteOrder(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/orders/$id'),
      );
      
      if (response.statusCode != 204) {
        throw Exception('Failed to delete order');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<int> setOrderStatus(int id, String status) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/orders/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'status': status}),
      );
      
      if (response.statusCode == 200) {
        final order = json.decode(response.body);
        return order['id'] as int;
      } else {
        throw Exception('Failed to update order');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  double _calculateTotal(List<CartItem> cartItems) {
    return cartItems.fold(0, (total, item) {
      return total + (item.menuItem.price * 1); // Adjust quantity as needed
    });
  }
}
```

## 3. Update Models

Update your Flutter models to match the API response format:

```dart
// Update fromMap to handle API JSON responses
class MenuItemModel {
  // ... existing fields

  factory MenuItemModel.fromJson(Map<String, dynamic> json) => MenuItemModel(
    id: json['id'] as int,
    name: json['name'] as String,
    category: json['category'] as String,
    price: (json['price'] as num).toDouble(),
    imageUrl: json['image_url'] as String?,
    description: json['description'] as String?,
    isAvailable: json['is_available'] as bool? ?? true,
    stockQuantity: json['stock_quantity'] as int?,
    prepTime: json['prep_time'] as int?,
    isRecommended: json['is_recommended'] as bool? ?? false,
    displayOrder: json['display_order'] as int? ?? 0,
    options: (json['options'] as List<dynamic>?)
        ?.map((option) => MenuOption.fromJson(option as Map<String, dynamic>))
        .toList() ?? [],
  );

  static Future<Map<String, dynamic>> toJson(MenuItemModel item) async {
    return {
      'id': item.id,
      'name': item.name,
      'category': item.category,
      'price': item.price,
      'image_url': item.imageUrl,
      'description': item.description,
      'is_available': item.isAvailable,
      'stock_quantity': item.stockQuantity,
      'prep_time': item.prepTime,
      'is_recommended': item.isRecommended,
      'display_order': item.displayOrder,
    };
  }
}
```

## 4. API Response Examples

### Get Menu Items

```bash
curl http://localhost:8000/api/v1/menu/items
```

Response:
```json
[
  {
    "id": 1,
    "name": "Pad Thai",
    "category": "Noodles",
    "price": 120.0,
    "description": "Stir-fried rice noodles...",
    "image_url": "https://...",
    "is_available": true,
    "stock_quantity": 50,
    "prep_time": 10,
    "is_recommended": true,
    "display_order": 1,
    "options": [
      {
        "id": 1,
        "name": "Sweetness Level",
        "description": "Choose your sweetness...",
        "option_type": "single",
        "is_required": true,
        "min_selection": null,
        "max_selection": null,
        "display_order": 1,
        "choices": [
          {
            "id": 1,
            "menu_option_id": 1,
            "name": "Not Sweet",
            "price_modifier": 0.0,
            "is_default": false,
            "display_order": 0
          }
        ]
      }
    ]
  }
]
```

### Create Order

```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 5,
    "total": 250.0,
    "items": [
      {
        "menu_item_id": 1,
        "name": "Pad Thai",
        "quantity": 1,
        "price": 120.0,
        "options_text": "Sweetness: Normal, Spice: Medium",
        "remark": "No peanuts"
      }
    ]
  }'
```

Response:
```json
{
  "id": 1,
  "total": 250.0,
  "status": "pending",
  "table_number": 5,
  "created_at": "2024-02-23T10:30:00",
  "updated_at": "2024-02-23T10:30:00",
  "items": [...]
}
```

## 5. Handle Network Errors

Add proper error handling in your BLoC:

```dart
class MenuBloc extends Bloc<MenuEvent, MenuState> {
  final MenuRepository repository;

  MenuBloc({required this.repository}) : super(MenuInitial()) {
    on<LoadMenu>(_onLoadMenu);
  }

  Future<void> _onLoadMenu(LoadMenu event, Emitter<MenuState> emit) async {
    emit(MenuLoading());
    try {
      final items = await repository.fetchMenuItems();
      emit(MenuLoaded(items));
    } catch (e) {
      emit(MenuError(e.toString()));
    }
  }
}
```

## 6. Running the Stack

### Terminal 1: Start FastAPI Backend

```bash
cd back-end/fastapi-ordering
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Terminal 2: Seed Sample Data (Optional)

```bash
cd back-end/fastapi-ordering
pip install requests
python seed_data.py
```

### Terminal 3: Run Flutter App

```bash
cd front-end/ordering_app
flutter run
```

## 7. Testing with cURL

### Get all menu items by category

```bash
curl "http://localhost:8000/api/v1/menu/items?category=Noodles"
```

### Get specific menu item

```bash
curl http://localhost:8000/api/v1/menu/items/1
```

### Get all orders with status filter

```bash
curl "http://localhost:8000/api/v1/orders?status=pending"
```

### Cancel an order

```bash
curl -X POST http://localhost:8000/api/v1/orders/1/cancel
```

### Complete an order

```bash
curl -X POST http://localhost:8000/api/v1/orders/1/complete
```

### Get order statistics

```bash
curl http://localhost:8000/api/v1/orders/summary/statistics
```

## 8. Environment Configuration

Create a `.env` file in the FastAPI project:

```env
# Application
APP_NAME=RestaurantHub API
APP_VERSION=1.0.0
DEBUG=True

# Database (SQLite for development)
DATABASE_URL=sqlite:///./restaurant.db

# Or PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/restaurant_db

# CORS
CORS_ORIGINS=["http://localhost:8081","http://localhost:3000","*"]

# API
API_V1_PREFIX=/api/v1
```

## 9. Troubleshooting

### Connection Refused
Make sure the FastAPI server is running: `uvicorn main:app --reload`

### CORS Errors
Check that your Flutter app URL is in the `CORS_ORIGINS` list in `.env`

### Stock Error
If you get "insufficient stock" error, the menu item doesn't have enough quantity

### Database Error
For SQLite, ensure you have permissions to create `restaurant.db` in the project directory

## 10. Next Steps

1. Implement authentication (JWT tokens)
2. Add payment processing
3. Implement WebSocket for real-time order updates
4. Add image upload functionality
5. Create admin dashboard
6. Add analytics and reporting

For more detailed API documentation, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
