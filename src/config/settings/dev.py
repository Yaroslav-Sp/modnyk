from config.settings.base import *  # NOQA
from config.settings.prod import DATABASES

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lhmdb$*b4-gvlxqaz76gc)00h*t+y6c!2a*=70ckth^awqt%*u"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ["django_extensions"]  # NOQA

if os.environ.get("GITHUB_WORKFLOW"):  # NOQA
    DATABASES = {  # NOQA
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",  # NOQA
            "USER": "postgres",  # NOQA
            "PASSWORD": "postgres",  # NOQA
            "HOST": "0.0.0.0",  # NOQA
            "PORT": 5432,  # NOQA
        }
    }
else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),  # NOQA
            "USER": os.environ.get("POSTGRES_USER"),  # NOQA
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),  # NOQA
            "HOST": os.environ.get("POSTGRES_HOST"),  # NOQA
            "PORT": os.environ.get("POSTGRES_PORT"),  # NOQA
        },
        # "default_sqlite": {
        #     "ENGINE": "django.db.backends.sqlite3",
        #     "NAME": BASE_DIR / "db.sqlite3",  # NOQA
        # }
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
