from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.menu import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse,
    MenuOptionCreate,
    MenuOptionUpdate,
    MenuOptionResponse,
    OptionChoiceCreate,
    OptionChoiceResponse,
)
from app.services.menu_service import MenuService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/menu",
    tags=["Menu Management"],
)


# Menu Items Endpoints

@router.get("/items", response_model=List[MenuItemResponse])
def get_all_menu_items(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get all menu items with optional filtering by category."""
    logger.info(f"Fetching menu items: category={category}, skip={skip}, limit={limit}")
    items = MenuService.get_all_menu_items(db, category=category, skip=skip, limit=limit)
    return items


@router.get("/items/{item_id}", response_model=MenuItemResponse)
def get_menu_item(
    item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Get menu item by ID."""
    logger.info(f"Fetching menu item: {item_id}")
    item = MenuService.get_menu_item_by_id(db, item_id)
    return item


@router.post("/items", response_model=MenuItemResponse, status_code=201)
def create_menu_item(
    item_create: MenuItemCreate,
    db: Session = Depends(get_db),
):
    """Create new menu item."""
    logger.info(f"Creating menu item: {item_create.name}")
    item = MenuService.create_menu_item(db, item_create)
    return item


@router.put("/items/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int = Path(..., gt=0),
    item_update: MenuItemUpdate = None,
    db: Session = Depends(get_db),
):
    """Update menu item."""
    logger.info(f"Updating menu item: {item_id}")
    item = MenuService.update_menu_item(db, item_id, item_update)
    return item


@router.delete("/items/{item_id}", status_code=204)
def delete_menu_item(
    item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Delete menu item."""
    logger.info(f"Deleting menu item: {item_id}")
    MenuService.delete_menu_item(db, item_id)
    return None


@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    """Get all menu categories."""
    logger.info("Fetching menu categories")
    categories = MenuService.get_categories(db)
    return categories


# Menu Options Endpoints

@router.get("/options", response_model=List[MenuOptionResponse])
def get_all_menu_options(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get all menu options."""
    logger.info(f"Fetching menu options: skip={skip}, limit={limit}")
    options = MenuService.get_all_menu_options(db)
    return options[skip : skip + limit]


@router.get("/options/{option_id}", response_model=MenuOptionResponse)
def get_menu_option(
    option_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Get menu option by ID."""
    logger.info(f"Fetching menu option: {option_id}")
    option = MenuService.get_menu_option_by_id(db, option_id)
    return option


@router.post("/options", response_model=MenuOptionResponse, status_code=201)
def create_menu_option(
    option_create: MenuOptionCreate,
    db: Session = Depends(get_db),
):
    """Create new menu option."""
    logger.info(f"Creating menu option: {option_create.name}")
    option = MenuService.create_menu_option(db, option_create)
    return option


@router.put("/options/{option_id}", response_model=MenuOptionResponse)
def update_menu_option(
    option_id: int = Path(..., gt=0),
    option_update: MenuOptionUpdate = None,
    db: Session = Depends(get_db),
):
    """Update menu option."""
    logger.info(f"Updating menu option: {option_id}")
    option = MenuService.update_menu_option(db, option_id, option_update)
    return option


@router.delete("/options/{option_id}", status_code=204)
def delete_menu_option(
    option_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Delete menu option."""
    logger.info(f"Deleting menu option: {option_id}")
    MenuService.delete_menu_option(db, option_id)
    return None


# Option Choices Endpoints

@router.post("/options/{option_id}/choices", response_model=OptionChoiceResponse, status_code=201)
def create_option_choice(
    option_id: int = Path(..., gt=0),
    choice_create: OptionChoiceCreate = None,
    db: Session = Depends(get_db),
):
    """Create option choice."""
    logger.info(f"Creating option choice for option: {option_id}")
    choice = MenuService.create_option_choice(db, option_id, choice_create)
    return choice


@router.put("/choices/{choice_id}", response_model=OptionChoiceResponse)
def update_option_choice(
    choice_id: int = Path(..., gt=0),
    choice_data: dict = None,
    db: Session = Depends(get_db),
):
    """Update option choice."""
    logger.info(f"Updating option choice: {choice_id}")
    choice = MenuService.update_option_choice(db, choice_id, choice_data)
    return choice


@router.delete("/choices/{choice_id}", status_code=204)
def delete_option_choice(
    choice_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    """Delete option choice."""
    logger.info(f"Deleting option choice: {choice_id}")
    MenuService.delete_option_choice(db, choice_id)
    return None
