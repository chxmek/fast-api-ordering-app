"""User management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.schemas import user as user_schemas
from app.db.database import get_db
from app.services import user_service
from app.core.security import JWTService
from app.models import UserRole, UserStatus

router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get current authenticated user from token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required"
        )
    
    # Extract token from "Bearer <token>"
    token = authorization
    if token.startswith("Bearer "):
        token = token[7:]
    
    user_id = JWTService.get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/me", response_model=user_schemas.UserResponse)
def get_current_user_profile(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get current logged-in user profile."""
    user = get_current_user(authorization, db)
    return user_schemas.UserResponse.from_orm(user)


@router.put("/me/profile", response_model=user_schemas.UserResponse)
def update_current_user_profile(
    update_data: user_schemas.UpdateProfileRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    user = get_current_user(authorization, db)
    updated_user = user_service.update_user_profile(db, user.id, update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_schemas.UserResponse.from_orm(updated_user)


@router.post("/me/change-password")
def change_current_user_password(
    request: user_schemas.ChangePasswordRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Change current user password."""
    user = get_current_user(authorization, db)
    try:
        user_service.change_user_password(
            db, user.id, request.old_password, request.new_password
        )
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# SuperAdmin-only endpoints
@router.get("/", response_model=list[user_schemas.UserListResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get all users (SuperAdmin only)."""
    user = get_current_user(authorization, db)
    if user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SuperAdmin can access this"
        )
    return user_service.get_users(db, skip, limit)


@router.get("/{user_id}", response_model=user_schemas.UserListResponse)
def get_user_by_id(
    user_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get a user by ID (SuperAdmin only)."""
    current_user = get_current_user(authorization, db)
    if current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SuperAdmin can access this"
        )
    
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_schemas.UserListResponse.from_orm(user)


@router.post("/", response_model=user_schemas.UserListResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    request: user_schemas.RegisterRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Create new user (Admin/SuperAdmin only)."""
    current_user = get_current_user(authorization, db)
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin/SuperAdmin can create users"
        )
    
    try:
        user = user_service.register_user(db, request)
        return user_schemas.UserListResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}/role", response_model=user_schemas.UserListResponse)
def update_user_role(
    user_id: int,
    new_role: user_schemas.UserRoleEnum,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update user role (SuperAdmin only)."""
    current_user = get_current_user(authorization, db)
    if current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SuperAdmin can change roles"
        )
    
    user = user_service.update_user_role(db, user_id, UserRole[new_role.value])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_schemas.UserListResponse.from_orm(user)


@router.put("/{user_id}/status", response_model=user_schemas.UserListResponse)
def update_user_status(
    user_id: int,
    new_status: user_schemas.UserStatusEnum,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update user status (SuperAdmin only)."""
    current_user = get_current_user(authorization, db)
    if current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SuperAdmin can change status"
        )
    
    user = user_service.update_user_status(db, user_id, UserStatus[new_status.value])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_schemas.UserListResponse.from_orm(user)


@router.delete("/{user_id}")
def soft_delete_user(
    user_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Soft delete user (SuperAdmin only)."""
    current_user = get_current_user(authorization, db)
    if current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SuperAdmin can delete users"
        )
    
    if user_service.soft_delete_user(db, user_id):
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
