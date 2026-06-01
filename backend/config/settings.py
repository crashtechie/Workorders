import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Enviroment configuration with typed access
def get_env(key, default=None, required=False):
    """
    Safely retrieve environment variables with optional type coercion.
    
    Args:
        key: Environment variable name
        default: Default value if not set (None if required=True)
        required: If True, raises an error if the variable is not set
        
    Returns:
        Value from enviroment or default
        
    Raises:
        RuntimeError: if required key is missing
    """
    value = os.getenv(key, default)
    if value is None and required:
        raise RuntimeError(f"Environment variable '{key}' is required but not set.")
    return value

def get_bool(key, default=False):
    "Convert environment variable to boolean"
    value = get_env(key, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')

# ============================================
# APPLICATION ENVIRONMENT CONFIGURATION
# ============================================
APP_ENV = get_env('APP_ENV', 'development')
DEBUG = APP_ENV in ('development', 'test')

if APP_ENV == 'production':
    ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', '').split(',')
    if not ALLOWED_HOSTS or not ALLOWED_HOSTS[0]:
        raise RuntimeError(
            "In Production, ALLOWED_HOSTS must be set to a comma-separated list of allowed hostnames."
            "Example: ALLOWED_HOSTS=example.com,www.example.com"
        )
    else:
        ALLOWED_HOSTS = ['*'] # Allow all hosts in development and test environments
        
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

# ==============================================
# DATABASE CONFIGURATION
# ==============================================

# Support both DATBASE_URL and individual database settings
DATABASE_URL = get_env('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL, 
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Database connection pooling for production
if APP_ENV == 'production':
    DATABASES['default']['CONN_MAX_AGE'] = 600  # Keep connections open for 10 minutes
    DATABASES['default']['CONN_HEALTH_CHECKS'] = True  # Enable health checks for persistent connections
    
# ============================================
# SECRET KEY & SECURITY
# ============================================
if APP_ENV == 'production':
    SECRET_KEY = get_env('SECRET_KEY', required=True)
else:
    SECRET_KEY = get_env(
        'SECRET_KEY',
        'dev-unsafe-change-in-production-' + 'x' * 40 
    )
    
# =============================================
# DJANGO REST FRAMEWORK CONFIGURATION
# =============================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(get_env('PAGE_SIZE', 20)),
    
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}

# ============================================
# SIMPLE JWT CONFIGURATION
# ============================================
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=int(get_env('ACCESS_TOKEN_LIFETIME_MINUTES', 15))
    ), 
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=int(get_env('REFRESH_TOKEN_LIFETIME_DAYS', 7))
    ),
    'ROTATE_REFRESH_TOKENS': get_bool('ROTATE_REFRESH_TOKENS', True),
    'BLACKLIST_AFTER_ROTATION': get_bool('BLACKLIST_AFTER_ROTATION', True),
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': get_env(
        'JWT_SIGNING_KEY',
        SECRET_KEY if APP_ENV == 'development' else None # Use Django's SECRET_KEY as fallback for JWT signing  
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

# ============================================
# BUSINESS LOGIGIC CONFIGURATION
# ============================================

# TAX calculation
DEFAULT_TAX_RATE = float(get_env('DEFAULT_TAX_RATE', 0.00))  # Default tax rate of 0%

# AUDIT LOGGING
AUDIT_LOGGING_ENABLED = get_bool('AUDIT_LOGGING_ENABLED', True)
AUDIT_LOG_RETENTION_DAYS = int(get_env('AUDIT_LOG_RETENTION_DAYS', 90))  # Retain logs for 90 days

# Pagination defaults
DEFAULT_PAGE_SIZE = int(get_env('DEFAULT_PAGE_SIZE', 20))
MAX_PAGE_SIZE = int(get_env('MAX_PAGE_SIZE', 100))

# API versioning
API_VERSION = get_env('API_VERSION', 'v1')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-3a=dw%telu8(@wwohrz!wf8=1yr*9!u(0l8ccravxn&b2tf52='

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#ALLOWED_HOSTS = ['*']



# Application definition

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
    'corsheaders',
    
    # Local apps
    'apps.audit',
    'apps.authz',
    'apps.billing',
    'apps.customers',
    'apps.inventory',
    'apps.reports',
    'apps.workorders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
