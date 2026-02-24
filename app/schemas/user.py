from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRoleEnum(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"


class UserStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    phone: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    """Schema for password change."""
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: 'UserResponse'
    expires_in: int


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRoleEnum
    status: UserStatusEnum
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = None
    phone: Optional[str] = None


class UserListResponse(BaseModel):
    """Schema for user list response."""
    id: int
    name: str
    email: str
    phone: Optional[str]
    role: UserRoleEnum
    status: UserStatusEnum
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True
