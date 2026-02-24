from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
)
from app.services.order_service import OrderService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/orders",
    tags=["Orders Management"],
)


@router.get("", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get all orders with optional filtering by status."""
    logger.info(f"Fetching orders: status={status}, skip={skip}, limit={limit}")
    orders = OrderService.get_all_orders(db, status=status, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Get order by ID."""
    logger.info(f"Fetching order: {order_id}")
    order = OrderService.get_order_by_id(db, order_id)
    return order


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
    order_create: OrderCreate,
    db: Session = Depends(get_db),
):
    """Create new order."""
    logger.info(f"Creating order with {len(order_create.items)} items")
    order = OrderService.create_order(db, order_create)
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int = Path(..., gt=0),
    order_update: OrderUpdate = None,
    db: Session = Depends(get_db),
):
    """Update order."""
    logger.info(f"Updating order: {order_id}")
    order = OrderService.update_order(db, order_id, order_update)
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Delete order and restore stock."""
    logger.info(f"Deleting order: {order_id}")
    OrderService.delete_order(db, order_id)
    return None


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Cancel order and restore stock."""
    logger.info(f"Cancelling order: {order_id}")
    order = OrderService.cancel_order(db, order_id)
    return order


@router.post("/{order_id}/complete", response_model=OrderResponse)
def complete_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Mark order as completed."""
    logger.info(f"Completing order: {order_id}")
    order = OrderService.complete_order(db, order_id)
    return order


@router.get("/summary/statistics", response_model=dict)
def get_order_summary(db: Session = Depends(get_db)):
    """Get order summary statistics."""
    logger.info("Fetching order summary")
    summary = OrderService.get_order_summary(db)
    return summary
