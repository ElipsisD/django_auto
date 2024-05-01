import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))

COMMAND_EXECUTOR = env.str("SELENIUM_DOMAIN")

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG")

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS").split()
CSRF_TRUSTED_ORIGINS = env.str("CSRF_TRUSTED_ORIGINS").split()

AUTODOC_LOGIN = env.str("AUTODOC_LOGIN")
AUTODOC_PASSWORD = env.str("AUTODOC_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("DB_HOST"),
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIR = [
    os.path.join(BASE_DIR, "static/"),
]

CELERY_BROKER_URL = env.str("REDIS_DOMAIN")
CELERY_TIMEZONE = "Asia/Krasnoyarsk"
CELERY_RESULT_BACKEND = env.str("REDIS_DOMAIN")

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
