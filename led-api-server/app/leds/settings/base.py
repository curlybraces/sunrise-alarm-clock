"""
Django settings for leds project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "corsheaders",
    "rest_framework",
    "alarms",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "leds.urls"

WSGI_APPLICATION = "leds.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Allow cross-site requests
CORS_ORIGIN_ALLOW_ALL = True


# Set up file logging on production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "apilogfile": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "api.log"),
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
        },
        "alarmslogfile": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "alarms.log"),
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
        },
    },
    "loggers": {
        "api": {"handlers": ["apilogfile"], "level": "DEBUG"},
        "alarms": {"handlers": ["alarmslogfile"], "level": "DEBUG"},
    },
}

# ZeroMQ Lazy Pirate settings
REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://zmq:5566"

ALARM_COMMAND = "python3 {} startalarm >> {} 2>&1".format(
    os.path.join(BASE_DIR, "manage.py"), os.path.join(BASE_DIR, "alarm_cron.log")
)

# Shell commands
ALARM_CRONTAB_COMMAND = "sudo python3 {}".format(
    os.path.join(BASE_DIR, "alarms/led_libs/start_alarm.py")
)  # TODO replace
ALARM_STOP_COMMAND = "sudo kill $(ps aux | grep 'start_alarm.py' | awk '{print $2}')"

# Default clock colors
CLOCK_BACKGROUND_COLOR = {"r": 0, "g": 0, "b": 0}
CLOCK_FOREGROUND_COLOR = {"r": 255, "g": 0, "b": 0}
