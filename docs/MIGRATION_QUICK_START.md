# Quick Migration Example (ตัวอย่างการใช้งานจริง)

## 📝 ตัวอย่าง: เพิ่ม Address Field ใน User Table

### 1️⃣ แก้ Model

```bash
vim app/models/user.py
```

เพิ่ม field ใหม่:
```python
class User(Base):
    # ... existing fields ...
    
    # 🆕 เพิ่มนี่
    address = Column(String(500), nullable=True)
    postal_code = Column(String(10), nullable=True)
```

### 2️⃣ สร้าง Migration

```bash
cd fast-api-ordering-app
make migrate-create
# พิมพ์: Add address and postal_code to users
```

### 3️⃣ Apply to Database

```bash
make migrate-up
```

✅ **เสร็จแล้ว!** Supabase database จะมี columns ใหม่ทันที

---

## 🚀 Quick Commands

```bash
# สร้าง migration
make migrate-create

# Apply migrations
make migrate-up

# Rollback
make migrate-down

# ดูสถานะ
make migrate-current

# ดู history
make migrate-history
```

---

## 🎯 สถานการณ์จริง

### เพิ่ม Table ใหม่ทั้งตัว

**1. สร้างไฟล์ `app/models/product.py`:**
```python
from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
```

**2. Import ใน `app/models/__init__.py`:**
```python
from app.models.product import Product

__all__ = [
    # ... existing
    "Product"
]
```

**3. Run:**
```bash
make migrate-create  # พิมพ์: Create products table
make migrate-up
```

✅ **Done!** มี table `products` บน Supabase แล้ว

---

## ⚠️ Important Notes

1. **ต้อง activate venv** ก่อน: `source ../venv/bin/activate`
2. **ต้องอยู่ใน `fast-api-ordering-app` folder**
3. **Review migration file** ก่อน apply ทุกครั้ง (อยู่ใน `alembic/versions/`)
4. **Backup database** ก่อน apply บน production

---

เปิดอ่านเพิ่มเติม: [DATABASE_MIGRATION_GUIDE.md](./DATABASE_MIGRATION_GUIDE.md)
