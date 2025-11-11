# Deployment Guide - Render.com

Complete guide to deploy Architecture Patterns Playground to Render.com

---

## 🚀 One-Click Deployment

The project is configured for **Blueprint deployment** on Render.com, which means all **9 services** can be deployed with just a few clicks.

### Services That Will Be Deployed

**Core Services:**
1. **Learning Platform** - `architecture-playground.onrender.com`
2. **Task Manager UI** - `architecture-playground-ui.onrender.com`

**Architecture Pattern Services (All 6 implementations):**
3. **Monolithic** - `arch-monolith.onrender.com`
4. **Modular Monolith** - `arch-modular-monolith.onrender.com`
5. **Microservices Gateway** - `arch-microservices-gateway.onrender.com`
6. **Microservices Task Service** - `arch-microservices-task-service.onrender.com`
7. **Event-Driven** - `arch-event-driven.onrender.com`
8. **Layered** - `arch-layered.onrender.com`
9. **Service-Based** - `arch-service-based.onrender.com`

### Free Tier Considerations

- **Total Services**: 9 web services
- **Free Hours**: 750 hours/month across all services
- **Spin-Down**: Services sleep after 15 minutes of inactivity
- **Wake-Up Time**: ~30 seconds for first request after sleep
- **Cost**: $0/month (free tier) or upgrade critical services to $7/month each

---

## 📋 Pre-Deployment Checklist

### ✅ Step 1: Push Code to GitHub

Make sure all your latest changes are pushed:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main  # or your main branch name
```

### ✅ Step 2: Verify `render.yaml` Exists

The `render.yaml` file in the root directory contains all deployment configuration. It defines 9 services:
- **Core**: Learning Platform, Task Manager UI
- **Architectures**: All 6 pattern implementations (Monolith, Modular Monolith, Microservices x2, Event-Driven, Layered, Service-Based)

### ✅ Step 3: Choose Deployment Option

You have three deployment options:

**Option 1 (Recommended): Deploy All Services**
- Complete educational experience with all 6 architecture patterns
- Uses ~9 services on free tier (may experience spin-down)
- Best for: Portfolio showcase, comprehensive learning

**Option 2 (Minimal): Deploy Core + 2-3 Patterns**
- Comment out unwanted services in `render.yaml`
- Lower resource usage, faster wake-up times
- Best for: Testing, focused learning on specific patterns

**Option 3 (Production): Upgrade Critical Services**
- Deploy all on free tier, upgrade 2-3 critical services to paid ($7/mo each)
- Recommended paid services: Learning Platform, Task Manager UI
- Best for: Live demos, always-available portfolio

---

## 🌐 Deployment Steps

### Option A: Deploy via Render Dashboard (Easiest)

1. **Sign up / Log in to Render.com**
   - Visit https://render.com
   - Sign up with GitHub (recommended)
   - No credit card required for free tier

2. **Create New Blueprint**
   - Click **"New +"** button
   - Select **"Blueprint"**
   - Connect your GitHub account (if not already)
   - Select the `architecture-playground` repository
   - Choose the branch to deploy (e.g., `main`)

3. **Review Services**
   - Render will detect `render.yaml` automatically
   - Review the 9 services that will be created:
     - `architecture-playground` (Learning Platform)
     - `architecture-playground-ui` (Task Manager UI)
     - `arch-monolith` (Monolithic Architecture)
     - `arch-modular-monolith` (Modular Monolith)
     - `arch-microservices-gateway` (Microservices Gateway)
     - `arch-microservices-task-service` (Microservices Task Service)
     - `arch-event-driven` (Event-Driven Architecture)
     - `arch-layered` (Layered Architecture)
     - `arch-service-based` (Service-Based Architecture)

4. **Deploy**
   - Click **"Apply"**
   - Render will start building and deploying all 9 services
   - This takes 15-20 minutes for first deployment (9 services building in parallel)

5. **Monitor Deployment**
   - Watch the build logs for each service
   - First deployment always takes longer
   - All services should show "Live" status when complete
   - Note: Services may take 30-60 seconds to respond initially

---

### Option B: Deploy via Render CLI

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy blueprint
render blueprint launch
```

---

## 🔗 Your Live URLs

