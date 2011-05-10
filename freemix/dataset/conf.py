from django.conf import settings
from urlparse import urljoin

AKARA_URL_PREFIX = getattr(settings, "AKARA_URL_PREFIX", "http://transformer.zepheira.com:8883")
AKARA_VERSION_URL = getattr(settings, "AKARA_VERSION_URL", urljoin(AKARA_URL_PREFIX, "freemix.loader.revision"))
AKARA_TRANSFORM_URL = getattr(settings, "AKARA_TRANSFORM_URL", urljoin(AKARA_URL_PREFIX, "freemix.json"))
AKARA_CONTENTDM_URL = getattr(settings, "AKARA_CONTENTDM_URL", urljoin(AKARA_URL_PREFIX, "contentdm.json"))
AKARA_OAIPMH_URL = getattr(settings, "AKARA_OAIPMH_URL", urljoin(AKARA_URL_PREFIX, "oaipmh.json"))

  