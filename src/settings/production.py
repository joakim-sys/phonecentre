import os
import random
import string


from .base import *

DEBUG = False

CSRF_TRUSTED_ORIGINS = [
    "https://phonecentre.net",
    "https://www.phonecentre.net",  # Include 'www' if applicable
]

if "DJANGO_SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print(  # noqa: T201
        "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
    )
    SECRET_KEY = "".join(
        [random.SystemRandom().choice(string.printable) for i in range(50)]
    )

# Make sure Django can detect a secure connection properly on Heroku:
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if "PRIMARY_HOST" in os.environ:
    WAGTAILADMIN_BASE_URL = "https://{}".format(os.environ["PRIMARY_HOST"])

WHITENOISE_MANIFEST_STRICT = False
MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

# Front-end cache
# This configuration is used to allow purging pages from cache when they are
# published.
if (
    "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in os.environ
    or "FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN" in os.environ
):
    INSTALLED_APPS.append("wagtail.contrib.frontend_cache")
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "ZONEID": os.environ["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }

    if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in os.environ:
        # To use an account-wide API key, set the following:
        #  * $FRONTEND_CACHE_CLOUDFLARE_TOKEN
        #  * $FRONTEND_CACHE_CLOUDFLARE_EMAIL
        #  * $FRONTEND_CACHE_CLOUDFLARE_ZONEID
        # These can be obtained from a sysadmin.
        WAGTAILFRONTENDCACHE["default"].update(
            {
                "EMAIL": os.environ["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
                "TOKEN": os.environ["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            }
        )

    else:
        # To use an API token with restricted access, set the following:
        #  * $FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN
        #  * $FRONTEND_CACHE_CLOUDFLARE_ZONEID
        WAGTAILFRONTENDCACHE["default"].update(
            {"BEARER_TOKEN": os.environ["FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN"]}
        )

# Force HTTPS redirect (enabled by default!)
# SECURE_SSL_REDIRECT = True

# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
# SECURE_HSTS_SECONDS = int(
#     os.environ.get("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS)
# )  # noqa

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
