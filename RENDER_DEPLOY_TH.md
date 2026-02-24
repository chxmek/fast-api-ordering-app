# วิธี Deploy FastAPI Backend ลง Render (ฟรี)

## ขั้นตอนที่ 1: เตรียม Render Account

1. ไปที่ https://render.com
2. คลิก **Get Started** หรือ **Sign Up**
3. เลือก **Sign up with GitHub** (แนะนำ - เชื่อมต่อง่ายที่สุด)
4. Authorize Render ให้เข้าถึง GitHub repositories ของคุณ

---

## ขั้นตอนที่ 2: สร้าง Web Service

1. ใน Render Dashboard คลิก **New +** (มุมบนขวา)
2. เลือก **Web Service**
3. เชื่อมต่อ GitHub repository:
   - คลิก **+ Connect account** (ถ้ายังไม่ได้เชื่อม)
   - หรือเลือก repo จากรายการ: `chxmek/fast-api-ordering-app`
   - คลิก **Connect**

---

## ขั้นตอนที่ 3: ตั้งค่า Web Service

กรอกข้อมูลดังนี้:

### Basic Settings:
- **Name**: `fast-api-ordering-app` (หรือชื่ออื่นที่ต้องการ)
- **Region**: `Singapore` (ใกล้ไทยที่สุด)
- **Branch**: `main`
- **Root Directory**: ปล่อยว่างไว้ (เพราะ repo เป็น backend อย่างเดียว)
- **Runtime**: `Python 3`

### Build & Deploy Settings:
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### Instance Type:
- เลือก **Free** (ฟรี - มีข้อจำกัดว่าจะหยุดทำงานหลังไม่มีคนใช้ 15 นาที)

---

## ขั้นตอนที่ 4: ตั้งค่า Environment Variables

คลิก **Advanced** แล้วเพิ่ม Environment Variables ต่อไปนี้:

### ตัวแปรที่จำเป็น:

1. **DATABASE_URL**
   ```
   postgresql://postgres.dilmwrcfffkpdlmrzmze:Mm6229744%21%40@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?options=-csearch_path%3Dpublic
   ```
   *(นี่คือ Supabase database ที่คุณใช้อยู่)*

