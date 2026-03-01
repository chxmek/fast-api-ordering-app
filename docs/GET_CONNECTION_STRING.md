## 📍 วิธีหา Database Connection String ที่ถูกต้อง

### ขั้นตอนที่ถูกต้อง 100%:

1. **เข้า Supabase Dashboard**: https://supabase.com/dashboard/project/dilmwrcfffkpdlmrzmze

2. **คลิกที่เมนูซ้าย → Project Settings** (ไอคอนเฟือง ⚙️)

3. **คลิกแท็บ "Database"** (ไม่ใช่ API!)

4. **Scroll ลงมาหา section "Connection string"**

5. **เลือก "URI" mode** (มี toggle ให้เลือก)

6. **คัดลอก connection string ทั้งหมด**
   - จะขึ้นต้นด้วย `postgresql://postgres`
   - มี `[YOUR-PASSWORD]` อยู่ในนั้น

7. **แทนที่ `[YOUR-PASSWORD]` ด้วย password จริง**

### ตัวอย่าง Connection String ที่อาจได้รับ:

**แบบที่ 1 (Transaction mode):**
```
postgresql://postgres:[YOUR-PASSWORD]@db.dilmwrcfffkpdlmrzmze.supabase.co:5432/postgres
```

**แบบที่ 2 (Session mode - พอร์ต 6543):**
```
postgresql://postgres:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

**แบบที่ 3 (Connection pooling):**
```
postgresql://postgres.dilmwrcfffkpdlmrzmze:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
```

### วิธีแทนที่ Password:

ถ้า connection string เป็น:
```
postgresql://postgres:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

และ password ของคุณคือ `Mm6229744!@`

ให้เปลี่ยนเป็น:
```
postgresql://postgres:Mm6229744%21%40@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

### ทดสอบ Connection:

หลังได้ connection string แล้ว รันคำสั่งนี้:
```bash
psql 'CONNECTION_STRING_ของคุณ' -c "SELECT version();"
```

ถ้าเชื่อมต่อสำเร็จ จะแสดง PostgreSQL version

### 🚨 สิ่งสำคัญ:
- ใช้ **single quotes** `'...'` คลุม connection string
- แทนที่ `!` ด้วย `%21` และ `@` ด้วย `%40`
- ตรวจสอบว่า password ถูกต้อง (ตรงกับตอนสร้าง project)
- Hostname ต้องเป็น `aws-...pooler.supabase.com` หรือ `db...supabase.co`
- Port อาจเป็น 5432 หรือ 6543

### ถ้ายังไม่ได้:
ลอง reset database password ใหม่:
1. Settings → Database
2. Scroll ลงไปหา "Database Password"
3. คลิก "Reset database password"
4. ใส่ password ใหม่: `SimplePassword123` (ไม่มีตัวพิเศษ)
5. Copy connection string ใหม่
