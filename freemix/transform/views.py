"""Views for transforming data via akara"""

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
import urllib2
from urllib import urlencode
from freemix.transform.forms import URLUploadForm,FileUploadForm
from freemix.utils.views import RESTResource, JSONResponse
from . import conf

import json
import cgi

ERROR = _("Error uploading and transforming data.  Please contact support.\n")

from django.core.cache import cache

def get_akara_version():
    version = cache.get("akara_version")
    if not version:
        version = cache_akara_version()
    return str(version)

def cache_akara_version():
    try:
        version = urllib2.urlopen(conf.AKARA_VERSION_URL).read(100)
    except:
        version = "Unknown"
    cache.set("akara_version", version, 60)
    return version

class AkaraTransformClient(object):
    def __init__(self, url, credentials=None):
        self.akara_url = url
        self.credentials = credentials

    def _akara_call(self, url, params={}, body=None, diagnostics=False):
        if diagnostics:
            params['diagnostics'] = 'yes'
        if self.credentials:
            auth_handler= urllib2.HTTPDigestAuthHandler()
            auth_handler.add_password(realm=self.credentials[0],
                                      uri=url,
                                      user=self.credentials[1],
                                      passwd=self.credentials[2])
            opener = urllib2.build_opener(auth_handler)
        else:
            opener=urllib2.build_opener()
        r = urllib2.Request('%s?%s' % (url, urlencode(params)), body)
        data = json.load(opener.open(r))
        return data

    def transform(self, contents, diagnostics=False):
        return self._akara_call(self.akara_url, body=contents, diagnostics=diagnostics)

    def contentdm(self, params, diagnostics=False):
        params['limit'] = 100
        return self._akara_call(conf.AKARA_CONTENTDM_URL, params=params, diagnostics=diagnostics)

    def oaipmh(self, params, diagnostics=False):
        return self._akara_call(conf.AKARA_OAIPMH_URL, params=params, diagnostics=diagnostics)

transform_client = AkaraTransformClient(conf.AKARA_TRANSFORM_URL)

class TransformView(RESTResource):
    """Generic transform proxy

    By default, posted data is sent directly to the provided client.  If the
    request included a `X-Data-Load-TxId` header, it will be included in the
    response as well.
    """
    def __init__(self, proxy = None):
        self.proxy = proxy or transform_client

    def __call__(self, request, *args, **kwargs):
        # Extract client provide transaction ID and append it to the response
        response = super(TransformView, self).__call__(request, args, kwargs)
        txid = request.META.get("HTTP_X_DATA_LOAD_TXID", None)
        if txid:
            response["X-Data-Load-TxId"] = txid
        return response

    def POST(self, request, *args, **kwargs):
        data = self.proxy.transform(request.raw_post_data)
        if data:
            return JSONResponse(data)
        return HttpResponseBadRequest()

class FileTransformView(TransformView):

    def __init__(self, proxy=None, form_class=None):
        super(FileTransformView, self).__init__(proxy)
        self.form_class = form_class or FileUploadForm

    def POST(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            input = file.read()
            file.close()
            output = self.proxy.transform(input, diagnostics=form.cleaned_data["diagnostics"])
            if not output:
                return HttpResponseBadRequest(_("Invalid Request"))
            output = "<textarea>%s</textarea>"% cgi.escape(json.dumps(output))
            response = HttpResponse(output)
            response['Content-Type'] = "text/html"
            return response
        return HttpResponseBadRequest()

class URLTransformView(TransformView):
    def __init__(self, proxy=None, form_class=None):
        super(URLTransformView, self).__init__(proxy)
        self.form_class = form_class or URLUploadForm

    def GET(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            url = form.cleaned_data['url']
            service = form.cleaned_data['service']
            diagnostics = form.cleaned_data['diagnostics']
            if service == 'cdm':
                cdm_collection_name = form.cleaned_data['cdm_collection_name']
                cdm_search_term = form.cleaned_data['cdm_search_term']
                params = {'site': url}
                if cdm_collection_name:
                    params["collection"] = cdm_collection_name
                if cdm_search_term:
                    params["query"] = cdm_search_term
                data = self.proxy.contentdm(params, diagnostics=diagnostics)
                if data:
                    return JSONResponse(data)
            elif service == 'oai':
                return None
            else:
                r= urllib2.urlopen(url)
                contents = r.read()
                data = self.proxy.transform(contents, diagnostics=diagnostics)
                if data:
                    return JSONResponse(data)
        return HttpResponseBadRequest()


