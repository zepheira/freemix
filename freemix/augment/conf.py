from django.conf import settings
from urlparse import urljoin
from freemix.transform import conf as transform_conf

AKARA_AUGMENT_URL = getattr(settings, "AKARA_AUGMENT_URL", urljoin(transform_conf.AKARA_URL_PREFIX, "augment.freemix.json"))



