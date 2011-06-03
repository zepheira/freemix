from freemix.utils.views import JSONView
from freemix.transform.views import RawTransformView, AkaraTransformClient
from freemix.augment import models
from freemix.augment import conf


class ListPatternJSONView(JSONView):
    def get_dict(self, *args, **kwargs):
        return models.ListPattern.to_dict()


pattern_jsonp = ListPatternJSONView.as_view(template="freemix/augment/patterns.js")
pattern_json = ListPatternJSONView.as_view()


class AugmentationErrorJSONView(JSONView):
    def get_dict(self, *args, **kwargs):
        return models.AugmentationErrorCode.to_dict()


error_json = AugmentationErrorJSONView.as_view()


transform = RawTransformView.as_view(transform=AkaraTransformClient(conf.AKARA_AUGMENT_URL))
