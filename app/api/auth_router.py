"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.schemas import user as user_schemas
from app.services import user_service
from app.core.security import JWTService
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=user_schemas.AuthResponse)
def register(
    request: user_schemas.RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    try:
        user = user_service.register_user(db, request)
        
        # Generate tokens
        access_token = JWTService.create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        )
        refresh_token = JWTService.create_refresh_token(subject=str(user.id))
        
        return user_schemas.AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_schemas.UserResponse.from_orm(user),
            expires_in=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login", response_model=user_schemas.AuthResponse)
def login(
    request: user_schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """Login with email and password."""
    try:
        user = user_service.authenticate_user(db, request.email, request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate tokens
        access_token = JWTService.create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        )
        refresh_token = JWTService.create_refresh_token(subject=str(user.id))
        
        return user_schemas.AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_schemas.UserResponse.from_orm(user),
            expires_in=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh", response_model=user_schemas.TokenResponse)
def refresh_token(
    request: dict,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    refresh_token = request.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required"
        )
    
    payload = JWTService.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = JWTService.get_user_id_from_token(refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_access_token = JWTService.create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    )
    
    return user_schemas.TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
    )


@router.post("/verify-token")
def verify_token(request: dict, db: Session = Depends(get_db)):
    """Verify if a token is valid."""
    token = request.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required"
        )
    
    payload = JWTService.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return {"valid": True, "user_id": payload.get("sub")}


@router.post("/forgot-password")
def forgot_password(
    request: user_schemas.ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Request password reset (TODO: implement email service)."""
    user = user_service.get_user_by_email(db, request.email)
    if not user:
        # Don't reveal if email exists
        return {"message": "If email exists, password reset link will be sent"}
    
    # TODO: Generate reset token and send email
    # For now, just return success message
    return {"message": "Password reset link sent to email"}


@router.post("/reset-password")
def reset_password(
    request: user_schemas.ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password with token."""
    # TODO: Implement proper token verification and password reset
    # For now, return success (placeholder implementation)
    return {"message": "Password reset successful"}


@router.post("/reset-password")
def reset_password(
    request: user_schemas.ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password with reset token."""
    # TODO: Verify reset token and update password
    raise HTTPException(status_code=501, detail="Feature not yet implemented")