After deployment completes, your services will be available at:

### Learning Platform (Main Website)
```
https://architecture-playground.onrender.com
```
- Homepage with architecture cards
- Pattern comparison pages
- Links to API and UI

### Monolith API (Backend)
```
https://architecture-playground-api.onrender.com
https://architecture-playground-api.onrender.com/docs
```
- REST API with 6 endpoints
- Interactive Swagger UI documentation
- CORS-enabled for UI

### Task Manager UI (Interactive Demo)
```
https://architecture-playground-ui.onrender.com
```
- Interactive task management
- Architecture selector
- Real-time performance metrics

---

## ⚙️ Environment Variables

The services use these environment variables (automatically set by `render.yaml`):

### Learning Platform
- `PYTHON_VERSION: 3.11.0`
- `API_URL: https://architecture-playground-api.onrender.com`
- `UI_URL: https://architecture-playground-ui.onrender.com`

### Monolith API
- `PYTHON_VERSION: 3.11.0`
- `CORS_ORIGINS: https://architecture-playground-ui.onrender.com,https://architecture-playground.onrender.com`

### Task Manager UI
- No environment variables (static site)
- URLs are auto-detected based on hostname

---

## 🔄 Auto-Deploy from GitHub

All services are configured with `autoDeploy: true`, which means:

✅ **Push to GitHub** → Render automatically rebuilds and deploys
✅ **No manual steps** → Just commit and push
✅ **See deploy status** → In Render dashboard

### To Trigger a Deployment

```bash
# Make changes
git add .
git commit -m "Update feature X"
git push origin main

# Render automatically detects and deploys!
```

---

## 🆓 Free Tier Limitations

### What You Get (FREE)

- ✅ 750 hours/month web service time
- ✅ 100 GB bandwidth/month
- ✅ Unlimited static sites
- ✅ SSL/HTTPS included
- ✅ Custom domains (optional)

### Limitations

- ⏱️ **Services spin down** after 15 minutes of inactivity
- ⏱️ **Cold start**: 30-60 seconds for first request after sleep
- 💾 **512 MB RAM** per service
- 💾 **SQLite database** resets on service restart (ephemeral disk)

### What This Means

- **For Portfolio**: Perfect! Works great for demos
- **For Production**: Upgrade to paid tier for always-on ($7/month per service)

---

## ⚡ Upgrading to Paid Tier

To eliminate cold starts and get better performance:

1. Go to service dashboard
2. Click **"Upgrade to Paid"**
3. Select **Starter plan** ($7/month)
4. Benefits:
   - Always-on (no sleep)
   - Faster response times
   - More RAM (512MB → 2GB+)
   - Persistent disk for SQLite

**Total cost for all 3 services:** $21/month (or just upgrade the API: $7/month)

---

## 📊 PostgreSQL Database (Optional Upgrade)

For production, consider upgrading from SQLite to PostgreSQL:

### Why Upgrade?

- ✅ Persistent data (survives restarts)
- ✅ Better performance
- ✅ Concurrent writes
- ✅ 90-day backup retention (free tier)

### How to Add PostgreSQL

1. **Uncomment in `render.yaml`:**

```yaml
databases:
  - name: architecture-playground-db
    plan: free
    databaseName: tasks
    user: tasks_user
```

2. **Update `sample-app/01-monolith/database.py`:**

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Use PostgreSQL if DATABASE_URL is set
if DATABASE_URL.startswith("postgres://"):
    # Update to use PostgreSQL instead of SQLite
    ...
