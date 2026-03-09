# Railway Deployment Setup

## Required Environment Variables

For Railway deployment, you need to set these environment variables:

### Essential Variables

1. **DATABASE_URL** (Auto-configured by Railway if you add PostgreSQL)
   - Railway automatically provides this when you add a PostgreSQL database
   - No manual configuration needed

2. **SECRET_KEY** (Recommended for production)
   ```
   Generate a secure key using:
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Then set it in Railway's environment variables

### Optional Variables

3. **ENVIRONMENT** (defaults to 'development')
   - Set to `production` for production deployment
   - Railway may auto-set this

4. **CORS_ORIGINS** (defaults to `*`)
   - Set to your frontend domain(s), comma-separated
   - Example: `https://myapp.com,https://www.myapp.com`

5. **PORT** (Railway sets this automatically)
   - Railway will set this - no need to configure

## How to Set Environment Variables on Railway

1. Go to your Railway project
2. Click on your service
3. Go to "Variables" tab
4. Add the required variables:
   - `SECRET_KEY`: (generate using the command above)
   - `CORS_ORIGINS`: (your allowed domains)
   - `ENVIRONMENT`: `production`

## Database Setup

1. In Railway, add a PostgreSQL database to your project
2. Link it to your service
3. Railway will automatically set the `DATABASE_URL` environment variable

## Deployment Configuration

The app is configured to run with Gunicorn in production. Railway will automatically use the configuration from `railway.toml` and `Procfile`.

### Files Created for Railway
- **`railway.toml`**: Railway-specific configuration
- **`Procfile`**: Defines the start command for the web service

The start command uses Railway's `$PORT` environment variable:
```
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**Important**: Railway automatically sets the `PORT` environment variable - you don't need to set it manually.

## Health Check

After deployment, verify the app is running:
- Health endpoint: `https://your-app.railway.app/health`
- API docs: `https://your-app.railway.app/docs` (if DEBUG is enabled)

## Common Issues

### App crashes on startup
- **Cause**: Missing SECRET_KEY (now auto-generated with warning)
- **Solution**: Set SECRET_KEY environment variable in Railway

### Database connection errors
- **Cause**: PostgreSQL not linked or DATABASE_URL incorrect
- **Solution**: Add PostgreSQL service and link to your app

### CORS errors
- **Cause**: CORS_ORIGINS not configured for your domain
- **Solution**: Set CORS_ORIGINS to include your frontend domain
