from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from datetime import datetime
from app.db.database import Base


class AuditLog(Base):
    """Audit log model for tracking all user actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    action = Column(String, nullable=False)  # e.g., "menu.created", "order.cancelled"
    resource_type = Column(String, nullable=False)  # e.g., "menu_item", "order", "user"
    resource_id = Column(Integer, nullable=False)
    old_value = Column(JSON, nullable=True)  # Previous value before change
    new_value = Column(JSON, nullable=True)  # New value after change
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    description = Column(Text, nullable=True)
