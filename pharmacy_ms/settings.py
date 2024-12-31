"""
Django settings for pharmacy_ms project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages_constant

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1^yuf2@hc*-jg&bk7ukaa!si3wr6)x4)uh2z@mgyavuh3h*unf"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["pharmacy-management-system-yqms.onrender.com", '127.0.0.1']



# Application definition
AUTH_USER_MODEL = "authentication.PharmacyUser"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
     "authentication",
     "useradmin",
     'django.contrib.humanize',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "pharmacy_ms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "pharmacy_ms/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "authentication.backends.PharmacyAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

WSGI_APPLICATION = "pharmacy_ms.wsgi.application"
X_FRAME_OPTIONS = 'SAMEORIGIN'
MESSAGE_TAGS = {
    messages_constant.ERROR: 'danger',
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.postgresql',
# 'NAME': 'pharmacy_ms',
# 'USER': 'pharmacy_ms_user',
# 'PASSWORD': '1XVxUSy8Ju7P6C2cHX9ghdX0IkUAlzhN',
# 'HOST': 'dpg-ctl64v3v2p9s738dk7lg-a.oregon-postgres.render.com',
# 'PORT': '5432',  
# 'CONN_MAX_AGE': 60
# }
# }


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'pharmacy_ms',
'USER': 'pharmacy_ms_user',
'PASSWORD': '1XVxUSy8Ju7P6C2cHX9ghdX0IkUAlzhN',
'HOST': 'dpg-ctl64v3v2p9s738dk7lg-a',
'PORT': '5432',  
'CONN_MAX_AGE': 60
}
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
 
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / "pharmacy_ms" / "static",
    BASE_DIR / "useradmin" / "static",
  
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "impanomanzienock@gmail.com"
EMAIL_HOST_PASSWORD = "zjrvwmqirryvjjvz"

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
PROFILE_IMAGE_SIZE = 2 * 1024 * 1024
RESET_TOKEN_TIMEOUT=60

LOGIN_URL = 'login'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'OPTIONS': {
            'location': BASE_DIR / 'media', 
        },
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

