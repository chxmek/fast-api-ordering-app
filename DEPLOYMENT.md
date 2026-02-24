# FastAPI Deployment Guide

## ✅ Deploy to Railway (Recommended - Free $5/month)

### Step 1: Prepare Repository
```bash
cd /Users/mekchawanwit/Desktop/Dev/ordering_fls_app
git add .
git commit -m "feat: add deployment configuration"
git push
```

### Step 2: Deploy on Railway

1. **Sign up**: https://railway.app (use GitHub account)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select `back-end/fastapi-ordering` folder

3. **Configure Environment Variables**:
   Click "Variables" tab and add:
   ```
   DATABASE_URL=postgresql://postgres.dilmwrcfffkpdlmrzmze:Mm6229744%21%40@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?options=-csearch_path%3Dpublic
   
   SECRET_KEY=your-secret-key-change-in-production-min-32-chars-long-key-12345
   
   DEBUG=False
   
   CORS_ORIGINS=["https://your-frontend-domain.com","http://localhost:3000"]
   ```

4. **Set Root Directory** (if needed):
   - Settings → General
   - Root Directory: `back-end/fastapi-ordering`

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your deployed URL: `https://your-app.railway.app`

### Step 3: Test Deployment
```bash
curl https://your-app.railway.app/docs
```

---

## 🔧 Alternative: Deploy to Render (Free tier)

### Step 1: Create render.yaml
Already included in project

### Step 2: Deploy on Render

1. **Sign up**: https://render.com (use GitHub)

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select your repo

3. **Configure**:
   - Name: `ordering-api`
   - Root Directory: `back-end/fastapi-ordering`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   Same as Railway above

5. **Deploy**: Click "Create Web Service"

---

## 🐳 Alternative: Deploy with Docker

### Using Railway/Render with Dockerfile
Just push - it will auto-detect Dockerfile

### Manual Docker Deploy
```bash
# Build
docker build -t ordering-api .

# Run locally
docker run -p 8000:8000 --env-file .env ordering-api

# Push to registry (Docker Hub, GCR, etc.)
docker tag ordering-api username/ordering-api:latest
docker push username/ordering-api:latest
```

---

## 📋 Post-Deployment Checklist

- [ ] API accessible at public URL
- [ ] /docs endpoint working
- [ ] Database connection successful
- [ ] CORS configured for frontend
- [ ] Environment variables set
- [ ] SSL/HTTPS enabled (auto on Railway/Render)
- [ ] Update frontend API_BASE_URL

---

## 🔒 Security Notes

1. **Never commit .env** - Already in .gitignore
2. **Use strong SECRET_KEY** in production
3. **Set DEBUG=False** in production
4. **Limit CORS_ORIGINS** to your frontend only
5. **Use HTTPS only** (enforced by Railway/Render)

---

## 💰 Cost Estimates

**Railway Free Tier:**
- $5 credit/month
- Enough for ~100 hours runtime
- Sleep after inactivity (free tier)

**Render Free Tier:**
- Free forever
- Auto-sleep after 15 min inactivity
- Slower cold starts

**Recommendation:**
- Development: Render (free)
- Production: Railway ($5-20/month)

---

## 🚀 Quick Deploy Commands

```bash
# 1. Commit changes
git add .
git commit -m "feat: ready for deployment"
git push

# 2. Go to Railway/Render dashboard
# 3. Connect GitHub repo
# 4. Add environment variables
# 5. Deploy!

# Your API will be live at:
# https://your-app.railway.app
# or
# https://your-app.onrender.com
```

---

## 📞 Update Flutter App

After deployment, update Flutter app:

```dart
// lib/services/api_client.dart
class ApiClient {
  static const String baseUrl = 'https://your-app.railway.app/api/v1';
  // Change from: http://127.0.0.1:8001/api/v1
}
```

---

## ✅ Done!

Your backend is now:
- ✅ Running on cloud
- ✅ Using Supabase database
- ✅ Accessible from anywhere
- ✅ Auto-scaling
- ✅ HTTPS enabled
