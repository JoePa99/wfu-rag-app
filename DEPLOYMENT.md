# Deployment Guide

This guide covers multiple deployment options for the Wake Forest RAG application.

## Pre-Deployment Checklist

Before deploying, ensure:
- [ ] All API keys are obtained and tested locally
- [ ] Default password has been changed
- [ ] Supabase database is configured
- [ ] Google Drive service account is set up
- [ ] Application works correctly on local machine
- [ ] `.env` and `service-account.json` are in `.gitignore`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Quick Deployment)

**Pros:** Easy, free tier available, minimal setup  
**Cons:** Public by default (private requires paid plan)

#### Steps:

1. **Prepare Repository**
   ```bash
   # Make sure sensitive files are not committed
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"

3. **Configure App**
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `app.py`

4. **Add Secrets**
   Click "Advanced settings" and add:
   ```toml
   # .streamlit/secrets.toml format
   ANTHROPIC_API_KEY = "your_key_here"
   OPENAI_API_KEY = "your_key_here"
   SUPABASE_URL = "your_url_here"
   SUPABASE_SERVICE_KEY = "your_key_here"
   GOOGLE_SERVICE_ACCOUNT_FILE = "./service-account.json"
   
   # For service account, paste the JSON content
   [google_service_account]
   # Paste entire JSON content here
   ```

5. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment

6. **Access**
   - Your app will be at: `https://your-app-name.streamlit.app`

#### Making it Private on Streamlit Cloud:
- Requires Streamlit Teams ($20+/month)
- Or rely on authentication system (password protection)

---

### Option 2: Docker + Cloud VPS (Most Flexible)

**Pros:** Full control, can be private, works on any VPS  
**Cons:** Requires server management

#### Supported Platforms:
- DigitalOcean
- AWS EC2
- Google Cloud Compute
- Azure VMs
- Linode
- Vultr

#### Steps:

1. **Prepare Docker Image**
   ```bash
   # Build image
   docker build -t wfu-rag-app .
   
   # Test locally
   docker-compose up
   ```

2. **Choose a VPS Provider**
   
   **DigitalOcean (Recommended for beginners):**
   - Create a Droplet (Ubuntu 22.04)
   - Size: Basic ($12/month, 2GB RAM)
   - Enable backups (optional)

   **AWS EC2:**
   - Instance type: t3.small or t3.medium
   - OS: Ubuntu 22.04 LTS
   - Security group: Allow port 8501

3. **SSH into Server**
   ```bash
   ssh root@your-server-ip
   ```

4. **Install Docker**
   ```bash
   # Update system
   apt update && apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install Docker Compose
   apt install docker-compose -y
   ```

5. **Deploy Application**
   ```bash
   # Create app directory
   mkdir /opt/wfu-rag-app
   cd /opt/wfu-rag-app
   
   # Upload files (from local machine)
   scp -r * root@your-server-ip:/opt/wfu-rag-app/
   
   # Or use git
   git clone your-repo-url .
   
   # Create .env file on server
   nano .env
   # Paste your environment variables
   
   # Upload service account
   # (Upload service-account.json via scp)
   
   # Run with Docker Compose
   docker-compose up -d
   ```

6. **Setup Nginx Reverse Proxy (Optional but Recommended)**
   ```bash
   # Install Nginx
   apt install nginx -y
   
   # Create config
   nano /etc/nginx/sites-available/wfu-rag
   ```
   
   Add this configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # Or use IP
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   Enable and restart:
   ```bash
   ln -s /etc/nginx/sites-available/wfu-rag /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx
   ```

7. **Setup SSL (Highly Recommended)**
   ```bash
   # Install Certbot
   apt install certbot python3-certbot-nginx -y
   
   # Get certificate
   certbot --nginx -d your-domain.com
   ```

8. **Access Application**
   - HTTP: `http://your-domain.com` or `http://your-server-ip`
   - HTTPS: `https://your-domain.com`

---

### Option 3: Heroku

**Pros:** Easy deployment, free tier (with limitations)  
**Cons:** Limited free hours, may sleep

