## 🔍 วิธีหา Connection String ที่ถูกต้องจาก Supabase

### ขั้นตอนที่ 1: เข้า Supabase Dashboard
1. เปิดเว็บ: https://supabase.com
2. Login เข้าบัญชีของคุณ
3. คลิกเลือก Project ที่สร้างไว้

### ขั้นตอนที่ 2: หา Connection String
1. ที่ Dashboard ด้านซ้าย คลิก **⚙️ Project Settings** (ไอคอนเฟือง)
2. เลือกแท็บ **Database**
3. scroll ลงมาจนเจอ section **Connection string**
4. เลือก mode: **URI** (ไม่ใช่ Session mode)
5. คัดลอก connection string ทั้งหมด

### ขั้นตอนที่ 3: แทนที่ Password
Connection string จะมีหน้าตาประมาณนี้:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

คุณต้อง:
1. แทนที่ `[YOUR-PASSWORD]` ด้วย: `Mm6229744%21%40` (password ที่ encode แล้ว)
2. เก็บ `@db.xxxxxxxxxxxxx.supabase.co` ไว้ตามที่ได้จาก Dashboard (ไม่ใช่ YOUR_ACTUAL_PROJECT_ID)

### ตัวอย่างที่ถูกต้อง:
```bash
# ถ้า Supabase ให้ connection string:
postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijk.supabase.co:5432/postgres

# คุณต้องเปลี่ยนเป็น:
postgresql://postgres:Mm6229744%21%40@db.abcdefghijk.supabase.co:5432/postgres
```

### ✅ วิธีทดสอบ Connection String ก่อน Migrate:

```bash
# รันคำสั่งนี้ (แทนที่ด้วย connection string จริง):
psql 'postgresql://postgres:Mm6229744%21%40@db.xxxxx.supabase.co:5432/postgres' -c "SELECT version();"

# ถ้าเชื่อมต่อได้ จะแสดง PostgreSQL version
# ถ้าเชื่อมต่อไม่ได้ จะแสดง error
```

### 🚨 สิ่งที่ต้องเช็ค:
- ✅ Project status เป็น "Active" (สีเขียว) ใน Supabase Dashboard
- ✅ Database password ถูกต้อง (ตรงกับตอนสร้าง project)
- ✅ ไม่มี space หรือ newline ใน connection string
- ✅ ใช้ %21%40 แทน !@ ใน password

### 💡 ถ้ายังไม่ได้:
1. ลอง reset database password ใหม่ใน Supabase Dashboard
2. ใช้ password ที่ไม่มีตัวอักษรพิเศษ (เช่น `Password123456`)
3. ลอง copy connection string ใหม่อีกครั้ง
