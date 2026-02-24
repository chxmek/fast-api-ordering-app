"""
Script to seed sample data into the database for testing and development.
Run this script after the API is running to populate the database with sample menu items and orders.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def seed_menu_options():
    """Create menu options (customizations) for menu items."""
    print("Creating menu options...")

    # Sweetness Level Option
    sweetness_option = {
        "name": "Sweetness Level",
        "description": "Choose your preferred sweetness level",
        "option_type": "single",
        "is_required": True,
        "display_order": 1,
        "choices": [
            {
                "name": "ไม่หวาน (Not Sweet)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 0,
            },
            {
                "name": "หวานน้อย (Less Sweet)",
                "price_modifier": 0,
                "is_default": True,
                "display_order": 1,
            },
            {
                "name": "หวานกำลังดี (Normal)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 2,
            },
            {
                "name": "หวานมาก (Extra Sweet)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 3,
            },
        ],
    }

    response = requests.post(f"{BASE_URL}/menu/options", json=sweetness_option)
    sweetness_id = response.json()["id"] if response.status_code == 201 else 1
    print(f"✓ Sweetness option created (ID: {sweetness_id})")

    # Spiciness Level Option
    spice_option = {
        "name": "Spiciness Level",
        "description": "Choose your preferred spice level",
        "option_type": "single",
        "is_required": True,
        "display_order": 2,
        "choices": [
            {
                "name": "ไม่เผ็ด (Not Spicy)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 0,
            },
            {
                "name": "เผ็ดน้อย (Mild)",
                "price_modifier": 0,
                "is_default": True,
                "display_order": 1,
            },
            {
                "name": "เผ็ดกำลังดี (Medium)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 2,
            },
            {
                "name": "เผ็ดมาก (Hot)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 3,
            },
            {
                "name": "เผ็ดมากๆ (Very Hot)",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 4,
            },
        ],
    }

    response = requests.post(f"{BASE_URL}/menu/options", json=spice_option)
    spice_id = response.json()["id"] if response.status_code == 201 else 2
    print(f"✓ Spiciness option created (ID: {spice_id})")

    # Protein Option (Multiple Choice)
    protein_option = {
        "name": "Protein",
        "description": "Choose your protein",
        "option_type": "single",
        "is_required": False,
        "display_order": 3,
        "choices": [
            {
                "name": "Chicken",
                "price_modifier": 0,
                "is_default": True,
                "display_order": 0,
            },
            {
                "name": "Pork",
                "price_modifier": 10,
                "is_default": False,
                "display_order": 1,
            },
            {
                "name": "Shrimp",
                "price_modifier": 20,
                "is_default": False,
                "display_order": 2,
            },
            {
                "name": "Fish",
                "price_modifier": 20,
                "is_default": False,
                "display_order": 3,
            },
            {
                "name": "Vegetarian",
                "price_modifier": 0,
                "is_default": False,
                "display_order": 4,
            },
        ],
    }

    response = requests.post(f"{BASE_URL}/menu/options", json=protein_option)
    protein_id = response.json()["id"] if response.status_code == 201 else 3
    print(f"✓ Protein option created (ID: {protein_id})")

    return [sweetness_id, spice_id, protein_id]


def seed_menu_items(option_ids):
    """Create menu items."""
    print("\nCreating menu items...")

    menu_items = [
        {
            "name": "Pad Thai",
            "category": "Noodles",
            "price": 120.0,
            "description": "Stir-fried rice noodles with shrimp, chicken, tofu, bean sprouts and peanuts",
            "image_url": "https://via.placeholder.com/300x300?text=Pad+Thai",
            "is_available": True,
            "stock_quantity": 50,
            "prep_time": 10,
            "is_recommended": True,
            "display_order": 1,
            "option_ids": option_ids,
        },
        {
            "name": "Green Curry",
            "category": "Curry",
            "price": 150.0,
            "description": "Spicy green curry with basil, bamboo shoots, and eggplant",
            "image_url": "https://via.placeholder.com/300x300?text=Green+Curry",
            "is_available": True,
            "stock_quantity": 40,
            "prep_time": 15,
            "is_recommended": True,
            "display_order": 2,
            "option_ids": option_ids,
        },
        {
            "name": "Massaman Curry",
            "category": "Curry",
            "price": 160.0,
            "description": "Rich and mild curry with potatoes, peanuts, and meat",
            "image_url": "https://via.placeholder.com/300x300?text=Massaman",
            "is_available": True,
            "stock_quantity": 35,
            "prep_time": 15,
            "is_recommended": False,
            "display_order": 3,
            "option_ids": option_ids,
        },
        {
            "name": "Tom Yum Soup",
            "category": "Soups",
            "price": 100.0,
            "description": "Spicy and sour soup with lemongrass, galangal, and lime",
            "image_url": "https://via.placeholder.com/300x300?text=Tom+Yum",
            "is_available": True,
            "stock_quantity": 60,
            "prep_time": 12,
            "is_recommended": True,
            "display_order": 1,
            "option_ids": option_ids,
        },
        {
            "name": "Larb",
            "category": "Salads",
            "price": 130.0,
            "description": "Spicy minced meat salad with herbs and lime dressing",
            "image_url": "https://via.placeholder.com/300x300?text=Larb",
            "is_available": True,
            "stock_quantity": 30,
            "prep_time": 10,
            "is_recommended": False,
            "display_order": 2,
            "option_ids": option_ids,
        },
        {
            "name": "Spring Rolls",
            "category": "Appetizers",
            "price": 80.0,
            "description": "Crispy spring rolls with sweet and sour sauce",
            "image_url": "https://via.placeholder.com/300x300?text=Spring+Rolls",
            "is_available": True,
            "stock_quantity": 100,
            "prep_time": 8,
            "is_recommended": True,
            "display_order": 1,
            "option_ids": [],
        },
        {
            "name": "Satay",
            "category": "Appetizers",
            "price": 90.0,
            "description": "Grilled meat skewers with peanut sauce",
            "image_url": "https://via.placeholder.com/300x300?text=Satay",
            "is_available": True,
            "stock_quantity": 50,
            "prep_time": 12,
            "is_recommended": True,
            "display_order": 2,
            "option_ids": option_ids,
        },
    ]

    created_items = []
    for item in menu_items:
        response = requests.post(f"{BASE_URL}/menu/items", json=item)
        if response.status_code == 201:
            created_item = response.json()
            created_items.append(created_item["id"])
            print(f"✓ {item['name']} created (ID: {created_item['id']})")
        else:
            print(f"✗ Failed to create {item['name']}: {response.text}")

    return created_items


def seed_sample_orders(item_ids):
    """Create sample orders."""
    print("\nCreating sample orders...")

    orders = [
        {
            "table_number": 1,
            "total": 250.0,
            "items": [
                {
                    "menu_item_id": item_ids[0] if len(item_ids) > 0 else 1,
                    "name": "Pad Thai",
                    "quantity": 1,
                    "price": 120.0,
                    "options_text": "Sweetness: Normal, Spice: Medium, Protein: Chicken",
                    "remark": "No peanuts",
                },
                {
                    "menu_item_id": item_ids[3] if len(item_ids) > 3 else 4,
                    "name": "Tom Yum Soup",
                    "quantity": 1,
                    "price": 100.0,
                    "options_text": "Sweetness: Normal, Spice: Hot",
                    "remark": "",
                },
            ],
        },
        {
            "table_number": 2,
            "total": 310.0,
            "items": [
                {
                    "menu_item_id": item_ids[1] if len(item_ids) > 1 else 2,
                    "name": "Green Curry",
                    "quantity": 2,
                    "price": 150.0,
                    "options_text": "Sweetness: Normal, Spice: Medium, Protein: Shrimp",
                    "remark": "Extra basil",
                },
            ],
        },
    ]

    for order in orders:
        response = requests.post(f"{BASE_URL}/orders", json=order)
        if response.status_code == 201:
            created_order = response.json()
            print(f"✓ Order created (ID: {created_order['id']}, Table: {order['table_number']})")
        else:
            print(f"✗ Failed to create order for table {order['table_number']}: {response.text}")


def main():
    """Main function to seed all data."""
    print("=" * 60)
    print("Restaurant Ordering System - Database Seeding")
    print("=" * 60)

    try:
        # Seed options first
        option_ids = seed_menu_options()

        # Seed menu items
        item_ids = seed_menu_items(option_ids)

        # Seed sample orders
        if item_ids:
            seed_sample_orders(item_ids)

        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        print("\nYou can now access the API at http://localhost:8000")
        print("- Swagger UI: http://localhost:8000/docs")
        print("- ReDoc: http://localhost:8000/redoc")

    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        print("\nMake sure the API is running at http://localhost:8000")


if __name__ == "__main__":
    main()
