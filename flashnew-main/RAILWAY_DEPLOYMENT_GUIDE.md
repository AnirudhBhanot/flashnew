# Railway Deployment Guide for FLASH

## Quick Deploy Steps

### Step 1: Login to Railway
1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway to access your GitHub

### Step 2: Create New Project
1. Click "New Project" button
2. Select "Deploy from GitHub repo"
3. Search for "flashnew" and select your repository
4. Railway will automatically detect the services

### Step 3: Configure Backend Service
1. Click on the backend service
2. Go to "Variables" tab
3. Click "Raw Editor"
4. Paste this entire block:

```
PORT=8001
PYTHONUNBUFFERED=1
DISABLE_AUTH=true
DEEPSEEK_API_KEY=sk-f68b7148243e4663a31386a5ea6093cf
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
MODEL_PATH=./models/production_v45_fixed
ENABLE_PATTERN_SYSTEM=true
LOG_LEVEL=INFO
```

5. Click "Save"

### Step 4: Configure Frontend Service
1. Click on the frontend service
2. Go to "Variables" tab
3. Add these variables:
   - `PORT` = `3000`
   - `REACT_APP_API_URL` = Copy the backend service URL (shown in backend service settings)

### Step 5: Deploy
1. Both services should start deploying automatically
2. Wait for both to show "Success" status (5-10 minutes)
3. Click on frontend service URL to access your app

## Alternative: One-Click Deploy

I've prepared a template that can deploy everything automatically:

1. Click this link: [Deploy on Railway](https://railway.app/new/template?template=https://github.com/FlashDemo8789/flashnew)
2. Click "Deploy Now"
3. Wait for deployment to complete

## Service URLs
After deployment, you'll get URLs like:
- Backend: `https://flashnew-production-backend.up.railway.app`
- Frontend: `https://flashnew-production-frontend.up.railway.app`

## Troubleshooting

### If backend fails to start:
1. Check logs in Railway dashboard
2. Ensure all Python dependencies are in requirements.txt
3. Verify PORT environment variable is set

### If frontend fails to build:
1. Check if node_modules are being installed
2. Verify REACT_APP_API_URL is set correctly
3. Check build logs for any missing dependencies

### If services can't connect:
1. Make sure REACT_APP_API_URL points to backend public URL
2. Check CORS settings in backend
3. Ensure both services are running

## Quick Commands (if using Railway CLI)

```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Link to existing project
railway link

# View logs
railway logs

# Add environment variable
railway variables set KEY=value

# Redeploy
railway up
```

## Environment Variables Reference

### Backend (.env)
```
PORT=8001
PYTHONUNBUFFERED=1
DISABLE_AUTH=true
DEEPSEEK_API_KEY=sk-f68b7148243e4663a31386a5ea6093cf
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
MODEL_PATH=./models/production_v45_fixed
ENABLE_PATTERN_SYSTEM=true
LOG_LEVEL=INFO
```

### Frontend (.env)
```
PORT=3000
REACT_APP_API_URL=https://[BACKEND_URL].railway.app
```

## Post-Deployment Checklist

- [ ] Backend health check works: `https://[backend-url]/health`
- [ ] Frontend loads without errors
- [ ] Can complete assessment flow
- [ ] API predictions return results
- [ ] Deep Dive analysis works
- [ ] All navigation works correctly

## Custom Domain (Optional)

1. Go to service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as shown
5. Wait for SSL certificate (automatic)

---

**Note**: This deployment will use Railway's free tier initially. You may need to upgrade for production use with higher traffic.