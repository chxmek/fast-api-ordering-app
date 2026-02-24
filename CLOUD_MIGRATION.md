# Cloud Database Migration Guide

## Step 1: Create Supabase Account

1. ไปที่ https://supabase.com
2. Sign up ด้วย GitHub account (แนะนำ)
3. คลิก "New Project"
4. กรอกข้อมูล:
   - Project name: `ordering-fls-app`
   - Database Password: (สร้าง strong password - เก็บไว้!)
   - Region: Singapore (ใกล้ที่สุด)
5. รอ ~2 นาที ให้ project สร้างเสร็จ

## Step 2: Get Connection String

1. ไปที่ Project Settings → Database
2. คัดลอก "Connection string" → "URI"
   
   ตัวอย่าง:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijk.supabase.co:5432/postgres
   ```

3. แทนที่ `[YOUR-PASSWORD]` ด้วย password จริง

## Step 3: Migration Options

### Option A: Backup & Restore (แนะนำ)
```bash
# 1. Backup local database
./backup_db.sh

# 2. Restore to cloud
gunzip -c backups/ordering_db_YYYYMMDD_HHMMSS.sql.gz | \
  psql "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
```

### Option B: Use pg_dump direct
```bash
pg_dump -U mek -d ordering_db | \
  psql "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
```

### Option C: Supabase Migration Tool
```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Link project
supabase link --project-ref YOUR_PROJECT_REF

# Push migrations
supabase db push
```

## Step 4: Update Environment Variables

Update `.env` file:
```env
# Old (local)
# DATABASE_URL="postgresql://mek:123456@localhost/ordering_db"

# New (Supabase)
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
```

## Step 5: Test Connection

```bash
cd back-end/fastapi-ordering
source venv/bin/activate
python -c "from app.db.database import engine; print('✅ Connected!' if engine else '❌ Failed')"
```

## Step 6: Run Application

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

## Troubleshooting

### Error: SSL required
Update connection string:
```
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres?sslmode=require"
```

### Error: Connection timeout
- ตรวจสอบ firewall
- ตรวจสอบว่า password ถูกต้อง
- ลองเปลี่ยน region

### Performance issues
- Enable connection pooling: `?pgbouncer=true`
- ใช้ Supabase connection pooler

## Security Best Practices

1. ใช้ environment variables แทน hardcode
2. ไม่ commit `.env` ใน git
3. ใช้ different passwords สำหรับ dev/prod
4. Enable SSL connection เสมอ

## Cost Estimation

**Supabase Free Tier:**
- 500 MB database storage
- Unlimited API requests
- 2 GB bandwidth
- 50 MB file storage

**เมื่อโตเกิน Free tier:**
- Pro plan: $25/month
- 8 GB database
- 250 GB bandwidth
