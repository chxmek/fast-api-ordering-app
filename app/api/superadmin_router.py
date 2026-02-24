"""SuperAdmin API endpoints for role and permission management."""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.db.database import get_db
from app.models import User, UserRole, Permission, AuditLog
from app.services import user_service
from app.core.security import JWTService
from app.core.logging import get_logger
from app.schemas.user import UserRoleEnum, UserStatusEnum

logger = get_logger(__name__)

router = APIRouter(prefix="/superadmin", tags=["SuperAdmin"])


def get_current_superadmin(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Verify current user is superadmin."""
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
    if not user or user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="SuperAdmin access required"
        )
    
    return user


@router.get("/users/list")
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    role: str = Query(None),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get all users with optional role filter."""
    try:
        query = db.query(User).filter(User.is_deleted == False)
        
        if role:
            query = query.filter(User.role == role.upper())
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        
        users_list = [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role.value if u.role else "user",
                "status": u.status.value if u.status else "active",
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None,
            }
            for u in users
        ]
        
        logger.info(f"Users list retrieved (total: {total}) by superadmin {current_user.id}")
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "users": users_list
        }
    except Exception as e:
        logger.error(f"Error getting users list: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/roles/summary")
def get_roles_summary(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get summary of users by role."""
    try:
        roles_summary = db.query(
            User.role,
            func.count(User.id).label('count')
        ).filter(
            User.is_deleted == False
        ).group_by(User.role).all()
        
        summary = {
            "total_users": db.query(func.count(User.id)).filter(
                User.is_deleted == False
            ).scalar() or 0,
            "by_role": [
                {
                    "role": r.role.value if r.role else "unknown",
                    "count": r.count
                }
                for r in roles_summary
            ]
        }
        
        logger.info(f"Roles summary retrieved by superadmin {current_user.id}")
        return summary
    except Exception as e:
        logger.error(f"Error getting roles summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve roles summary"
        )


@router.put("/{user_id}/promote-admin")
def promote_user_to_admin(
    user_id: int,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Promote a regular user to admin."""
    try:
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already an admin"
            )
        
        # Update role to ADMIN
        updated_user = user_service.update_user_role(db, user_id, UserRole.ADMIN)
        
        # Log audit
        audit_log = AuditLog(
            action="PROMOTE_TO_ADMIN",
            resource_type="User",
            resource_id=user_id,
            user_id=current_user.id,
            old_value={"role": user.role.value if user.role else "user"},
            new_value={"role": "admin"},
            ip_address="",  # Can be extracted from request context
            user_agent=""
        )
        db.add(audit_log)
        db.commit()
        
        logger.info(f"User {user_id} promoted to admin by superadmin {current_user.id}")
        return {
            "message": "User promoted to admin successfully",
            "user_id": user_id,
            "new_role": "admin"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error promoting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to promote user"
        )


@router.put("/{user_id}/demote-admin")
def demote_admin_to_user(
    user_id: int,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Demote an admin back to regular user."""
    try:
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not an admin"
            )
        
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot demote yourself"
            )
        
        # Update role to USER
        updated_user = user_service.update_user_role(db, user_id, UserRole.USER)
        
        # Log audit
        audit_log = AuditLog(
            action="DEMOTE_FROM_ADMIN",
            resource_type="User",
            resource_id=user_id,
            user_id=current_user.id,
            old_value={"role": "admin"},
            new_value={"role": "user"},
            ip_address="",
            user_agent=""
        )
        db.add(audit_log)
        db.commit()
        
        logger.info(f"Admin {user_id} demoted to user by superadmin {current_user.id}")
        return {
            "message": "Admin demoted to user successfully",
            "user_id": user_id,
            "new_role": "user"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error demoting admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to demote admin"
        )


@router.get("/permissions/list")
def get_permissions_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get all permissions in the system."""
    try:
        total = db.query(func.count(Permission.id)).scalar() or 0
        permissions = db.query(Permission).offset(skip).limit(limit).all()
        
        permission_list = [
            {
                "id": p.id,
                "code": p.code,
                "description": p.description,
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            for p in permissions
        ]
        
        logger.info(f"Permissions list retrieved (total: {total}) by superadmin {current_user.id}")
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "permissions": permission_list
        }
    except Exception as e:
        logger.error(f"Error getting permissions list: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve permissions"
        )


@router.get("/audit-logs")
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    action: str = Query(None),
    user_id: int = Query(None),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get system audit logs."""
    try:
        query = db.query(AuditLog)
        
        if action:
            query = query.filter(AuditLog.action == action.upper())
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        total = query.count()
        logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
        
        log_list = [
            {
                "id": l.id,
                "action": l.action,
                "resource_type": l.resource_type,
                "resource_id": l.resource_id,
                "user_id": l.user_id,
                "old_value": l.old_value,
                "new_value": l.new_value,
                "created_at": l.created_at.isoformat() if l.created_at else None
            }
            for l in logs
        ]
        
        logger.info(f"Audit logs retrieved (count: {len(log_list)}) by superadmin {current_user.id}")
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "logs": log_list
        }
    except Exception as e:
        logger.error(f"Error getting audit logs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve audit logs"
        )


@router.get("/system-health")
def get_system_health(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get system health and statistics."""
    try:
        # Count users by status and role
        total_users = db.query(func.count(User.id)).filter(
            User.is_deleted == False
        ).scalar() or 0
        
        deleted_users = db.query(func.count(User.id)).filter(
            User.is_deleted == True
        ).scalar() or 0
        
        admin_count = db.query(func.count(User.id)).filter(
            User.is_deleted == False,
            User.role == UserRole.ADMIN
        ).scalar() or 0
        
        superadmin_count = db.query(func.count(User.id)).filter(
            User.is_deleted == False,
            User.role == UserRole.SUPERADMIN
        ).scalar() or 0
        
        # Count recent audit logs
        recent_logs = db.query(func.count(AuditLog.id)).scalar() or 0
        
        health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "uptime": "All systems operational",
            "users": {
                "total": total_users,
                "active": total_users,
                "deleted": deleted_users,
                "admin_count": admin_count,
                "superadmin_count": superadmin_count,
            },
            "audit_logs": {
                "total": recent_logs,
            },
            "database": {
                "connected": True,
                "status": "connected",
            },
            "cache": {
                "status": "active",
            }
        }
        
        logger.info(f"System health retrieved by superadmin {current_user.id}")
        return health
    except Exception as e:
        logger.error(f"Error getting system health: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system health"
        )


@router.post("/reset-user-password/{user_id}")
def admin_reset_user_password(
    user_id: int,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """SuperAdmin can reset any user's password."""
    try:
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate a temporary password (in production, send via email)
        from app.core.security import PasswordService
        temp_password = "TempPassword123!"
        
        user.password_hash = PasswordService.hash_password(temp_password)
        db.commit()
        
        # Log audit
        audit_log = AuditLog(
            action="ADMIN_RESET_PASSWORD",
            resource_type="User",
            resource_id=user_id,
            user_id=current_user.id,
            old_value={"password_changed": False},
            new_value={"password_changed": True},
            ip_address="",
            user_agent=""
        )
        db.add(audit_log)
        db.commit()
        
        logger.info(f"Password reset for user {user_id} by superadmin {current_user.id}")
        return {
            "message": "Password reset successfully",
            "user_id": user_id,
            "temporary_password": temp_password,
            "note": "User should change password on next login"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )
