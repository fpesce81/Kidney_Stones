# Vercel Deployment Guide for Kidney Stones Django App

This guide explains how to deploy the Kidney Stones Django application to Vercel.

## Prerequisites

1. Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed: `npm i -g vercel`
3. Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Environment Variables

Set up the following environment variables in Vercel:

```bash
DJANGO_SECRET_KEY=your-very-secret-key-here
DJANGO_SETTINGS_MODULE=kidney_stones_django.settings_production
DATABASE_URL=postgres://user:password@host:port/dbname  # Optional, uses SQLite if not set
CUSTOM_DOMAIN=yourdomain.com  # Optional
```

### 2. Database Considerations

- **Development**: Uses SQLite in `/tmp` directory (temporary)
- **Production**: Recommended to use PostgreSQL with a service like:
  - Vercel Postgres
  - Supabase
  - Neon
  - Railway

### 3. Deploy via Git

1. Push your code to a Git repository
2. Import the project in Vercel dashboard
3. Vercel will automatically detect the configuration

### 4. Deploy via CLI

```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

## Important Notes

### Static Files
- Static files are collected during build
- Served via Vercel's CDN automatically
- WhiteNoise handles static file serving

### Limitations
- Vercel functions have a 10-second timeout (60 seconds for Pro accounts)
- Maximum payload size: 5MB
- Temporary file system in `/tmp` (cleared between invocations)
- No persistent file storage

### Database Migrations
- Migrations run automatically during build
- For production, use a persistent database (PostgreSQL)
- SQLite data is lost between deployments

### Sessions
- Database sessions recommended for production
- File-based sessions won't persist

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Static Files 404**
   - Run `python manage.py collectstatic` locally to test
   - Check `STATIC_ROOT` and `STATIC_URL` settings

3. **Database Errors**
   - Verify `DATABASE_URL` is set correctly
   - Check database credentials and connectivity

4. **CORS Issues**
   - Update `CORS_ALLOWED_ORIGINS` in settings_production.py
   - Add your custom domain to allowed origins

## Performance Optimization

1. **Cold Starts**
   - Keep dependencies minimal
   - Use lazy imports where possible

2. **Database Queries**
   - Use `select_related()` and `prefetch_related()`
   - Implement caching for frequently accessed data

3. **Static Assets**
   - Use CDN for large static files
   - Optimize images before deployment

## Security Checklist

- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Enable HTTPS redirect
- [ ] Configure CORS properly
- [ ] Set secure cookie settings
- [ ] Review `ALLOWED_HOSTS`
- [ ] Enable security headers

## Alternative Deployment Options

If Vercel doesn't meet your needs, consider:
- **Render**: Better Django support with persistent storage
- **Railway**: Easy Django deployment with PostgreSQL
- **Fly.io**: Global deployment with persistent volumes
- **DigitalOcean App Platform**: Managed Django hosting