#### Steps:

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create wfu-rag-app
   ```

4. **Add Buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

5. **Create `Procfile`**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

6. **Set Environment Variables**
   ```bash
   heroku config:set ANTHROPIC_API_KEY=your_key
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set SUPABASE_URL=your_url
   heroku config:set SUPABASE_SERVICE_KEY=your_key
   heroku config:set GOOGLE_SERVICE_ACCOUNT_FILE=./service-account.json
   ```

7. **Deploy**
   ```bash
   git push heroku main
   ```

---

### Option 4: Wake Forest IT Infrastructure

If Wake Forest has internal hosting:

1. **Contact IT Department**
   - Request VM or container hosting
   - Provide requirements: Python 3.9+, 2GB RAM minimum

2. **Security Compliance**
   - Ensure compliance with university data policies
   - May need security review
   - Discuss data residency requirements

3. **Integration**
   - Consider SSO integration with university authentication
   - May integrate with existing monitoring systems

---

## Post-Deployment

### 1. Test Everything
- [ ] Login works
- [ ] Can index documents
- [ ] Queries return results
- [ ] Source citations work
- [ ] All buttons and features functional

### 2. Security Hardening

**Change Default Password:**
```bash
python generate_password.py
```

**Set Strong Cookie Key:**
Edit `config.yaml`:
```yaml
cookie:
  key: "CHANGE_THIS_TO_RANDOM_STRING_32_CHARS"
```

**Enable HTTPS:**
- Use SSL certificate (Let's Encrypt free)
- Force HTTPS in Nginx config

**Firewall Rules:**
```bash
# If using UFW on Ubuntu
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp  # SSH
ufw enable
```

### 3. Monitoring

**Application Logs:**
```bash
# Docker
docker-compose logs -f

# Systemd service
journalctl -u wfu-rag-app -f
```

**Resource Monitoring:**
```bash
# Install htop
apt install htop
htop

# Check disk space
df -h

# Check memory
free -h
```

**Uptime Monitoring:**
- Use UptimeRobot (free)
- Or Pingdom
- Or AWS CloudWatch

### 4. Backups

**Supabase:**
- Enable automated backups in Supabase dashboard
- Pro plan includes point-in-time recovery

**Configuration:**
```bash
# Backup config files
tar -czf backup-$(date +%Y%m%d).tar.gz \
  config.yaml \
  .env \
  service-account.json

# Store securely offsite
```

### 5. Maintenance

**Regular Updates:**
```bash
# Update packages
pip install -r requirements.txt --upgrade

# Rebuild Docker image
docker-compose build --no-cache
docker-compose up -d
```

**Monitor API Usage:**
- Check Anthropic usage dashboard
- Check OpenAI usage dashboard
- Set up billing alerts

**Log Rotation:**
```bash
# Docker logs
docker system prune -a

# System logs
journalctl --vacuum-time=7d
```

---

## Scaling Considerations

### For Heavy Usage:

1. **Upgrade Server Resources**
   - More RAM (4GB → 8GB)
   - More CPU cores
   - SSD storage

2. **Optimize Supabase**
   - Upgrade to Pro plan
   - Enable connection pooling
   - Add indexes for common queries

3. **Rate Limiting**
   - Implement request rate limits
   - Add user quotas if needed

4. **Caching**
   - Cache common queries
   - Use Redis for session storage

5. **Load Balancing**
   - Multiple instances behind load balancer
   - Database read replicas

---

## Cost Breakdown by Option

### Streamlit Cloud
- Free tier: $0/month (public)
- Teams: $20/month (private)
- Enterprise: Custom pricing

### VPS Hosting
- DigitalOcean: $12-24/month
- AWS EC2: $15-50/month (t3.small-medium)
- Domain: $10-15/year
- SSL: Free (Let's Encrypt)

### Heroku
- Free: $0/month (550 hours)
- Hobby: $7/month
- Standard: $25/month

### Additional Costs (All Options)
- Supabase: Free → $25/month
- Anthropic API: Pay per use (~$0.01-0.03/query)
- OpenAI API: Pay per use (~$0.10/1M tokens)

**Total Estimated Monthly Cost:**
- Light usage: $10-30/month
- Medium usage: $50-100/month
- Heavy usage: $100-200/month

---

## Troubleshooting Deployment

### "Port already in use"
```bash
# Find process
lsof -i :8501
# Kill process
kill -9 <PID>
```

### "Permission denied"
```bash
# Fix file permissions
chmod +x verify_setup.py generate_password.py
```

### "Out of memory"
```bash
# Check memory
free -h
# Restart container
docker-compose restart
```

### "Cannot connect to Supabase"
- Check firewall rules
- Verify Supabase URL and key
- Test connection manually

---

## Support Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Docker Docs:** https://docs.docker.com/
- **DigitalOcean Tutorials:** https://www.digitalocean.com/community/tutorials
- **Nginx Docs:** https://nginx.org/en/docs/

For Wake Forest specific support, contact your IT department.
