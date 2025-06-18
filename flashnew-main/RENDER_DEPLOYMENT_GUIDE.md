# Render Deployment Guide for FLASH

## 🚀 Quick Deploy Instructions

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (use FlashDemo8789 account)
4. Authorize Render to access your repositories

### Step 2: Deploy Using render.yaml (Easiest Method)
1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your GitHub repository (FlashDemo8789/flashnew)
3. Render will detect the `render.yaml` file
4. Click "Apply" to create all services automatically
5. Wait 10-15 minutes for deployment

### Step 3: Get Your URLs
After deployment, you'll have:
- Backend: `https://flash-backend.onrender.com`
- Frontend: `https://flash-frontend.onrender.com`

## 📋 Manual Deployment (Alternative Method)

### Deploy Backend Service
1. Click "New +" → "Web Service"
2. Connect GitHub repo: FlashDemo8789/flashnew
3. Configure:
   - Name: `flash-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python api_server_unified.py`
4. Set Environment Variables:
   ```
   PORT=10000
   DISABLE_AUTH=true
   DEEPSEEK_API_KEY=sk-f68b7148243e4663a31386a5ea6093cf
   DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
   MODEL_PATH=./models/production_v45_fixed
   ENABLE_PATTERN_SYSTEM=true
   LOG_LEVEL=INFO
   ```
5. Click "Create Web Service"

### Deploy Frontend Service
1. Click "New +" → "Web Service"
2. Connect same GitHub repo
3. Configure:
   - Name: `flash-frontend`
   - Root Directory: `flash-frontend-apple`
   - Environment: `Node`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm start`
4. Set Environment Variables:
   ```
   PORT=3000
   REACT_APP_API_URL=https://flash-backend.onrender.com
   ```
5. Click "Create Web Service"

## 🔍 Important Notes

### Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 512MB RAM limit (upgrade to paid for 4GB)
- Perfect for testing with users!

### When to Upgrade
Upgrade to paid plan ($7/month per service) when:
- You need services always running (no sleep)
- You need more than 512MB RAM
- You have consistent user traffic

### Monitoring Your App
1. Check service logs in Render dashboard
2. Monitor metrics (CPU, Memory, Response time)
3. Set up health checks for alerts

## 🎯 Testing Your Deployment

1. **Backend Health Check**:
   ```
   https://flash-backend.onrender.com/health
   ```

2. **Frontend Access**:
   ```
   https://flash-frontend.onrender.com
   ```

3. **Test Flow**:
   - Click "Get Started"
   - Use autofill to populate test data
   - Complete assessment
   - Verify results appear

## 🐛 Troubleshooting

### Backend Issues
- Check logs for Python errors
- Verify all dependencies in requirements.txt
- Ensure models directory exists
- Check environment variables are set

### Frontend Issues
- Verify REACT_APP_API_URL is correct
- Check for build errors in logs
- Ensure all npm dependencies installed

### Connection Issues
- Backend must be deployed first
- Frontend needs correct backend URL
- Check CORS settings if requests fail

## 📈 Next Steps

1. **Share with testers**: 
   - Frontend URL: `https://flash-frontend.onrender.com`
   - Tell them to use autofill for quick testing

2. **Monitor usage**:
   - Watch service metrics
   - Check logs for errors
   - Gather user feedback

3. **Optimize**:
   - Upgrade RAM if needed ($7/month)
   - Add custom domain later
   - Enable auto-scaling when growing

## 🔗 Useful Links
- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Service Logs: Available in each service's dashboard
- Metrics: Built into Render dashboard

---

**Remember**: The free tier is perfect for user testing! Services will wake up when users access them (just takes ~30 seconds for first request).