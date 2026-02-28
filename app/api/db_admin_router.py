"""
Database Admin Router - For managing database schema
SuperAdmin only endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from app.db.database import get_db
from app.models.user import User, UserRole
from app.services import user_service
from app.core.security import JWTService


router = APIRouter(prefix="/db-admin", tags=["Database Administration"])


def get_current_superadmin(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Verify current user is superadmin."""
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
    if not user or user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="SuperAdmin access required"
        )
    
    return user

router = APIRouter(prefix="/db-admin", tags=["Database Administration"])


@router.get("/tables", response_model=List[str])
async def list_tables(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db),
):
    """List all tables in the database"""
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    return tables


@router.get("/tables/{table_name}/schema")
async def get_table_schema(
    table_name: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db),
):
    """Get schema information for a specific table"""
    try:
        inspector = inspect(db.bind)
        
        # Check if table exists
        if table_name not in inspector.get_table_names():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table '{table_name}' not found"
            )
        
        columns = inspector.get_columns(table_name)
        primary_keys = inspector.get_pk_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)
        
        return {
            "table_name": table_name,
            "columns": columns,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys,
            "indexes": indexes,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting table schema: {str(e)}"
        )


@router.post("/tables/{table_name}/add-column")
async def add_column(
    table_name: str,
    column_name: str,
    column_type: str,
    nullable: bool = True,
    default_value: str | None = None,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db),
):
    """
    Add a new column to an existing table
    
    Example column types:
    - VARCHAR(255)
    - INTEGER
    - BOOLEAN
    - TIMESTAMP
    - TEXT
    - DECIMAL(10,2)
    """
    try:
        inspector = inspect(db.bind)
        
        # Check if table exists
        if table_name not in inspector.get_table_names():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table '{table_name}' not found"
            )
        
        # Check if column already exists
        existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
        if column_name in existing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Column '{column_name}' already exists in table '{table_name}'"
            )
        
        # Build ALTER TABLE statement
        null_constraint = "NULL" if nullable else "NOT NULL"
        default_clause = f"DEFAULT {default_value}" if default_value else ""
        
        alter_sql = f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_type} {null_constraint} {default_clause}
        """
        
        db.execute(text(alter_sql))
        db.commit()
        
        return {
            "success": True,
            "message": f"Column '{column_name}' added to table '{table_name}'",
            "table_name": table_name,
            "column_name": column_name,
            "column_type": column_type,
            "nullable": nullable,
            "default_value": default_value,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding column: {str(e)}"
        )


@router.post("/tables/create")
async def create_table(
    table_name: str,
    columns: List[Dict[str, Any]],
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db),
):
    """
    Create a new table
    
    columns format:
    [
        {
            "name": "id",
            "type": "INTEGER",
            "primary_key": true,
            "nullable": false,
            "auto_increment": true
        },
        {
            "name": "name",
            "type": "VARCHAR(255)",
            "nullable": false
        },
        {
            "name": "created_at",
            "type": "TIMESTAMP",
            "default": "CURRENT_TIMESTAMP"
        }
    ]
    """
    try:
        inspector = inspect(db.bind)
        
        # Check if table already exists
        if table_name in inspector.get_table_names():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table '{table_name}' already exists"
            )
        
        # Build column definitions
        column_defs = []
        for col in columns:
            col_name = col.get("name")
            col_type = col.get("type")
            
            if not col_name or not col_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each column must have 'name' and 'type'"
                )
            
            col_def = f"{col_name} {col_type}"
            
            if col.get("primary_key"):
                col_def += " PRIMARY KEY"
            
            if col.get("auto_increment"):
                # PostgreSQL uses SERIAL or BIGSERIAL
                if "INT" in col_type.upper():
                    col_def = col_def.replace(col_type, "SERIAL")
            
            if not col.get("nullable", True) and not col.get("primary_key"):
                col_def += " NOT NULL"
            
            if col.get("default"):
                col_def += f" DEFAULT {col['default']}"
            
            if col.get("unique"):
                col_def += " UNIQUE"
            
            column_defs.append(col_def)
        
        # Build CREATE TABLE statement
        create_sql = f"""
            CREATE TABLE {table_name} (
                {', '.join(column_defs)}
            )
        """
        
        db.execute(text(create_sql))
        db.commit()
        
        return {
            "success": True,
            "message": f"Table '{table_name}' created successfully",
            "table_name": table_name,
            "columns": columns,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating table: {str(e)}"
        )


@router.delete("/tables/{table_name}")
async def drop_table(
    table_name: str,
    confirm: bool = False,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db),
):
    """
    Drop (delete) a table - DANGEROUS!
    Requires confirm=true query parameter
    """
    if not confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please set confirm=true to drop the table"
        )
    
    try:
        inspector = inspect(db.bind)
        
        # Check if table exists
        if table_name not in inspector.get_table_names():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table '{table_name}' not found"
            )
        
        # Prevent dropping critical tables
        protected_tables = [
            "users", "permissions", "user_permissions", 
            "audit_logs", "menu_items", "orders"
        ]
        if table_name in protected_tables:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cannot drop protected table '{table_name}'"
            )
        
        drop_sql = f"DROP TABLE {table_name}"
        db.execute(text(drop_sql))
        db.commit()
        
        return {
            "success": True,
            "message": f"Table '{table_name}' dropped successfully",
            "table_name": table_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error dropping table: {str(e)}"
        )


@router.get("/tables/{table_name}/data")
async def get_table_data(
    table_name: str,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db),
):
    """Get data from a table (for preview)"""
    try:
        inspector = inspect(db.bind)
        
        # Check if table exists
        if table_name not in inspector.get_table_names():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table '{table_name}' not found"
            )
        
        # Query data
        query = f"SELECT * FROM {table_name} LIMIT :limit OFFSET :offset"
        result = db.execute(text(query), {"limit": limit, "offset": offset})
        
        # Get column names
        columns = result.keys()
        
        # Convert rows to dictionaries
        rows = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Convert datetime to string for JSON serialization
                if isinstance(value, datetime):
                    value = value.isoformat()
                row_dict[col] = value
            rows.append(row_dict)
        
        # Get total count
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        total_count = db.execute(text(count_query)).scalar()
        
        return {
            "table_name": table_name,
            "columns": list(columns),
            "data": rows,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting table data: {str(e)}"
        )
