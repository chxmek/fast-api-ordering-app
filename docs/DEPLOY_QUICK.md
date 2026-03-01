# 🚀 Deploy FastAPI Backend - Quick Guide

## ตัวเลือกที่ 1: Railway (แนะนำ - ง่ายที่สุด)

### ขั้นตอน:

1. **Push code ขึ้น GitHub**:
   ```bash
   git push origin main
   ```

2. **ไปที่ Railway**: https://railway.app
   - Sign up ด้วย GitHub
   - Click "New Project"
   - เลือก "Deploy from GitHub repo"
   - เลือก repository ของคุณ
   - Root Directory: `back-end/fastapi-ordering`

3. **เพิ่ม Environment Variables**:
   ใน Railway Dashboard → Variables tab:
   ```
   DATABASE_URL=postgresql://postgres.dilmwrcfffkpdlmrzmze:Mm6229744%21%40@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?options=-csearch_path%3Dpublic
   
   SECRET_KEY=your-secret-key-min-32-chars
   DEBUG=False
   ```

4. **Deploy**: กด "Deploy" รอ 2-3 นาที

5. **ทดสอบ**: เปิด `https://your-app.railway.app/docs`

---

## ตัวเลือกที่ 2: Render (Free ตลอดกาล)

1. **ไปที่ Render**: https://render.com
   - Sign up ด้วย GitHub
   - New → Web Service
   - Connect repository

2. **Configure**:
   - Name: `ordering-api`
   - Root Directory: `back-end/fastapi-ordering`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**: เหมือน Railway

4. **Deploy**: Create Web Service

---

## 🔑 Environment Variables ที่ต้องตั้ง:

```bash
DATABASE_URL=postgresql://postgres.dilmwrcfffkpdlmrzmze:Mm6229744%21%40@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?options=-csearch_path%3Dpublic

SECRET_KEY=your-production-secret-key-min-32-chars

DEBUG=False

CORS_ORIGINS=["https://your-frontend.com"]
```

---

## ✅ หลัง Deploy แล้ว:

1. **ทดสอบ API**:
   ```bash
   curl https://your-app.railway.app/docs
   ```

2. **Update Flutter app** - เปลี่ยน API URL:
   ```dart
   // lib/services/api_client.dart
   static const String baseUrl = 'https://your-app.railway.app/api/v1';
   ```

3. **ทดสอบ login จาก Flutter app**

---

## 💰 ค่าใช้จ่าย:

- **Railway**: $5 free credit/เดือน (พอใช้งาน development)
- **Render**: Free ตลอดกาล (แต่จะ sleep หลัง 15 นาที idle)

---

## 🆘 ถ้ามีปัญหา:

1. เช็ค logs ใน Railway/Render dashboard
2. ตรวจสอบ Environment Variables
3. ทดสอบ DATABASE_URL ใน local ก่อน
4. อ่าน DEPLOYMENT.md สำหรับรายละเอียดเพิ่มเติม
