# 🚀 Deployment Guide

## Local Development

See QUICKSTART.md for local setup.

## Production Deployment

### Option 1: Docker Compose (Recommended)

#### Prerequisites
- VPS/Server with Docker installed
- Domain name (optional)
- SSL certificate (Let's Encrypt recommended)

#### Steps

1. **Prepare Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose
```

2. **Clone Project**
```bash
git clone <your-repo>
cd smartjobhunter
```

3. **Configure Environment**
```bash
cp .env.example .env
nano .env

# Set production values:
# - Strong SECRET_KEY
# - Production database credentials
# - API keys
# - Set ENVIRONMENT=production
# - Set DEBUG=False
```

4. **Start Services**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

5. **Setup Nginx (Optional)**
```bash
sudo apt install nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/jobhunter

# Add:
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/jobhunter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Option 2: Manual Deployment

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend
```bash
cd frontend
npm install
npm run build
# Serve dist/ folder with nginx or any static server
```

### Database Migration (SQLite to PostgreSQL)

```bash
# Backup SQLite data
sqlite3 data/jobhunter.db .dump > backup.sql

# Create PostgreSQL database
createdb jobhunter

# Migrate (requires manual schema adjustments)
# Or use alembic migrations
```

### Monitoring

#### Health Checks
- Backend: http://localhost:8000/health
- Check logs: `docker-compose logs -f`

#### Automated Backups
```bash
# Add to crontab
0 2 * * * docker exec jobhunter_db pg_dump -U postgres jobhunter > /backup/$(date +\%Y\%m\%d).sql
```

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable firewall (ufw)
- [ ] Setup SSL/HTTPS
- [ ] Regular backups
- [ ] Update dependencies regularly
- [ ] Monitor logs for suspicious activity

### Performance Optimization

1. **Redis Caching**
   - Enable Redis in production config
   - Cache frequent queries

2. **Database Indexing**
   - Already configured in models
   - Monitor slow queries

3. **CDN for Static Assets**
   - Consider Cloudflare for frontend

4. **Load Balancing**
   - Use nginx for multiple backend workers

### Scaling

#### Horizontal Scaling
```bash
# Scale backend workers
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

#### Database Scaling
- Consider managed PostgreSQL (AWS RDS, DigitalOcean)
- Setup read replicas for heavy loads

### Troubleshooting

**High Memory Usage**
- Adjust worker count in production config
- Monitor with `docker stats`

**Slow Scraping**
- Increase scraping delays
- Reduce concurrent scrapers

**Database Lock Issues**
- Migrate to PostgreSQL for production
- Use connection pooling

### Cost Estimates

**Hetzner CX21** (Recommended for start)
- 2 vCPU, 4GB RAM
- ~€5/month
- Suitable for 1000+ jobs/day

**DigitalOcean Droplet**
- $12/month for 2GB RAM
- Managed databases +$15/month (optional)

**API Costs**
- Gemini Pro: Free tier (60 requests/minute)
- Claude/GPT-4: Pay per use (optional fallback)

