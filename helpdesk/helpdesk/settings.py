"""
Django settings for helpdesk project.
Most configuration can be accomplished thought the config.json file.
This file may be overwritten by updates. There should not be a need to edit it.
"""

import os
import json

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2018, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.config/helpdesk/config.json')

with open(CONFIG_FILE, 'r') as f:
    CONFIG = json.load(f)

# SECURITY WARNING: keep the secret key used in production secret!
# A new secret key can be easily generated using scripts/update_secret_key.py
SECRET_KEY = CONFIG['secret_key']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(CONFIG['debug'])


ALLOWED_HOSTS = CONFIG['allowed_hosts']

# Application definition

INSTALLED_APPS = [
    'userportal.apps.UserportalConfig',
    'tickets.apps.TicketsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
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

ROOT_URLCONF = 'helpdesk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates', ],
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

WSGI_APPLICATION = 'helpdesk.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

ACTIVE_DB = CONFIG['databases']['active_db']

DATABASES = {
    'default': CONFIG['databases'][ACTIVE_DB]
}

# Password validation

# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

# set timezone here
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media Files To Be Served Statically
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Setting for Google Authentication
# These can be configured in config.json
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = CONFIG['google_oauth2']['key']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = CONFIG['google_oauth2']['secret']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = CONFIG['google_oauth2']['domain_whitelist']

# Email Server Settings - Used to send email
# These can be configured in config.json
EMAIL_HOST = CONFIG['email_server']['host']
EMAIL_PORT = CONFIG['email_server']['port']
EMAIL_HOST_USER = CONFIG['email_server']['user']
EMAIL_HOST_PASSWORD = CONFIG['email_server']['password']
EMAIL_USE_TLS = CONFIG['email_server']['use_tls']
