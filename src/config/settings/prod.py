import os

from config.settings.base import *  # NOQA

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost"]  # NOQA


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),  # NOQA
        "USER": os.environ.get("POSTGRES_USER"),  # NOQA
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),  # NOQA
        "HOST": os.environ.get("POSTGRES_HOST"),  # NOQA
        "PORT": os.environ.get("POSTGRES_PORT"),  # NOQA
    },
    "default sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"  # NOQA
STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media"  # NOQA
MEDIA_URL = "media/"
