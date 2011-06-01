from freemix.utils.views import JSONView
from freemix.transform.views import RawTransformView, AkaraTransformClient
import models
from . import conf

pattern_jsonp = JSONView(models.ListPattern.to_dict, "freemix/augment/patterns.js")
pattern_json = JSONView(models.ListPattern.to_dict)

error_json = JSONView(models.AugmentationErrorCode.to_dict)

transform = RawTransformView.as_view(transform=AkaraTransformClient(conf.AKARA_AUGMENT_URL))
