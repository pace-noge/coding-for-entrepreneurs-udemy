import os
from django.conf import settings


DEBUG = False

TEMPLATE_DEBUG = True

DATABASES = settings.DATABASES

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "static_dirs"),
)
