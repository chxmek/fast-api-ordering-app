"""API Router Module"""

from . import auth_router, user_router, menu_router, orders_router, admin_router, superadmin_router

__all__ = ["auth_router", "user_router", "menu_router", "orders_router", "admin_router", "superadmin_router"]
