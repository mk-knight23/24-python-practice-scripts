# Python Practice - Deployment Guide

This guide covers how to deploy the Python Practice application on various platforms.

## Table of Contents

1. [Local Development](#local-development)
2. [Vercel Deployment](#vercel-deployment)
3. [Render Deployment](#render-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Production Considerations](#production-considerations)

## Local Development

### Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher (for web dashboard)
- npm or yarn

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mk-knight23/24-python-practice-scripts.git
   cd 24-python-practice-scripts
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run CLI version**
   ```bash
   python cli/runner.py
   ```

5. **Run web dashboard**
   ```bash
   python app.py
   ```
   Open http://localhost:5000 in your browser.

## Vercel Deployment

### Prerequisites

- Vercel account
- Vercel CLI installed

### Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel
   ```
   Follow the prompts to link your repository and deploy.

3. **Environment Variables**
   - Add `PYTHON_VERSION` with value `3.10`
   - Add `VERCEL` with value `1`

### Alternative (Vercel Functions)

Create `app/index.py` and deploy as a Python function:

```python
# app/index.py
from app import app

if __name__ == '__main__':
    app.run()
```

## Render Deployment

### Prerequisites

- Render account
- Render CLI installed

### Steps

1. **Create a new service**
   - Select Web Service
   - Connect GitHub repository
   - Choose Python environment

2. **Build Command**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command**
   ```bash
   gunicorn app:app
   ```

4. **Environment Variables**
   ```
   PYTHON_VERSION=3.10
   PORT=10000
   ```

## Heroku Deployment

### Prerequisites

- Heroku account
- Heroku CLI installed

### Steps

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Add Python buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Docker Deployment

### Build Docker Image

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 5000

   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

2. **Build the image**
   ```bash
   docker build -t python-practice .
   ```

3. **Run the container**
   ```bash
   docker run -p 5000:5000 python-practice
   ```

4. **Docker Compose**
   ```yaml
   version: '3.8'
   services:
     python-practice:
       build: .
       ports:
         - "5000:5000"
       environment:
         - PYTHON_VERSION=3.10
   ```

## Production Considerations

### Database

- Use PostgreSQL instead of SQLite for production
- Set up proper database migrations
- Configure environment variables for database connection

### Security

- Set up proper authentication
- Use HTTPS in production
- Implement rate limiting
- Secure environment variables

### Performance

- Use Redis for caching
- Set up proper logging
- Use a production WSGI server (Gunicorn/uWSGI)
- Implement proper error handling

### Monitoring

- Set up health checks
- Monitor application performance
- Set up alerts for errors
- Track user engagement metrics

### Environment Variables

Create a `.env` file in production:

```env
PYTHON_VERSION=3.10
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
```

## Testing

Run tests before deployment:

```bash
# Run pytest
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=cli --cov=app

# Type check
mypy cli/ app/
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

2. **Database Issues**
   - Ensure SQLite database is created
   - Check database permissions

3. **Port Conflicts**
   - Change port in app.run()
   - Check if port is available

4. **Build Failures**
   - Check requirements.txt syntax
   - Verify Python version compatibility

### Logs

Check application logs:

```bash
# Local logs
tail -f logs/app.log

# Vercel logs
vercel logs

# Heroku logs
heroku logs --tail
```

## Support

If you encounter any issues during deployment:

1. Check the troubleshooting section
2. Review the GitHub issues
3. Create a new issue with:
   - Deployment platform
   - Error messages
   - Steps to reproduce
   - Environment details

## Contributing

If you want to contribute to deployment improvements:

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request
5. Include deployment instructions if applicable