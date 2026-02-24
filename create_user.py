#!/usr/bin/env python3
"""Create a test user for authentication."""
from app.services import user_service
from app.schemas.user import RegisterRequest
from app.db.database import SessionLocal

def create_test_user():
    """Create a test user account."""
    db = SessionLocal()
    try:
        # Check if user exists
        existing = user_service.get_user_by_email(db, 'mek@email.com')
        if existing:
            print('✓ User mek@email.com already exists')
            print(f'  User ID: {existing.id}')
            print(f'  Name: {existing.name}')
            print(f'  Role: {existing.role}')
            print(f'  Status: {existing.status}')
        else:
            # Register new user
            register_data = RegisterRequest(
                name='Mek',
                email='mek@email.com',
                password='password123',
                phone='1234567890'
            )
            user = user_service.register_user(db=db, register_data=register_data)
            print(f'✓ Created user: {user.email}')
            print(f'  User ID: {user.id}')
            print(f'  Name: {user.name}')
            print(f'  Role: {user.role}')
            print(f'  Status: {user.status}')
    finally:
        db.close()

if __name__ == '__main__':
    create_test_user()
