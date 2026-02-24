from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    """Schema for creating order item."""
    menu_item_id: int
    name: str
    quantity: int
    price: float
    options_text: Optional[str] = None
    remark: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    id: int
    order_id: int
    menu_item_id: int
    name: str
    quantity: int
    price: float
    options_text: Optional[str]
    remark: Optional[str]

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating order."""
    total: float
    table_number: Optional[int] = None
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    """Schema for updating order."""
    status: Optional[str] = None
    table_number: Optional[int] = None


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: int
    total: float
    status: str
    table_number: Optional[int]
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
