from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OptionChoiceCreate(BaseModel):
    """Schema for creating option choice."""
    name: str
    price_modifier: float = 0.0
    is_default: bool = False
    display_order: int = 0


class OptionChoiceResponse(BaseModel):
    """Schema for option choice response."""
    id: int
    menu_option_id: int
    name: str
    price_modifier: float
    is_default: bool
    display_order: int

    class Config:
        from_attributes = True


class MenuOptionCreate(BaseModel):
    """Schema for creating menu option."""
    name: str
    description: Optional[str] = None
    option_type: str = 'single'  # 'single' or 'multiple'
    is_required: bool = False
    min_selection: Optional[int] = None
    max_selection: Optional[int] = None
    display_order: int = 0
    choices: List[OptionChoiceCreate] = []


class MenuOptionUpdate(BaseModel):
    """Schema for updating menu option."""
    name: Optional[str] = None
    description: Optional[str] = None
    option_type: Optional[str] = None
    is_required: Optional[bool] = None
    min_selection: Optional[int] = None
    max_selection: Optional[int] = None
    display_order: Optional[int] = None


class MenuOptionResponse(BaseModel):
    """Schema for menu option response."""
    id: int
    name: str
    description: Optional[str]
    option_type: str
    is_required: bool
    min_selection: Optional[int]
    max_selection: Optional[int]
    display_order: int
    choices: List[OptionChoiceResponse]

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    """Schema for creating menu item."""
    name: str
    category: str
    price: float
    image_url: Optional[str] = None
    description: Optional[str] = None
    is_available: bool = True
    stock_quantity: Optional[int] = None
    prep_time: Optional[int] = None
    is_recommended: bool = False
    display_order: int = 0
    option_ids: List[int] = []


class MenuItemUpdate(BaseModel):
    """Schema for updating menu item."""
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = None
    prep_time: Optional[int] = None
    is_recommended: Optional[bool] = None
    display_order: Optional[int] = None
    option_ids: Optional[List[int]] = None


class MenuItemResponse(BaseModel):
    """Schema for menu item response."""
    id: int
    name: str
    category: str
    price: float
    image_url: Optional[str]
    description: Optional[str]
    is_available: bool
    stock_quantity: Optional[int]
    prep_time: Optional[int]
    is_recommended: bool
    display_order: int
    options: List[MenuOptionResponse]

    class Config:
        from_attributes = True
