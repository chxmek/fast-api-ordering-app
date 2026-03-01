#!/usr/bin/env python3
"""Promote user to SUPERADMIN role."""
from app.services import user_service
from app.db.database import SessionLocal
from app.models.user import UserRole

def promote_to_superadmin(email: str):
    """Promote a user to SUPERADMIN role."""
    db = SessionLocal()
    try:
        user = user_service.get_user_by_email(db, email)
        if not user:
            print(f'❌ User {email} not found')
            return
        
        # Update role to SUPERADMIN
        user.role = UserRole.SUPERADMIN
        db.commit()
        db.refresh(user)
        
        print(f'✅ User promoted to SUPERADMIN')
        print(f'  Email: {user.email}')
        print(f'  Name: {user.name}')
        print(f'  Role: {user.role}')
        print(f'  Status: {user.status}')
    finally:
        db.close()

if __name__ == '__main__':
    promote_to_superadmin('mek@email.com')
