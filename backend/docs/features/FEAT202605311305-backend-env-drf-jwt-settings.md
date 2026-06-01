# Feature: Backend Environment, DRF, and JWT Settings

**Feature ID:** FEAT202605311305  
**Status:** In Development  
**Sprint:** Backend Sprint 1  
**Ticket Mapping:** BE-M1-01  
**Requirement Mapping:** R8, R15  
**Last Updated:** 2026-05-31

---

## Table of Contents
1. [Feature Overview](#feature-overview)
2. [User Stories](#user-stories)
3. [Acceptance Criteria](#acceptance-criteria)
4. [Detailed Implementation Guide](#detailed-implementation-guide)
5. [Configuration Examples](#configuration-examples)
6. [Testing Strategy](#testing-strategy)
7. [Validation & Verification](#validation--verification)
8. [Deployment Guide](#deployment-guide)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [References](#references)

---

## Feature Overview

Create the backend runtime foundation so the service can run with environment-driven settings and API security defaults.

### Why this matters:
- **Removes hardcoded local-only behavior** – Code is portable across environments
- **Enables predictable API behavior** – Consistent auth, permissions, and pagination across dev/test/prod
- **Creates secure default baseline** – All protected endpoints reject unauthenticated requests automatically
- **Supports containerization** – Environment variables enable Docker and orchestration platform deployments
- **Improves compliance** – Separates secrets from code and prevents accidental exposure

### Design Principles:
- **Environment-driven configuration:** All runtime settings come from environment variables with documented defaults
- **Fail-safe defaults:** Development mode has safe, non-production-ready defaults; production mode requires explicit configuration
- **DRF consistency:** All REST endpoints inherit the same authentication, permission, and pagination behavior
- **JWT security:** Authentication tokens are validated on every protected request
- **Configuration transparency:** `.env.example` documents all required and optional settings

---

## User Stories

### Story 1: Developer Environment Control
- **As a** backend developer
- **I want** environment variables to control app runtime settings
- **So that** I can run the same code in local, CI, and container environments

**Acceptance Criteria:**
- Environment variables override hardcoded defaults
- Missing non-critical vars fall back to safe defaults
- Missing critical vars fail fast with clear error messages

### Story 2: API Behavior Consistency
- **As an** API maintainer
- **I want** DRF defaults configured centrally
- **So that** all endpoints inherit consistent auth, permission, and pagination behavior

**Acceptance Criteria:**
- New list endpoints automatically paginate with configured page size
- New endpoints respect global authentication and permission classes
- Configuration changes apply to all endpoints without code modifications

### Story 3: Security Baseline
- **As a** security reviewer
- **I want** JWT authentication baseline configured
- **So that** protected endpoints reject unauthenticated requests by default

**Acceptance Criteria:**
- Unauthenticated requests to protected endpoints return HTTP 401
- Valid JWT tokens are accepted and validated
- Invalid or expired tokens are rejected with HTTP 401
- Token validation includes signature verification and expiration checks

---

## Acceptance Criteria

### Criterion 1: Environment Variable Configuration
- **Given** the service starts with environment variables configured
- **When** Django settings load
- **Then** DB and security-sensitive settings are read from environment and not hardcoded

**Test:** `test_settings_load_from_env()`

### Criterion 2: Unauthenticated Request Rejection
- **Given** a protected endpoint is called without token
- **When** request is processed
- **Then** API returns HTTP `401 Unauthorized`

**Test:** `test_protected_endpoint_requires_auth()`

### Criterion 3: DRF Default Application
- **Given** DRF settings are configured
- **When** a list endpoint is created
- **Then** default pagination and auth behavior apply automatically

**Test:** `test_list_endpoint_applies_drf_defaults()`

---

## Detailed Implementation Guide

### Phase 1: Environment Variable Loading

#### 1.1 Install python-dotenv

Add to `backend/requirements.txt`:
```
python-dotenv==1.0.0
```

Install in development:
```bash
pip install python-dotenv==1.0.0
```

#### 1.2 Update Django Settings (`backend/config/settings.py`)

Add at the **top** of the file (before any other settings):

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment configuration with typed access
def get_env(key, default=None, required=False):
    """
    Safely retrieve environment variables with optional type coercion.
    
    Args:
        key: Environment variable name
        default: Default value if not set (None if required=True)
        required: If True, raises error if key is missing
        
    Returns:
        Value from environment or default
        
    Raises:
        RuntimeError: If required key is missing
    """
    value = os.getenv(key, default)
    if value is None and required:
        raise RuntimeError(f"Required environment variable '{key}' is not set")
    return value

def get_bool(key, default=False):
    """Convert environment variable to boolean."""
    value = get_env(key, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')
```

### Phase 2: Core Settings Configuration

#### 2.1 Application Environment

Add after the environment helper functions:

```python
# ============================================================================
# APPLICATION ENVIRONMENT
# ============================================================================

APP_ENV = get_env('APP_ENV', 'development')
DEBUG = APP_ENV in ('development', 'test')

if APP_ENV == 'production':
    ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', '').split(',')
    if not ALLOWED_HOSTS or not ALLOWED_HOSTS[0]:
        raise RuntimeError(
            "In production, ALLOWED_HOSTS environment variable must be set. "
            "Example: ALLOWED_HOSTS=api.example.com,www.example.com"
        )
else:
    ALLOWED_HOSTS = ['*']  # Safe for development only

# Security settings based on environment
if APP_ENV == 'production':
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
```

#### 2.2 Database Configuration

Add after application environment settings:

```python
# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Support both DATABASE_URL and individual database settings
DATABASE_URL = get_env('DATABASE_URL')

if DATABASE_URL:
    # Use dj-database-url for parsing connection strings
    # Example: sqlite:///db.sqlite3 or postgresql://user:pass@localhost/dbname
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Database connection pooling for production
if APP_ENV == 'production':
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['CONN_HEALTH_CHECKS'] = True
```

#### 2.3 Secret Key Management

```python
# ============================================================================
# SECRET KEY & SECURITY
# ============================================================================

if APP_ENV == 'production':
    SECRET_KEY = get_env('SECRET_KEY', required=True)
else:
    # Safe default for development (never use in production!)
    SECRET_KEY = get_env(
        'SECRET_KEY',
        'dev-unsafe-change-in-production-' + 'x' * 40
    )
```

### Phase 3: DRF Configuration

#### 3.1 Install Dependencies

Add to `backend/requirements.txt`:
```
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.2
```

#### 3.2 Configure DRF Defaults

Add to `backend/config/settings.py`:

```python
# ============================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ============================================================================

REST_FRAMEWORK = {
    # Authentication Classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Permission Classes - All endpoints require authentication by default
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(get_env('PAGE_SIZE', 20)),
    
    # Filtering and Searching
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Exception Handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Default renderer and parser
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    
    # Authentication scheme for API documentation
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}
```

#### 3.3 Configure JWT Settings

```python
# ============================================================================
# SIMPLE JWT CONFIGURATION
# ============================================================================

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=int(get_env('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 15))
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=int(get_env('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7))
    ),
    'ROTATE_REFRESH_TOKENS': get_bool('JWT_ROTATE_REFRESH_TOKENS', True),
    'BLACKLIST_AFTER_ROTATION': get_bool('JWT_BLACKLIST_AFTER_ROTATION', True),
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': get_env(
        'JWT_SIGNING_KEY',
        SECRET_KEY if APP_ENV == 'development' else None
    ),
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'AUTH_REFRESH_CLASS': 'rest_framework_simplejwt.tokens.RefreshToken',
    
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    'JTI_CLAIM': 'jti',
}
```

### Phase 4: Application Settings

#### 4.1 INSTALLED_APPS

Add REST framework and Simple JWT:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',  # For frontend integration
    
    # Local apps
    'apps.audit',
    'apps.authz',
    'apps.billing',
    'apps.customers',
    'apps.inventory',
    'apps.reports',
    'apps.workorders',
]
```

#### 4.2 Business Logic Configuration

```python
# ============================================================================
# BUSINESS LOGIC CONFIGURATION
# ============================================================================

# Tax calculation
DEFAULT_TAX_RATE = float(get_env('TAX_RATE_DEFAULT', 0.0))

# Audit logging
AUDIT_LOG_ENABLED = get_bool('AUDIT_LOG_ENABLED', True)
AUDIT_LOG_RETENTION_DAYS = int(get_env('AUDIT_LOG_RETENTION_DAYS', 90))

# Pagination defaults
PAGE_SIZE = int(get_env('PAGE_SIZE', 20))
MAX_PAGE_SIZE = int(get_env('MAX_PAGE_SIZE', 100))

# API versioning (if needed)
API_VERSION = get_env('API_VERSION', 'v1')
```

### Phase 5: Create .env.example

Create `backend/.env.example`:

```bash
# ============================================================================
# APPLICATION ENVIRONMENT
# ============================================================================
# Options: development, test, production
APP_ENV=development

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# Format: sqlite:///db.sqlite3 or postgresql://user:password@localhost:5432/dbname
# If not set, defaults to SQLite in development
DATABASE_URL=sqlite:///db.sqlite3

# ============================================================================
# SECURITY & SECRETS
# ============================================================================
# NEVER commit actual secret keys. Generate strong keys in production.
# In development, a default is provided but MUST be changed in production.
SECRET_KEY=your-super-secret-key-change-in-production

# CORS configuration (comma-separated list)
ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================================================
# JWT CONFIGURATION
# ============================================================================
# JWT signing key (defaults to SECRET_KEY in development)
JWT_SIGNING_KEY=your-jwt-signing-key

# Token lifetime in minutes (default: 15)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15

# Refresh token lifetime in days (default: 7)
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Rotate refresh tokens automatically (default: true)
JWT_ROTATE_REFRESH_TOKENS=true

# Blacklist tokens after rotation (default: true)
JWT_BLACKLIST_AFTER_ROTATION=true

# ============================================================================
# BUSINESS LOGIC CONFIGURATION
# ============================================================================
# Default tax rate for calculations (0.0 to 1.0)
TAX_RATE_DEFAULT=0.0

# Enable audit logging (default: true)
AUDIT_LOG_ENABLED=true

# Days to retain audit logs (default: 90)
AUDIT_LOG_RETENTION_DAYS=90

# ============================================================================
# API CONFIGURATION
# ============================================================================
# Default page size for list endpoints (default: 20)
PAGE_SIZE=20

# Maximum allowed page size (default: 100)
MAX_PAGE_SIZE=100

# API version
API_VERSION=v1

# ============================================================================
# DEPLOYMENT (Production Only)
# ============================================================================
# PostgreSQL Example:
# DATABASE_URL=postgresql://postgres:password@db-host:5432/workorders_prod

# Redis cache (optional):
# REDIS_URL=redis://cache-host:6379/0
```

---

## Configuration Examples

### Development Setup

**Copy and configure `.env` file:**

```bash
cd backend
cp .env.example .env
```

**Edit `.env` for local development:**

```bash
APP_ENV=development
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=dev-secret-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1
TAX_RATE_DEFAULT=0.08
AUDIT_LOG_ENABLED=true
PAGE_SIZE=20
```

**Then load variables and run:**

```bash
python manage.py migrate
python manage.py runserver
```

### Docker Development Setup

**In your `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=2)"

EXPOSE 8000

# Use gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.wsgi:application"]
```

**In `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      APP_ENV: development
      DATABASE_URL: sqlite:///db.sqlite3
      SECRET_KEY: dev-secret-key
      DEBUG: "true"
    volumes:
      - ./backend:/app
    command: python manage.py runserver 0.0.0.0:8000
```

### Production Configuration

**Environment variables (set in deployment platform):**

```bash
APP_ENV=production
DATABASE_URL=postgresql://user:password@db-host:5432/workorders
SECRET_KEY=<generate-with-django.core.management.utils.get_random_secret_key>
ALLOWED_HOSTS=api.example.com,api-backup.example.com
JWT_SIGNING_KEY=<unique-production-key>
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
JWT_REFRESH_TOKEN_LIFETIME_DAYS=30
TAX_RATE_DEFAULT=0.08
AUDIT_LOG_ENABLED=true
AUDIT_LOG_RETENTION_DAYS=180
PAGE_SIZE=50
MAX_PAGE_SIZE=200
```

---

## Testing Strategy

### 1. Settings Loading Tests

Create `backend/config/tests/test_settings.py`:

```python
import os
from django.test import TestCase, override_settings
from django.conf import settings


class SettingsLoadingTests(TestCase):
    """Test environment variable loading and Django settings configuration."""
    
    def test_debug_mode_based_on_env(self):
        """DEBUG setting should respect APP_ENV."""
        self.assertTrue(settings.DEBUG)  # In test environment
    
    @override_settings(DEBUG=False, APP_ENV='production')
    def test_production_security_headers(self):
        """Production should enforce security settings."""
        # In production, security headers should be enabled
        # This is verified during production deployment
        pass
    
    def test_database_url_configuration(self):
        """Database should be configurable via DATABASE_URL."""
        self.assertIn('default', settings.DATABASES)
        self.assertIsNotNone(settings.DATABASES['default']['ENGINE'])
    
    def test_secret_key_not_exposed(self):
        """SECRET_KEY should not be a development default in production."""
        # This test runs in development/test only
        self.assertIsNotNone(settings.SECRET_KEY)
    
    def test_drf_pagination_configured(self):
        """DRF should have pagination configured."""
        drf_config = settings.REST_FRAMEWORK
        self.assertEqual(
            drf_config['DEFAULT_PAGINATION_CLASS'],
            'rest_framework.pagination.PageNumberPagination'
        )
        self.assertIsNotNone(drf_config['PAGE_SIZE'])
    
    def test_jwt_configuration(self):
        """JWT settings should be properly configured."""
        jwt_config = settings.SIMPLE_JWT
        self.assertEqual(jwt_config['ALGORITHM'], 'HS256')
        self.assertIsNotNone(jwt_config['ACCESS_TOKEN_LIFETIME'])
```

### 2. Authentication Tests

Create `backend/config/tests/test_auth.py`:

```python
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class JWTAuthenticationTests(APITestCase):
    """Test JWT authentication baseline."""
    
    def setUp(self):
        """Create test user and tokens."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
    
    def test_protected_endpoint_without_token_returns_401(self):
        """Unauthenticated request should return 401."""
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 401)
    
    def test_protected_endpoint_with_valid_token_returns_200(self):
        """Request with valid JWT token should succeed."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/customers/')
        # May return 200 or other 2xx depending on data
        self.assertLess(response.status_code, 400)
    
    def test_invalid_token_returns_401(self):
        """Request with invalid token should return 401."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-token')
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 401)
    
    def test_malformed_auth_header_returns_401(self):
        """Malformed Authorization header should return 401."""
        self.client.credentials(HTTP_AUTHORIZATION='InvalidScheme token')
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 401)
    
    def test_token_refresh_endpoint(self):
        """Refresh token should work at /token/refresh/ endpoint."""
        response = self.client.post(
            '/api/token/refresh/',
            {'refresh': str(self.refresh)},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
```

### 3. DRF Default Application Tests

Create `backend/config/tests/test_drf_defaults.py`:

```python
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings


class DRFDefaultsTests(APITestCase):
    """Test DRF defaults are applied to all endpoints."""
    
    def setUp(self):
        """Create authenticated client."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
    
    def test_pagination_applied_to_list_views(self):
        """List endpoints should apply pagination."""
        # Assuming an endpoint exists
        response = self.client.get('/api/customers/')
        if response.status_code == 200:
            # Paginated response should have these keys
            self.assertIn('results', response.data)
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)
    
    def test_page_size_respects_setting(self):
        """Pagination should respect PAGE_SIZE setting."""
        response = self.client.get('/api/customers/')
        if response.status_code == 200 and response.data.get('results'):
            max_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
            self.assertLessEqual(
                len(response.data['results']),
                max_page_size
            )
    
    def test_all_endpoints_use_authentication(self):
        """All endpoints should require authentication."""
        endpoints = [
            '/api/customers/',
            '/api/workorders/',
            '/api/inventory/',
        ]
        
        # Remove credentials to test unauthenticated access
        self.client.credentials()
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                401,
                f"Endpoint {endpoint} did not require authentication"
            )
```

---

## Validation & Verification

### 1. Manual Testing Checklist

Run these commands to verify the implementation:

```bash
cd backend

# 1. Check environment variables load
python -c "from django.conf import settings; print(f'DEBUG: {settings.DEBUG}'); print(f'APP_ENV: {settings.APP_ENV}')"

# 2. Verify DRF is installed
python -c "import rest_framework; print(f'DRF Version: {rest_framework.VERSION}')"

# 3. Verify SimpleJWT is installed
python -c "import rest_framework_simplejwt; print('SimpleJWT installed')"

# 4. Run migrations
python manage.py migrate

# 5. Create superuser for testing
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

### 2. Test Token Generation

```bash
# In a Python shell or Django shell
python manage.py shell

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# Get a user or create one
user = User.objects.first()

# Generate tokens
refresh = RefreshToken.for_user(user)
print(f"Access Token: {str(refresh.access_token)}")
print(f"Refresh Token: {str(refresh)}")
```

### 3. Test Authentication via cURL

```bash
# Get tokens
TOKENS=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}')

ACCESS_TOKEN=$(echo $TOKENS | jq -r '.access')

# Access protected endpoint
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/customers/

# Test without token (should return 401)
curl http://localhost:8000/api/customers/
```

### 4. Run Test Suite

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test config.tests.test_settings.SettingsLoadingTests

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## Deployment Guide

### Production Deployment Steps

#### Step 1: Generate Production Secrets

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT_SIGNING_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Step 2: Configure Environment Variables

Set in your deployment platform (Heroku, AWS, Azure, Docker, etc.):

```
APP_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=<generated-key>
JWT_SIGNING_KEY=<generated-key>
ALLOWED_HOSTS=api.example.com,api-backup.example.com
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
AUDIT_LOG_ENABLED=true
```

#### Step 3: Run Migrations

```bash
# Via CI/CD pipeline before deployment
python manage.py migrate --noinput

# Or manually in production
./manage.py migrate
```

#### Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### Step 5: Deploy Application

Use your deployment tool (Docker, systemd, Kubernetes, etc.):

**Docker Example:**
```bash
docker build -t workorders-api:latest .
docker run -d \
  -e APP_ENV=production \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=... \
  -p 8000:8000 \
  workorders-api:latest
```

#### Step 6: Health Checks

```bash
# Test the API
curl -H "Authorization: Bearer <token>" https://api.example.com/health/

# Check logs for errors
docker logs <container-id>
# or
tail -f /var/log/app/app.log
```

### Environment-Specific Configurations

**Development:**
```
APP_ENV=development
DEBUG=true
SECURE_SSL_REDIRECT=false
```

**Staging:**
```
APP_ENV=staging
DEBUG=false
SECURE_SSL_REDIRECT=true
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
```

**Production:**
```
APP_ENV=production
DEBUG=false
SECURE_SSL_REDIRECT=true
SECURE_HSTS_SECONDS=31536000
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
```

---

## Troubleshooting

### Issue: Environment Variable Not Loaded

**Symptoms:** Settings showing default values instead of environment values

**Solutions:**
```bash
# 1. Verify .env file exists and has content
cat backend/.env

# 2. Check environment variables are set
echo $APP_ENV
echo $DATABASE_URL

# 3. Reload Python environment
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('APP_ENV'))"
```

### Issue: Database Connection Fails

**Symptoms:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
```bash
# 1. Verify DATABASE_URL format
# PostgreSQL: postgresql://user:password@host:port/dbname
# SQLite: sqlite:///db.sqlite3

# 2. Test database connection
python manage.py dbshell

# 3. Check database credentials
echo "SELECT 1;" | psql -U user -h host -d dbname
```

### Issue: Authentication Returns 401 Even with Valid Token

**Symptoms:** All requests return `{"detail": "Invalid token."}` even with valid JWT

**Solutions:**
```bash
# 1. Verify JWT_SIGNING_KEY is consistent
# Should be same in token generation and validation

# 2. Check token expiration
python -c "from rest_framework_simplejwt.tokens import RefreshToken; from django.contrib.auth.models import User; user = User.objects.first(); refresh = RefreshToken.for_user(user); print(refresh.access_token)"

# 3. Verify JWT authentication is in REST_FRAMEWORK settings
python -c "from django.conf import settings; print(settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])"

# 4. Check token format in Authorization header
# Format: Authorization: Bearer <token>
# NOT: Authorization: Token <token>
```

### Issue: CORS Error When Accessing from Frontend

**Symptoms:** Browser console shows `Access-Control-Allow-Origin` error

**Solutions:**
```python
# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

# Configure CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://app.example.com",
]
```

### Issue: Missing Required Environment Variable

**Symptoms:** `RuntimeError: Required environment variable 'X' is not set`

**Solutions:**
```bash
# 1. Check which variable is missing from error message

# 2. Copy .env.example and configure
cp .env.example .env
nano .env  # Edit to set all required variables

# 3. Source the .env file before running
set -a  # Export all variables
source .env
set +a
python manage.py runserver
```

---

## Best Practices

### Security Best Practices

1. **Never commit `.env` files to version control**
   ```bash
   echo ".env" >> .gitignore
   echo ".env.local" >> .gitignore
   echo "*.key" >> .gitignore
   ```

2. **Use strong, unique secrets for each environment**
   ```bash
   # Generate 50-character random secret
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

3. **Rotate secrets regularly** (especially in production)
   - Change `SECRET_KEY` and `JWT_SIGNING_KEY` at least annually
   - Update immediately if exposed

4. **Use HTTPS in production**
   ```python
   if APP_ENV == 'production':
       SECURE_SSL_REDIRECT = True
       SESSION_COOKIE_SECURE = True
       CSRF_COOKIE_SECURE = True
   ```

5. **Monitor token usage**
   - Implement token blacklisting for logout
   - Log authentication attempts
   - Alert on repeated failed attempts

### Configuration Best Practices

1. **Document all environment variables in `.env.example`**
   - Include default values
   - Add descriptions for each variable
   - Mark required vs optional

2. **Use type-safe environment access**
   ```python
   # Good
   PAGE_SIZE = int(get_env('PAGE_SIZE', 20))
   DEBUG = get_bool('DEBUG', False)
   
   # Avoid
   PAGE_SIZE = os.getenv('PAGE_SIZE')  # Returns string
   ```

3. **Validate configuration on startup**
   ```python
   def validate_settings():
       """Validate critical settings on Django startup."""
       errors = []
       
       if APP_ENV == 'production':
           if SECRET_KEY.startswith('dev-'):
               errors.append("SECRET_KEY still has development prefix")
           if not ALLOWED_HOSTS:
               errors.append("ALLOWED_HOSTS not configured for production")
       
       if errors:
           raise RuntimeError(f"Configuration errors:\n" + "\n".join(errors))
   
   # Call in settings.py
   validate_settings()
   ```

4. **Keep secrets out of logs**
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'standard': {
               'format': '{levelname} {asctime} {name} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.FileHandler',
               'filename': 'debug.log',
               'formatter': 'standard',
           },
       },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
            },
        },
    }
   ```

### Testing Best Practices

1. **Test with real environment variables in CI**
   ```yaml
   # GitHub Actions Example
   env:
     APP_ENV: test
     DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
     SECRET_KEY: test-secret-key
   ```

2. **Use separate test settings**
   ```bash
   # Create config/test_settings.py
   # Reference in test runner: python manage.py test --settings=config.test_settings
   ```

3. **Mock external services in tests**
   ```python
   from unittest.mock import patch
   
   @patch('apps.billing.services.TaxService')
   def test_order_with_tax(self, mock_tax_service):
       mock_tax_service.calculate.return_value = 10.0
       # Test code
   ```

---

## References

### Official Documentation
- [Django Settings Documentation](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
- [12 Factor App - Config](https://12factor.net/config)

### Security Resources
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)

### Related Features
- [FEAT202605311310 - Backend API Routing & Contracts](FEAT202605311310-backend-api-routing-contracts.md)
- [FEAT202605311315 - Core Models & Migrations](FEAT202605311315-backend-core-models-migrations.md)
- [FEAT202605311300 - Backend Sprint 1 Overview](FEAT202605311300-backend-sprint1-overview.md)

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-05-31 | Backend Team | Created detailed development guide |

## Status

- **Current Status:** In Development
- **Last Updated:** 2026-05-31
- **Next Review:** When implementation is complete
- **Owner:** Backend Team
