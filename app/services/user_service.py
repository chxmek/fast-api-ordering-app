from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models import User, UserRole, UserStatus
from app.schemas import UserCreate, RegisterRequest, UpdateProfileRequest
from app.core.security import PasswordService, JWTService


def create_user(db: Session, user: UserCreate, role: UserRole = UserRole.USER) -> User:
    """Create a new user in the database."""
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=PasswordService.hash_password(user.password),
        role=role,
        status=UserStatus.ACTIVE,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def register_user(db: Session, register_data: RegisterRequest) -> User:
    """Register a new user."""
    if get_user_by_email(db, register_data.email):
        raise ValueError(f"Email {register_data.email} already registered")
    
    db_user = User(
        name=register_data.name,
        email=register_data.email,
        password_hash=PasswordService.hash_password(register_data.password),
        phone=register_data.phone,
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Authenticate a user with email and password."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not PasswordService.verify_password(password, user.password_hash):
        return None
    if user.status == UserStatus.BANNED:
        raise ValueError("User account is banned")
    if user.status == UserStatus.INACTIVE:
        raise ValueError("User account is inactive")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users from the database."""
    return db.query(User).filter(User.is_deleted == False).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get a user by ID."""
    return db.query(User).filter(
        and_(User.id == user_id, User.is_deleted == False)
    ).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email."""
    return db.query(User).filter(
        and_(User.email == email, User.is_deleted == False)
    ).first()


def update_user_profile(db: Session, user_id: int, update_data: UpdateProfileRequest) -> User | None:
    """Update user profile information."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if update_data.name:
        user.name = update_data.name
    if update_data.phone:
        user.phone = update_data.phone
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def change_user_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
    """Change user password."""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    if not PasswordService.verify_password(old_password, user.password_hash):
        raise ValueError("Old password is incorrect")
    
    user.password_hash = PasswordService.hash_password(new_password)
    user.updated_at = datetime.utcnow()
    db.commit()
    return True


def update_user_role(db: Session, user_id: int, new_role: UserRole) -> User | None:
    """Update user role (SuperAdmin only)."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.role = new_role
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def update_user_status(db: Session, user_id: int, new_status: UserStatus) -> User | None:
    """Update user status (ban/unban/activate/deactivate)."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.status = new_status
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user_id: int) -> bool:
    """Soft delete a user."""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    user.is_deleted = True
    user.updated_at = datetime.utcnow()
    db.commit()
    return True