2. **SECRET_KEY**
   ```
   your-secret-key-here-change-this-to-random-string
   ```
   *(ควรสร้างใหม่ด้วยคำสั่ง: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

3. **DEBUG**
   ```
   False
   ```

4. **ENVIRONMENT** (optional)
   ```
   production
   ```

### วิธีเพิ่ม Environment Variables:
- คลิก **Add Environment Variable**
- กรอก Key และ Value
- ทำซ้ำสำหรับแต่ละตัวแปร

---

## ขั้นตอนที่ 5: Deploy

1. ตรวจสอบข้อมูลทั้งหมดให้ถูกต้อง
2. คลิก **Create Web Service** (ปุ่มสีน้ำเงินด้านล่าง)
3. Render จะเริ่ม build และ deploy โดยอัตโนมัติ
4. รอประมาณ **5-10 นาที** (ครั้งแรก)

### ติดตามสถานะ:
- ดู **Logs** tab เพื่อเช็คว่า build สำเร็จหรือไม่
- ถ้าเห็นข้อความ `Application startup complete` แปลว่าสำเร็จ

---

## ขั้นตอนที่ 6: ทดสอบ API

หลัง deploy สำเร็จ Render จะให้ URL เช่น:
```
https://fast-api-ordering-app.onrender.com
```

### ทดสอบ endpoints:

1. **API Docs (Swagger UI)**:
   ```
   https://fast-api-ordering-app.onrender.com/docs
   ```

2. **Health Check**:
   ```bash
   curl https://fast-api-ordering-app.onrender.com/health
   ```

3. **API Base**:
   ```
   https://fast-api-ordering-app.onrender.com/api/v1
   ```

---

## ข้อจำกัดของ Free Tier

⚠️ **สิ่งที่ต้องรู้:**

1. **Cold Start**: หยุดทำงานหลังไม่มีคนใช้ 15 นาที
   - ครั้งแรกที่เปิดจะช้า 30-60 วินาที (กำลัง wake up)
   - ไม่เหมาะกับ production จริงๆ แต่ดีสำหรับ demo/testing

2. **Performance**: 
   - CPU/RAM จำกัด
   - ถ้าต้องการเร็วขึ้น อัพเกรดเป็น Paid plan ($7/เดือน)

3. **Database**: 
   - Supabase ของคุณทำงานตลอด (ไม่หยุด)
   - เฉพาะ Render API ที่จะหยุด

---

## ขั้นตอนที่ 7: อัพเดท Flutter App

หลังได้ production URL แล้ว ต้องแก้ Flutter app ให้ชี้ไปที่ URL ใหม่:

### แก้ไฟล์: `lib/repositories/api_client.dart` (หรือที่เก็บ base URL)

เปลี่ยนจาก:
```dart
static const String baseUrl = 'http://127.0.0.1:8001/api/v1';
```

เป็น:
```dart
static const String baseUrl = 'https://fast-api-ordering-app.onrender.com/api/v1';
```

**หรือ** ใช้ Environment Variables ใน Flutter:
```dart
static const String baseUrl = String.fromEnvironment(
  'API_URL',
  defaultValue: 'http://127.0.0.1:8001/api/v1', // dev
);
```

แล้ว build Flutter app ด้วย:
```bash
flutter build apk --dart-define=API_URL=https://fast-api-ordering-app.onrender.com/api/v1
```

---

## Auto Deploy (Optional)

Render จะ auto-deploy ทุกครั้งที่คุณ push code ใหม่ขึ้น GitHub branch `main`

วิธีปิด auto-deploy (ถ้าไม่ต้องการ):
1. ไปที่ Settings → Build & Deploy
2. ปิด **Auto-Deploy**

---

## Troubleshooting

### ถ้า Deploy ไม่สำเร็จ:

1. **เช็ค Logs**:
   - ไปที่ tab **Logs**
   - ดูข้อความ error สีแดง

2. **ปัญหาที่พบบ่อย**:
   - `ModuleNotFoundError`: ลืมใส่ package ใน `requirements.txt`
   - `Connection refused`: ตรวจสอบ `DATABASE_URL` ว่าถูกต้อง
   - `Port already in use`: ตรวจสอบ start command ว่าใช้ `$PORT` (ต้องมี `$`)

3. **ลอง Manual Deploy**:
   - ไปที่ tab **Manual Deploy**
   - คลิก **Deploy latest commit**

---

## เช็ค Environment Variables หลัง Deploy

```bash
# ในหน้า Render Dashboard
Settings → Environment → Environment Variables
```

ตรวจสอบว่า:
- ✅ `DATABASE_URL` มี Supabase connection string
- ✅ `SECRET_KEY` ไม่ใช่ default value
- ✅ `DEBUG` = `False`

---

## คำสั่งที่เป็นประโยชน์

### สร้าง SECRET_KEY ใหม่:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### ทดสอบ local ก่อน deploy:
```bash
cd /Users/mekchawanwit/Desktop/Dev/ordering_fls_app/ordering-fls-backend
source venv/bin/activate
DEBUG=False uvicorn main:app --host 0.0.0.0 --port 8000
```

### Test production database connection:
```bash
python test_db.py
```

---

## สรุป

1. ✅ Sign up Render ด้วย GitHub
2. ✅ Connect repo: `chxmek/fast-api-ordering-app`
3. ✅ ตั้งค่า: Python 3, Build/Start commands
4. ✅ เพิ่ม Environment Variables (DATABASE_URL, SECRET_KEY, DEBUG)
5. ✅ คลิก **Create Web Service**
6. ✅ รอ 5-10 นาที
7. ✅ ทดสอบที่ `/docs`
8. ✅ อัพเดท Flutter app ให้ชี้ไปที่ production URL

---

## Support

ถ้าติดปัญหา:
- ดู Render Logs: https://dashboard.render.com/
- เช็ค GitHub repo: https://github.com/chxmek/fast-api-ordering-app
- Render Docs: https://render.com/docs/deploy-fastapi

---

**เริ่มได้เลย!** 🚀
