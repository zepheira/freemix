from django.conf import settings
from urlparse import urljoin

AKARA_URL_PREFIX = getattr(settings, "AKARA_URL_PREFIX", "http://transformer.zepheira.com:8883")
AKARA_TRANSFORM_URL = getattr(settings, "AKARA_TRANSFORM_URL", urljoin(AKARA_URL_PREFIX, "freemix.json"))