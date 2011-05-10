from freemix.utils.views import JSONView
from freemix.transform.views import TransformView
import models

pattern_jsonp = JSONView(models.ListPattern.to_dict, "freemix/augment/patterns.js")
pattern_json = JSONView(models.ListPattern.to_dict)

error_json = JSONView(models.AugmentationErrorCode.to_dict)

transform = TransformView(models.augment_client)
