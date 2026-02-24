from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


# Association table for many-to-many relationship between MenuItems and MenuOptions
menu_item_options = Table(
    'menu_item_options',
    Base.metadata,
    Column('menu_item_id', Integer, ForeignKey('menu_items.id', ondelete='CASCADE'), primary_key=True),
    Column('menu_option_id', Integer, ForeignKey('menu_options.id', ondelete='CASCADE'), primary_key=True),
)


class MenuItem(Base):
    """Menu item database model."""
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    image_url = Column(String(500), nullable=True)
    description = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True)
    stock_quantity = Column(Integer, nullable=True)  # NULL means unlimited
    prep_time = Column(Integer, nullable=True)  # Preparation time in minutes
    is_recommended = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    options = relationship(
        "MenuOption",
        secondary=menu_item_options,
        back_populates="menu_items"
    )
    order_items = relationship("OrderItem", back_populates="menu_item", cascade="all, delete-orphan")


class MenuOption(Base):
    """Menu option (e.g., Sweetness Level, Spiciness Level)."""
    __tablename__ = "menu_options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    option_type = Column(String(50), default='single')  # 'single' or 'multiple'
    is_required = Column(Boolean, default=False)
    min_selection = Column(Integer, nullable=True)  # For multiple type
    max_selection = Column(Integer, nullable=True)  # For multiple type
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    choices = relationship("OptionChoice", back_populates="menu_option", cascade="all, delete-orphan")
    menu_items = relationship(
        "MenuItem",
        secondary=menu_item_options,
        back_populates="options"
    )


class OptionChoice(Base):
    """Option choice (e.g., ไม่หวาน, หวานน้อย, หวานมาก)."""
    __tablename__ = "option_choices"

    id = Column(Integer, primary_key=True, index=True)
    menu_option_id = Column(Integer, ForeignKey("menu_options.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    price_modifier = Column(Float, default=0.0)  # Additional cost for this choice
    is_default = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    menu_option = relationship("MenuOption", back_populates="choices")