```

3. **Update requirements.txt:**

```
psycopg2-binary>=2.9.9
```

4. **Redeploy** - Render will create the database automatically

---

## 🔍 Monitoring & Debugging

### View Logs

1. Go to Render dashboard
2. Click on a service
3. Click **"Logs"** tab
4. See real-time logs

### Health Checks

All services have health checks configured:
- Platform: `GET /`
- API: `GET /`
- UI: Checks static file availability

### Common Issues

#### 1. Service Shows "Build Failed"
**Solution:** Check build logs for errors
```bash
# Common issues:
- Missing dependencies in requirements.txt
- Python version mismatch
- Import errors
```

#### 2. CORS Errors in Browser
**Solution:** Check environment variables
```bash
# Verify CORS_ORIGINS is set correctly:
Dashboard → API Service → Environment → CORS_ORIGINS
Should be: https://architecture-playground-ui.onrender.com,https://architecture-playground.onrender.com
```

#### 3. Task Manager UI Can't Connect to API
**Solution:**
- Wait for API service to wake up (30 seconds first load)
- Check browser console for exact error
- Verify API URL in browser network tab

#### 4. Service Constantly Restarting
**Solution:** Check for:
- Runtime errors in logs
- Memory limit exceeded (upgrade to paid)
- Port binding issues

---

## 🎨 Custom Domain (Optional)

Add your own domain:

1. Go to service settings
2. Click **"Custom Domains"**
3. Add your domain (e.g., `playground.yourdomain.com`)
4. Update DNS records as instructed
5. SSL certificate auto-generated

**Cost:** Free! Included with all plans

---

## 🔐 Security Best Practices

### For Production

1. **Add Authentication**
   ```python
   # In monolith API, add:
   from fastapi.security import HTTPBearer
   ```

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   ```

3. **Environment Secrets**
   - Use Render's secret environment variables
   - Never commit secrets to Git

4. **Database Backup**
   - Enable PostgreSQL (includes 90-day backups)
   - Or use external backup service

---

## 📈 Performance Optimization

### Speed Up Cold Starts

1. **Upgrade to Paid** ($7/month) - Best option
2. **Keep Service Warm**:
   ```bash
   # Use a cron job to ping every 10 minutes
   curl https://architecture-playground-api.onrender.com/
   ```

3. **Optimize Build Time**:
   ```yaml
   # In render.yaml, use cached dependencies:
   buildCommand: pip install --cache-dir /opt/render/.pip-cache -r requirements.txt
   ```

---

## 🧪 Testing Deployment

Before sharing with others:

### 1. Test Learning Platform
```
✓ Visit https://architecture-playground.onrender.com
✓ Click "Try Interactive Demo" button
✓ Navigate to comparison page
✓ Click on architecture detail pages
```

### 2. Test Monolith API
```
✓ Visit https://architecture-playground-api.onrender.com/docs
✓ Try creating a task via Swagger UI
✓ Verify CORS headers in browser network tab
```

### 3. Test Task Manager UI
```
✓ Visit https://architecture-playground-ui.onrender.com
✓ Create a task
✓ Update task status
✓ Filter tasks
✓ Click "Back to Learning Platform"
✓ Verify response times display
```

---

## 🚨 Rollback Deployment

If something goes wrong:

1. Go to service in dashboard
2. Click **"Manual Deploy"** tab
3. Select previous successful deploy
4. Click **"Redeploy"**

Or:

```bash
# Revert Git commit and push
git revert HEAD
git push origin main
# Render auto-deploys the reverted version
```

---

## 📞 Support

### Render.com Support

- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Project Issues

- GitHub Issues: https://github.com/gkaria/architecture-playground/issues
- Check logs in Render dashboard first

---

## ✅ Post-Deployment Checklist

After successful deployment:

- [ ] All 3 services show "Live" status
- [ ] Learning Platform loads and displays correctly
- [ ] API documentation accessible
- [ ] Task Manager UI can create/update tasks
- [ ] No CORS errors in browser console
- [ ] Architecture selector works
- [ ] Navigation between services works
- [ ] GitHub link works
- [ ] Response times display correctly

---

## 🎉 You're Live!

Your Architecture Patterns Playground is now deployed and accessible worldwide!

**Share these URLs:**
- Main Site: `https://architecture-playground.onrender.com`
- Interactive Demo: `https://architecture-playground-ui.onrender.com`
- API Docs: `https://architecture-playground-api.onrender.com/docs`

**Add to:**
- Portfolio website
- Resume
- LinkedIn projects
- GitHub README

---

## 💡 Next Steps

1. **Monitor Usage** - Check Render dashboard weekly
2. **Add Analytics** - Consider Google Analytics
3. **Get Feedback** - Share with friends/colleagues
4. **Iterate** - Add Phase 2 (Modular Monolith)
5. **Blog About It** - Write about your learnings

**Congratulations on deploying your architecture learning platform!** 🚀
