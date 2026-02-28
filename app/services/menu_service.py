from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models.menu import MenuItem, MenuOption, OptionChoice
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, MenuOptionCreate, MenuOptionUpdate, OptionChoiceCreate
from app.core.exceptions import AppException


class MenuService:
    """Service for menu operations."""

    @staticmethod
    def get_all_menu_items(
        db: Session,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[MenuItem]:
        """Get all menu items with optional filtering."""
        query = db.query(MenuItem)
        if category:
            query = query.filter(MenuItem.category == category)
        return query.order_by(MenuItem.display_order, MenuItem.id).offset(skip).limit(limit).all()

    @staticmethod
    def get_menu_item_by_id(db: Session, item_id: int) -> MenuItem:
        """Get menu item by ID."""
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not item:
            raise AppException("Menu item not found", 404)
        return item

    @staticmethod
    def create_menu_item(
        db: Session,
        item_create: MenuItemCreate
    ) -> MenuItem:
        """Create new menu item."""
        # Get max display order for this category
        max_order = db.query(func.max(MenuItem.display_order)).filter(
            MenuItem.category == item_create.category
        ).scalar() or 0

        menu_item = MenuItem(
            name=item_create.name,
            category=item_create.category,
            price=item_create.price,
            image_url=item_create.image_url,
            description=item_create.description,
            is_available=item_create.is_available,
            stock_quantity=item_create.stock_quantity,
            prep_time=item_create.prep_time,
            is_recommended=item_create.is_recommended,
            display_order=item_create.display_order or max_order + 1,
        )

        # Add options if provided
        if item_create.option_ids:
            options = db.query(MenuOption).filter(
                MenuOption.id.in_(item_create.option_ids)
            ).all()
            menu_item.options = options

        db.add(menu_item)
        db.commit()
        db.refresh(menu_item)
        return menu_item

    @staticmethod
    def update_menu_item(
        db: Session,
        item_id: int,
        item_update: MenuItemUpdate
    ) -> MenuItem:
        """Update menu item."""
        item = MenuService.get_menu_item_by_id(db, item_id)

        # Update fields if provided
        update_data = item_update.dict(exclude_unset=True)
        option_ids = update_data.pop('option_ids', None)

        for field, value in update_data.items():
            if value is not None:
                setattr(item, field, value)

        if option_ids is not None:
            options = db.query(MenuOption).filter(
                MenuOption.id.in_(option_ids)
            ).all()
            item.options = options

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_menu_item(db: Session, item_id: int) -> None:
        """Delete menu item."""
        item = MenuService.get_menu_item_by_id(db, item_id)
        db.delete(item)
        db.commit()

    @staticmethod
    def get_categories(db: Session) -> List[str]:
        """Get all menu categories."""
        categories = db.query(MenuItem.category).distinct().all()
        return [cat[0] for cat in categories]

    # Menu Options Management

    @staticmethod
    def get_all_menu_options(db: Session) -> List[MenuOption]:
        """Get all menu options."""
        return db.query(MenuOption).order_by(MenuOption.display_order, MenuOption.id).all()

    @staticmethod
    def get_menu_option_by_id(db: Session, option_id: int) -> MenuOption:
        """Get menu option by ID."""
        option = db.query(MenuOption).filter(MenuOption.id == option_id).first()
        if not option:
            raise AppException("Menu option not found", 404)
        return option

    @staticmethod
    def create_menu_option(
        db: Session,
        option_create: MenuOptionCreate
    ) -> MenuOption:
        """Create new menu option with choices."""
        menu_option = MenuOption(
            name=option_create.name,
            description=option_create.description,
            option_type=option_create.option_type,
            is_required=option_create.is_required,
            min_selection=option_create.min_selection,
            max_selection=option_create.max_selection,
            display_order=option_create.display_order,
        )

        # Add choices
        for idx, choice_create in enumerate(option_create.choices):
            choice = OptionChoice(
                name=choice_create.name,
                price_modifier=choice_create.price_modifier,
                is_default=choice_create.is_default,
                display_order=choice_create.display_order or idx,
            )
            menu_option.choices.append(choice)

        db.add(menu_option)
        db.commit()
        db.refresh(menu_option)
        return menu_option

    @staticmethod
    def update_menu_option(
        db: Session,
        option_id: int,
        option_update: MenuOptionUpdate
    ) -> MenuOption:
        """Update menu option."""
        option = MenuService.get_menu_option_by_id(db, option_id)

        update_data = option_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                # Map option_type to option_type column
                if field == 'option_type':
                    setattr(option, 'option_type', value)
                else:
                    setattr(option, field, value)

        db.commit()
        db.refresh(option)
        return option

    @staticmethod
    def delete_menu_option(db: Session, option_id: int) -> None:
        """Delete menu option."""
        option = MenuService.get_menu_option_by_id(db, option_id)
        db.delete(option)
        db.commit()

    # Option Choices Management

    @staticmethod
    def create_option_choice(
        db: Session,
        option_id: int,
        choice_create: OptionChoiceCreate
    ) -> OptionChoice:
        """Create option choice."""
        option = MenuService.get_menu_option_by_id(db, option_id)

        choice = OptionChoice(
            menu_option_id=option_id,
            name=choice_create.name,
            price_modifier=choice_create.price_modifier,
            is_default=choice_create.is_default,
            display_order=choice_create.display_order,
        )

        db.add(choice)
        db.commit()
        db.refresh(choice)
        return choice

    @staticmethod
    def update_option_choice(
        db: Session,
        choice_id: int,
        choice_data: dict
    ) -> OptionChoice:
        """Update option choice."""
        choice = db.query(OptionChoice).filter(OptionChoice.id == choice_id).first()
        if not choice:
            raise AppException("Option choice not found", 404)

        for field, value in choice_data.items():
            if value is not None:
                setattr(choice, field, value)

        db.commit()
        db.refresh(choice)
        return choice

    @staticmethod
    def delete_option_choice(db: Session, choice_id: int) -> None:
        """Delete option choice."""
        choice = db.query(OptionChoice).filter(OptionChoice.id == choice_id).first()
        if not choice:
            raise AppException("Option choice not found", 404)

        db.delete(choice)
        db.commit()

    @staticmethod
    def reorder_option_choices(
        db: Session,
        option_id: int,
        choice_orders: List[dict]
    ) -> List[OptionChoice]:
        """Reorder option choices. Expected: [{"id": 1, "display_order": 1}, ...]"""
        option = MenuService.get_menu_option_by_id(db, option_id)

        # Update display_order for each choice
        for choice_order in choice_orders:
            choice = db.query(OptionChoice).filter(
                OptionChoice.id == choice_order['id'],
                OptionChoice.menu_option_id == option_id
            ).first()
            if choice:
                choice.display_order = choice_order['display_order']

        db.commit()

        # Return sorted choices
        return db.query(OptionChoice).filter(
            OptionChoice.menu_option_id == option_id
        ).order_by(OptionChoice.display_order, OptionChoice.id).all()
