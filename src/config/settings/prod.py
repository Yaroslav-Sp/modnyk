import os

from config.settings.base import *  # NOQA

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["localhost", 'ec2-13-53-130-108.eu-north-1.compute.amazonaws.com']  # NOQA


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
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
