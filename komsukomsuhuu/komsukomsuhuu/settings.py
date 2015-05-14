"""
Django settings for komsukomsuhuu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qkpqh1ovl)n8k7%gi_x&erp26icb(e)o10xo!x=h)jr3b30m*r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

# Email Set-up
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'huhukomsukomsu@gmail.com'
EMAIL_HOST_PASSWORD = 'komsuhu123'
DEFAULT_FROM_EMAIL = 'huhukomsukomsu@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_ID=1


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
   #'django.contrib.sessions',
    'user_sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiles',
    'groups',
    'entities',
    'messages',
    'notifications',
    'django_gravatar',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
   #'django.contrib.sessions.middleware.SessionMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SESSION_ENGINE = 'user_sessions.backends.db'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "messages.context_processors.message_count"
)

ROOT_URLCONF = 'komsukomsuhuu.urls'

WSGI_APPLICATION = 'komsukomsuhuu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#Template direction
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "static", "templates"),
)

MEDIA_URL = '/media/'
#STATIC_ROOT = os.path.join(BASE_DIR, "static", "static-only")
MEDIA_ROOT =  os.path.join(BASE_DIR, "static", "media")


