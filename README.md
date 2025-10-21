# Veterinary Educational Platform API

A production-ready FastAPI backend for veterinary education with comprehensive features including authentication, content management, push notifications, and more.

## 🌟 Features

- **🔐 Authentication & Authorization**
  - JWT-based authentication with refresh tokens
  - Role-based access control (Admin/User)
  - Google OAuth integration
  - Secure password hashing with bcrypt

- **📚 Content Management**
  - Dictionary words (veterinary terminology)
  - Diseases database
  - Drugs & medications
  - Books & resources
  - Medical instruments
  - Clinical notes
  - Laboratory test categories (Haematology, Serology, Biochemistry, etc.)
  - Medical slides (Urine, Stool, Other)
  - Normal ranges for lab values

- **🔔 Notifications**
  - OneSignal push notification integration
  - In-app notification system
  - Automatic notifications for new content

- **🛡️ Security**
  - Rate limiting middleware
  - CORS configuration
  - Security headers
  - SQL injection protection
  - Input validation

- **📊 Monitoring & Logging**
  - Comprehensive logging system
  - Health check endpoints
  - Metrics endpoint
  - Database connection pooling
  - Request/response logging

- **🚀 Production Ready**
  - Database migrations with Alembic
  - Environment-based configuration
  - Error handling middleware
  - Connection retry logic
  - Graceful startup/shutdown

## 📋 Requirements

- Python 3.8+
- PostgreSQL (recommended) or SQLite
- Redis (optional, for caching)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd python-database-main

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Set SECRET_KEY for production!
```

### 3. Database Setup

```bash
# Initialize Alembic (first time only)
python alembic_setup.py

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development mode
python main.py

# Production mode with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
```

The API will be available at `http://localhost:5000`

## 📖 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Application environment | `development` |
| `SECRET_KEY` | JWT secret key | Auto-generated in dev |
| `DATABASE_URL` | Database connection string | SQLite |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |
| `RATE_LIMIT_REQUESTS` | Requests per minute | `60` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `60` |
| `ONESIGNAL_APP_ID` | OneSignal app ID | - |
| `ONESIGNAL_REST_API_KEY` | OneSignal API key | - |

See `.env.example` for all available options.

## 🗄️ Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## 🔐 Authentication

### Register a New User

```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "user@example.com",
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Login

```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "abc...",
  "token_type": "bearer"
}
```

### Use Authentication

```bash
GET /api/dictionary/
Authorization: Bearer eyJ...
```

## 📊 Monitoring

### Health Check

```bash
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "database": "connected",
  "database_info": {...}
}
```

### Metrics

```bash
GET /metrics

Response:
{
  "users": 150,
  "dictionary_words": 5000,
  "diseases": 200,
  "drugs": 500,
  "books": 50
}
```

## 🏗️ Project Structure

```
python-database-main/
├── api/                    # API route modules
│   ├── auth.py            # Authentication endpoints
│   ├── dictionary.py      # Dictionary endpoints
│   ├── diseases.py        # Diseases endpoints
│   └── ...
├── alembic/               # Database migrations
├── logs/                  # Application logs
├── uploads/               # Uploaded files
├── main.py                # Application entry point
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── database.py            # Database configuration
├── auth.py                # Authentication logic
├── crud.py                # CRUD operations
├── config.py              # Configuration management
├── logger.py              # Logging configuration
├── middleware.py          # Custom middleware
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## 🔒 Security Best Practices

1. **Always set a strong SECRET_KEY in production**
2. **Configure specific CORS origins** (not `*`)
3. **Use HTTPS in production**
4. **Keep dependencies updated**
5. **Use environment variables for sensitive data**
6. **Enable rate limiting**
7. **Regular security audits**
8. **Database backups**

## 🚀 Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Docker (Coming Soon)

```bash
# Build image
docker build -t vetstan-api .

# Run container
docker run -p 5000:5000 --env-file .env vetstan-api
```

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Dictionary
- `GET /api/dictionary/` - List dictionary words
- `POST /api/dictionary/` - Create word (admin)
- `GET /api/dictionary/{name}` - Get word by name
- `PUT /api/dictionary/{name}` - Update word (admin)
- `DELETE /api/dictionary/{name}` - Delete word (admin)

### Diseases
- `GET /api/diseases/` - List diseases
- `POST /api/diseases/` - Create disease (admin)
- `GET /api/diseases/{name}` - Get disease
- `PUT /api/diseases/{name}` - Update disease (admin)
- `DELETE /api/diseases/{name}` - Delete disease (admin)

### Drugs
- `GET /api/drugs/` - List drugs
- `POST /api/drugs/` - Create drug (admin)
- `GET /api/drugs/{name}` - Get drug
- `PUT /api/drugs/{name}` - Update drug (admin)
- `DELETE /api/drugs/{name}` - Delete drug (admin)

*See `/docs` for complete API documentation*

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📈 Performance

- **Rate Limiting**: 60 requests/minute per IP
- **Database Connection Pooling**: Configured for PostgreSQL
- **Async Operations**: FastAPI async support
- **Caching**: Ready for Redis integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

[Your License Here]

## 📞 Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: support@example.com

## 🎯 Roadmap

- [ ] Redis caching integration
- [ ] WebSocket support for real-time updates
- [ ] GraphQL API
- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] API versioning
- [ ] Automated testing CI/CD
- [ ] Performance monitoring dashboard

---

**Version**: 3.0.0  
**Last Updated**: 2024-01-15
