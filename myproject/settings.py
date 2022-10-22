"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import sys
import django_heroku


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (os.environ.get('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('DEBUGMODE') == 'True':
    DEBUG = (os.environ.get('DEBUGMODE') == 'True')
else:
    DEBUG = (os.environ.get('DEBUGMODE') != 'False')

if os.environ.get('PRODUCTIONVERSION') == 'True':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    
ALLOWED_HOSTS = [
    'https://find-your-garage.herokuapp.com',
    'https://znajdzwarsztacik.pl',
    'https://www.znajdzwarsztacik.pl',
    'localhost',
    '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My Applications
    'accounts',
    'main',
    'garages',

    # Third-party software
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap5',
    'anymail',
    'address',
    'places',
    'widget_tweaks',
]

SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'account_login'

DEFAULT_FROM_EMAIL = 'support@znajdzwarsztacik.pl'

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    "MAILGUN_SENDER_DOMAIN": 'mg.znajdzwarsztacik.pl',
}


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
PLACES_MAPS_API_KEY = os.environ.get('GOOGLE_API_KEY')
PLACES_MARKER_OPTIONS = '{"draggable": true}'
PLACES_MAP_WIDGET_HEIGHT = 480

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME_TEST'),
            'USER': os.environ.get('DBUSER_TEST'),
            'PASSWORD': os.environ.get('DBPASSWORD_TEST'),
            'HOST': os.environ.get('DBENDPOINT_TEST'),
            'PORT': os.environ.get('DBPORT'),
            'TEST': {
                'NAME': os.environ.get('DBNAME_TEST'),
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME'),
            'USER': os.environ.get('DBUSER'),
            'PASSWORD': os.environ.get('DBPASSWORD'),
            'HOST': os.environ.get('DBENDPOINT'),
            'PORT': os.environ.get('DBPORT'),
            'TEST': {
                'NAME': os.environ.get('DBNAME'),
            }
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pl-pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ['static']
STATIC_ROOT = BASE_DIR / "staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Activate Django-Heroku.
django_heroku.settings(locals())
