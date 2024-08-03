import os
from .base import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['*']

MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
# STORAGES['STATICFILES_STORAGE'] = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STORAGES['STATICFILES_STORAGE'] = 'django.contrib.staticfiles.storage.StaticFilesStorage'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
# SECURE_HSTS_SECONDS = int(
#     os.environ.get("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS)
# ) 
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# REFERRER_POLICY = os.environ.get(  # noqa
#     "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
# ).strip()

# WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"


try:
    from .local import *
except ImportError:
    pass
