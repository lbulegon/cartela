"""
Django settings for cartela project.
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS - aceita domínios do Railway automaticamente
ALLOWED_HOSTS_ENV = config('ALLOWED_HOSTS', default='', cast=str)
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')]
else:
    # Verifica se está rodando no Railway
    is_railway = (
        os.getenv('RAILWAY_ENVIRONMENT') or 
        os.getenv('RAILWAY_SERVICE_NAME') or
        os.getenv('PORT')  # Railway sempre define PORT
    )
    
    if is_railway:
        # Em produção (Railway), aceita todos os domínios .railway.app
        ALLOWED_HOSTS = ['.railway.app', '.up.railway.app']
    else:
        # Desenvolvimento local
        ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CSRF Trusted Origins - permite requisições do Railway
CSRF_TRUSTED_ORIGINS_ENV = config('CSRF_TRUSTED_ORIGINS', default='', cast=str)
if CSRF_TRUSTED_ORIGINS_ENV:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_ENV.split(',')]
else:
    # Verifica se está rodando no Railway
    is_railway = (
        os.getenv('RAILWAY_ENVIRONMENT') or 
        os.getenv('RAILWAY_SERVICE_NAME') or
        os.getenv('PORT')
    )
    
    if is_railway:
        # Em produção (Railway), adiciona domínios
        # Nota: Django não suporta wildcards, então precisamos adicionar domínios específicos
        railway_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
        csrf_origins = []
        
        # Adiciona domínio público do Railway se disponível
        if railway_domain:
            csrf_origins.append(f'https://{railway_domain}')
        
        # Adiciona domínios comuns do Railway
        csrf_origins.extend([
            'https://cartela-development.up.railway.app',
            # Adicione outros domínios do Railway aqui conforme necessário
        ])
        
        CSRF_TRUSTED_ORIGINS = csrf_origins
        CSRF_COOKIE_SECURE = True
        CSRF_COOKIE_SAMESITE = 'Lax'
    else:
        # Desenvolvimento local
        CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    # Apps locais
    'app_cartela',
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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# ========================
# Banco de Dados
# ========================

# Railway usa DATABASE_URL automaticamente
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Produção (Railway)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Desenvolvimento local - busca do .env
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='railway'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='jcIUPXPaIAOHWcUhVBVsGRWFbjkIsMoX'),
            'HOST': config('DB_HOST', default='yamabiko.proxy.rlwy.net'),
            'PORT': config('DB_PORT', default='26292'),
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# STATICFILES_DIRS só em desenvolvimento (se o diretório existir)
static_dir = BASE_DIR / 'static'
if static_dir.exists():
    STATICFILES_DIRS = [static_dir]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'app_cartela:login'
LOGIN_REDIRECT_URL = 'app_cartela:dashboard'
LOGOUT_REDIRECT_URL = 'app_cartela:login'

