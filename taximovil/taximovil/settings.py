"""
Django settings for taximovil project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3gcv0hu#@&41478@pp7+i*ue0z$=q*14)_#h3uvf#ly&^=e5+%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '35.155.214.25']

AUTH_USER_MODEL = 'config.Usuario'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'fcm_django',
    'config.apps.ConfigConfig',
    'webapp.apps.WebappConfig',
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

ROOT_URLCONF = 'taximovil.urls'

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

WSGI_APPLICATION = 'taximovil.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'taximovildb',
        'USER': 'taximovildb',
        'PASSWORD': 'i3N%g6$uE-F8',
        'HOST': 'postgrestaximovil.cl7uq5voofn2.us-west-2.rds.amazonaws.com',
        'PORT': '5432'
    },
    # 'default': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'NAME': 'taximovil',
    #     'USER': 'postgres',
    #     'PASSWORD': 'n0m3l0s3',
    #     'HOST': 'localhost',
    #     'PORT': '5432'
    # },
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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, "taximovil/static"), ]

STATIC_URL = "/static/"

MEDIA_URL = "/media/"

STATIC_ROOT = "/var/django/static/"

MEDIA_ROOT = "/var/django/media/"

FILE_UPLOAD_PERMISSIONS = 0o644

CONEKTA_PRIVATE_KEY = 'key_rt8Pspor443aAyiVqGJRyg'
CONEKTA_PUBLIC_KEY = 'key_MSsP3AaNQ5j8yCEb57ms4EA'
CONEKTA_LOCALE = 'es'
CONEKTA_VERSION = '2.0.0'

TWILIO_NUMBER = '+18182755763'
TWILIO_TOKEN = 'fd5a055b5112f98c287e7905e9458744'
TWILIO_SID = 'AC6f1b0f55393a44a5049348073a6fc895'
GOOGLE_MAPS_KEY = 'AIzaSyA1A_A1RVbjaW-YQFtVW4ie3PlTyz2UauQ'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M",
}

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AIzaSyCgzPI09rajeH0azwz8UAbmIAvRCTkFetY",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
}


EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIAIOVOEHAPD7XY6Q5Q'
EMAIL_HOST_PASSWORD = 'AstnGpe2+cG2R1mAnwlX87I6V2aXCNd/yFPmUfBjvqun'

DEFAULT_FROM_EMAIL = 'contacto@taximovil.com.mx'
SERVER_EMAIL = 'contacto@taximovil.com.mx'