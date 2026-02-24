"""Admin dashboard API endpoints for analytics and management."""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.database import get_db
from app.models import Order, OrderItem, User, UserRole
from app.services import user_service
from app.services.order_service import OrderService
from app.core.security import JWTService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_current_admin(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Verify current user is admin or superadmin."""
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
    if not user or user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user


@router.get("/dashboard/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics (total orders, revenue, users, etc)."""
    try:
        # Total orders
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        
        # Total revenue
        total_revenue = db.query(func.sum(Order.total)).scalar() or 0
        
        # Total users
        total_users = db.query(func.count(User.id)).filter(
            User.is_deleted == False
        ).scalar() or 0
        
        # Active users (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_users = db.query(func.count(User.id)).filter(
            User.last_login >= thirty_days_ago,
            User.is_deleted == False
        ).scalar() or 0
        
        # Orders today
        today = datetime.utcnow().date()
        orders_today = db.query(func.count(Order.id)).filter(
            func.date(Order.created_at) == today
        ).scalar() or 0
        
        # Revenue today
        revenue_today = db.query(func.sum(Order.total)).filter(
            func.date(Order.created_at) == today
        ).scalar() or 0
        
        logger.info(f"Dashboard stats retrieved by user {current_user.id}")
        
        return {
            "total_orders": total_orders,
            "total_revenue": float(total_revenue) if total_revenue else 0,
            "total_users": total_users,
            "active_users_30d": active_users,
            "orders_today": orders_today,
            "revenue_today": float(revenue_today) if revenue_today else 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard statistics"
        )


@router.get("/orders/summary")
def get_orders_summary(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get order summary for the last N days."""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        orders = db.query(
            func.date(Order.created_at).label('date'),
            func.count(Order.id).label('count'),
            func.sum(Order.total).label('revenue')
        ).filter(
            Order.created_at >= start_date
        ).group_by(
            func.date(Order.created_at)
        ).all()
        
        summary = [
            {
                "date": str(order.date),
                "order_count": order.count,
                "revenue": float(order.revenue) if order.revenue else 0
            }
            for order in orders
        ]
        
        logger.info(f"Orders summary retrieved for {days} days by user {current_user.id}")
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error getting orders summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve orders summary"
        )


@router.get("/revenue/report")
def get_revenue_report(
    start_date: str = Query(...),  # YYYY-MM-DD
    end_date: str = Query(...),    # YYYY-MM-DD
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get revenue report for a date range."""
    try:
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        end = end + timedelta(days=1)  # Include end date
        
        # Get orders in range
        orders = db.query(Order).filter(
            Order.created_at >= start,
            Order.created_at < end
        ).all()
        
        # Calculate metrics
        total_orders = len(orders)
        total_revenue = sum(o.total or 0 for o in orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Get orders by status
        status_breakdown = {}
        for order in orders:
            status = order.status or "unknown"
            if status not in status_breakdown:
                status_breakdown[status] = {
                    "count": 0,
                    "revenue": 0
                }
            status_breakdown[status]["count"] += 1
            status_breakdown[status]["revenue"] += order.total or 0
        
        logger.info(f"Revenue report retrieved for {start_date} to {end_date} by user {current_user.id}")
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "average_order_value": avg_order_value,
            "status_breakdown": status_breakdown
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    except Exception as e:
        logger.error(f"Error getting revenue report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve revenue report"
        )


@router.get("/users/list")
def get_users_list(
    role: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get list of users (admin only)."""
    try:
        query = db.query(User).filter(User.is_deleted == False)
        
        if role:
            # Filter by role
            try:
                user_role = UserRole[role.upper()]
                query = query.filter(User.role == user_role)
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role: {role}"
                )
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        
        user_list = [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "phone": u.phone,
                "role": u.role.value if u.role else "user",
                "status": u.status.value if u.status else "active",
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "last_login": u.last_login.isoformat() if u.last_login else None
            }
            for u in users
        ]
        
        logger.info(f"Users list retrieved (count: {total}) by user {current_user.id}")
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "users": user_list
        }
    except Exception as e:
        logger.error(f"Error getting users list: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users list"
        )


@router.get("/top-products")
def get_top_products(
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get top selling products for the last N days."""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Note: This assumes OrderItem has a product_name or similar field
        # Adjust based on your actual schema
        top_products = db.query(
            OrderItem.name.label('product_name'),
            func.count(OrderItem.id).label('quantity_sold'),
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
        ).join(Order).filter(
            Order.created_at >= start_date,
            OrderItem.name.isnot(None)
        ).group_by(
            OrderItem.name
        ).order_by(
            func.sum(OrderItem.quantity * OrderItem.price).desc()
        ).limit(limit).all()
        
        products = [
            {
                "product_name": p.product_name,
                "times_ordered": p.quantity_sold,
                "total_quantity": p.total_quantity or 0,
                "total_revenue": float(p.total_revenue) if p.total_revenue else 0
            }
            for p in top_products
        ]
        
        logger.info(f"Top products retrieved (count: {len(products)}) by user {current_user.id}")
        
        return {
            "days": days,
            "limit": limit,
            "products": products
        }
    except Exception as e:
        logger.error(f"Error getting top products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve top products"
        )


@router.get("/orders/by-status")
def get_orders_by_status(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get order count and revenue breakdown by status."""
    try:
        orders_by_status = db.query(
            Order.status,
            func.count(Order.id).label('count'),
            func.sum(Order.total).label('revenue'),
            func.avg(Order.total).label('avg_amount')
        ).group_by(Order.status).all()
        
        breakdown = [
            {
                "status": o.status or "unknown",
                "count": o.count,
                "total_revenue": float(o.revenue) if o.revenue else 0,
                "avg_order_value": float(o.avg_amount) if o.avg_amount else 0
            }
            for o in orders_by_status
        ]
        
        logger.info(f"Orders by status retrieved by user {current_user.id}")
        return {"breakdown": breakdown}
    except Exception as e:
        logger.error(f"Error getting orders by status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve orders by status"
        )
