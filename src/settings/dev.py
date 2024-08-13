from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


WAGTAILADMIN_BASE_URL = "http://localhost:8000"


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
