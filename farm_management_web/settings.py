"""
Django settings for farm_management_web project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import dotenv
dotenv.load_dotenv()
from pathlib import Path
import os
import sys
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = '/login/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Controls the HTTP Strict Transport Security (HSTS) policy
SECURE_HSTS_SECONDS = 31536000

# All HTTP requests are redirected to HTTPS
# SECURE_SSL_REDIRECT = True

# Session cookies are only sent over HTTPS connections
# SESSION_COOKIE_SECURE = True

# CSRF cookies are only sent over HTTPS connections,
# CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS) policy includes all subdomains of your site
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Site can be submitted to the browser preload list,
SECURE_HSTS_PRELOAD = True

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False

DEBUG = False

ALLOWED_HOSTS = ['157.245.103.7', 'windwoodfarmersnetwork.com', '127.0.0.1']

print(f"__file__: {__file__}")
BASE_DIR = Path(__file__).resolve().parent.parent
print(f"BASE_DIR: {BASE_DIR}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'fontawesomefree',
    'channels',
]

ASGI_APPLICATION = "farm_management_web.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('157.245.103.7', 6379), ('127.0.0.1', 6379)],
        },
    }
}

CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'channels.middleware.WebSocketMiddleware'
]

ROOT_URLCONF = 'farm_management_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'farm_management_web.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#  Postgres database connection
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'False') == 'True'

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            }
            }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv('DATABASE_URL', None) is None:
        raise Exception('DATABASE_URL environment variable not defined!!!')
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL")),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Additional directories to look for static files during development
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Directory where collected static files will be stored
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'main.CustomUser'

# URL to redirect to after changing the password
PASSWORD_RESET_COMPLETE = '/login'

# # #  set up to send emails 
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True    
# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = '2525'

