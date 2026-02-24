from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.order import Order, OrderItem
from app.models.menu import MenuItem
from app.schemas.order import OrderCreate, OrderUpdate
from app.core.exceptions import AppException


class OrderService:
    """Service for order operations."""

    @staticmethod
    def get_all_orders(
        db: Session,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Order]:
        """Get all orders with optional filtering by status."""
        query = db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:
        """Get order by ID."""
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise AppException("Order not found", 404)
        return order

    @staticmethod
    def create_order(db: Session, order_create: OrderCreate) -> Order:
        """Create new order."""
        # Validate stock if needed
        for item in order_create.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            if not menu_item:
                raise AppException(f"Menu item {item.menu_item_id} not found", 400)
            if not menu_item.is_available:
                raise AppException(f"Menu item '{menu_item.name}' is not available", 400)
            if menu_item.stock_quantity is not None and menu_item.stock_quantity < item.quantity:
                raise AppException(
                    f"Menu item '{menu_item.name}' has insufficient stock. Available: {menu_item.stock_quantity}, Requested: {item.quantity}",
                    400
                )

        order = Order(
            total=order_create.total,
            table_number=order_create.table_number,
            status='pending'
        )

        # Add order items
        for item_create in order_create.items:
            order_item = OrderItem(
                menu_item_id=item_create.menu_item_id,
                name=item_create.name,
                quantity=item_create.quantity,
                price=item_create.price,
                options_text=item_create.options_text,
                remark=item_create.remark,
            )
            order.items.append(order_item)

            # Reduce stock if applicable
            menu_item = db.query(MenuItem).filter(MenuItem.id == item_create.menu_item_id).first()
            if menu_item and menu_item.stock_quantity is not None:
                menu_item.stock_quantity -= item_create.quantity

        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Order:
        """Update order."""
        order = OrderService.get_order_by_id(db, order_id)

        update_data = order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(order, field, value)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def delete_order(db: Session, order_id: int) -> None:
        """Delete order and restore stock."""
        order = OrderService.get_order_by_id(db, order_id)

        # Restore stock
        for item in order.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            if menu_item and menu_item.stock_quantity is not None:
                menu_item.stock_quantity += item.quantity

        db.delete(order)
        db.commit()

    @staticmethod
    def cancel_order(db: Session, order_id: int) -> Order:
        """Cancel order and restore stock."""
        order = OrderService.get_order_by_id(db, order_id)

        if order.status == 'cancelled':
            raise AppException("Order is already cancelled", 400)

        # Restore stock
        for item in order.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            if menu_item and menu_item.stock_quantity is not None:
                menu_item.stock_quantity += item.quantity

        order.status = 'cancelled'
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def complete_order(db: Session, order_id: int) -> Order:
        """Mark order as completed."""
        order = OrderService.get_order_by_id(db, order_id)

        if order.status == 'completed':
            raise AppException("Order is already completed", 400)

        if order.status == 'cancelled':
            raise AppException("Cannot complete a cancelled order", 400)

        order.status = 'completed'
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order_summary(db: Session) -> dict:
        """Get order summary statistics."""
        total_orders = db.query(Order).count()
        completed_orders = db.query(Order).filter(Order.status == 'completed').count()
        pending_orders = db.query(Order).filter(Order.status == 'pending').count()
        cancelled_orders = db.query(Order).filter(Order.status == 'cancelled').count()

        return {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'cancelled_orders': cancelled_orders,
        }
