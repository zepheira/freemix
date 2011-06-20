"""Views for managing datasets and their associated JSON description files, as
   well as JSON representations of transformed data.
"""
from django.utils.translation import ugettext_lazy as _

from django.http import *
from django.views.defaults import *
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.base import View

from freemix.utils import get_user
from freemix.utils import get_site_url

from freemix.freemixprofile.models import Freemix
from .models import DataProfile, DataFile
from .models import create_dataset

from freemix.transform.forms import FileUploadForm, URLUploadForm
import json

from freemix.utils.views import JSONResponse, JSONView, LegacyListView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from functools import wraps

def is_user(fn):
    def _wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user == kwargs.get("other_user") or request.user.username == kwargs.get("username"):
                return fn(request, *args, **kwargs)
        return HttpResponseForbidden(_("You do not seem to have the "
                                       "appropriate permissions to perform "
                                       "that request."))
    _wrap.__doc__ = fn.__doc__
    _wrap.__dict__ = fn.__dict__

    return wraps(fn)(_wrap)

class DatasetListView(LegacyListView):
    """
    Returns a list of datasets for a particular user on GET.
    """
    template = "dataset/dataset_list_by_owner.html"

    def get_queryset(self, request, username, other_user):
        return DataProfile.objects.filter(user__username=username)

    def extra_context(self, request, username):
        return {"other_user": get_user(username)}

datasets_by_user = DatasetListView()

def get_data_profile(username, slug):
    return get_object_or_404(DataProfile, slug=slug, user__username=username)


class CreateDatasetView(View):
    """
    Create a new Dataset belonging to the specified user based on an
    incoming JSON document
    """

    def create_dataset(self, user, contents):
        """
        Creates the dataset and returns an HTML fragment including the URL for
        the new dataset
        """

        data_profile = create_dataset(user, contents)
        url = data_profile.get_absolute_url()


        return HttpResponse("<span><a href='%s'>%s</a></span>" %
                            (url, get_site_url(url)))

    def extract_content(self, request):
        """
        Defines how the JSON document will be extracted from the incoming
        request
        """
        return request.raw_post_data

    @method_decorator(login_required)
    def post(self, request, username):
        """
        Creates a new dataset on POST.  Expects to be able to extract the
        profile describing the new dataset by calling self.extract_content()
        """
        user = request.user
        contents = json.loads(self.extract_content(request))
        return self.create_dataset(user, contents)

    def put(self, request, *args, **kwargs):
        """
        Creates a new dataset.  Same behavior as POST
        """
        return self.post(request, *args, **kwargs)

publish_dataset = CreateDatasetView.as_view()

class DatasetMetadataView(View):
    """
    Read, update, delete the profile for a particular dataset,
    identified by a username and slug
    """

    def get(self, request, username, slug):
        """
        Return the profile JSON for the requested dataset
        """
        return JSONResponse(get_data_profile(username, slug).get_dict())

    @method_decorator(login_required)
    @method_decorator(is_user)
    def put(self, request, username, slug):
        """
        Updates the dataset profile.  Expects a JSON document.
        """
        contents = json.loads(request.raw_post_data)
        profile = get_data_profile(username, slug)

        profile.update_profile(contents)
        url = profile.get_absolute_url()

        return HttpResponse("<span><a href='%s'>%s</a></span>"
        % (url, get_site_url(url)))

    def post(self, *args, **kwargs):
        self.put(*args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(is_user)
    def delete(self, request, username, slug):
        """
        Deletes the dataset and notifies the owners of all data views that
        reference this profile
        """
        profile = get_data_profile(username, slug)

        # Get children freemixes
        freemixes = Freemix.objects.filter(data_profile=profile)
        # send messages to the owners of each freemix
        profile_url = profile.get_absolute_url()
        for freemix in freemixes:
            if freemix.user:
                freemix_url = freemix.get_absolute_url()
                freemix.user.message_set.create(
                    message=_("The data view at "
                              "%(freemix_url)s has been deleted because the "
                              "data set at %(profile_url)s was deleted") %
                            {'freemix_url': freemix_url,
                             'profile_url': profile_url})

        request.user.message_set.create(
            message=_("The data profile at %(profile_url)s has been deleted") %
                    {'profile_url': profile_url})
        profile.delete()

        return HttpResponse(_("%(file_id)s deleted") % {'file_id': profile_url})

dataset_profile = DatasetMetadataView.as_view()

class DatasetView(DatasetMetadataView):
    """
    Overrides the metadata view to display the HTML viewer for a dataset on GET
    """

    def get(self, request, username, slug,
            template_name="dataset/dataset_detail.html"):
        profile = get_data_profile(username, slug)

        response = render_to_response(template_name, {
            "profile": profile,
            "username": username,
            "slug": slug,
            "user": request.user,
            }, context_instance=RequestContext(request))

        return response

dataset_view = DatasetView.as_view()

@login_required
@is_user
def edit_dataset(request, username, slug,
                 template_name="dataset/dataset_edit.html"):
    """
    Renders the editor for an existing dataset
    """

    profile = get_data_profile(username, slug)


    response = render_to_response(template_name, {
        "username": username,
        "slug": slug,
        "publishurl": profile.get_absolute_url(),
        "file_form": FileUploadForm(),
        "url_form": URLUploadForm(),
        "owner": username
    }, context_instance=RequestContext(request))



    return response


@login_required
def upload_dataset(request, template_name="dataset/upload/upload.html"):
    """
    Renders the editor and forms to create a new dataset
    """
    username = request.user.username


    response = render_to_response(template_name, {
        "username": username,
        "publishurl": reverse("publish_dataset",
                              kwargs={"username": username}),
        "upload": True,
        "file_form": FileUploadForm(),
        "url_form": URLUploadForm(),
        "owner": username
    }, context_instance=RequestContext(request))


    return response
    

class DataFileView(View):
    """
    Provides a somewhat RESTful interface for managing JSON files associated
    with a particular dataset
    """

    filekey = "data.json"
    jsonp_template="dataset/data.js"
    

    def get_json(self, username, slug):
        profile = get_data_profile(username, slug)
        data = get_object_or_404(DataFile, name=self.filekey,
                                 data_profile=profile)
        return data.json

    def get(self, request, username, slug, jsonp=False):
        file_json = self.get_json(username, slug)
        if jsonp:
            response = JSONResponse(file_json, self.jsonp_template,
                                    file_name=self.filekey)
        else:
            response = JSONResponse(file_json)
        return response

    @method_decorator(login_required)
    @method_decorator(is_user)
    def put(self, request, username, slug):
        contents = json.loads(request.raw_post_data)
        profile = get_data_profile(username, slug)

        profile.save_file(self.filekey, contents)
        url = request.build_absolute_uri(request.get_full_path())
        response = HttpResponse("<span><a href='%s'>%s</a></span>"
        % (url, url))

        return response

    def post(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(is_user)
    def delete(self, request, username, slug):
        profile = get_data_profile(username, slug)
        file = get_object_or_404(DataFile, name=self.filekey,
                                 data_profile=profile)
        file.delete()
        response = HttpResponse(_("%(file_id)s deleted") % {'fileid': slug})
        return response

# Returns transformed data
transformed_data = DataFileView.as_view()

# JSON representations of merged datasets
class MergedDataJSONView(JSONView):

    def get_dict(self, *args, **kwargs):
        return get_data_profile(kwargs["username"], kwargs["slug"]).merge_data()

merged_dataset = MergedDataJSONView.as_view()


class EverythingJSONView(JSONView):

    def get_dict(self, *args, **kwargs):
        return get_data_profile(kwargs["username"], kwargs["slug"]).everything()


everything_json = EverythingJSONView.as_view()
editor_jsonp = EverythingJSONView.as_view(template="dataset/edit/data.jsonp")
viewer_jsonp = EverythingJSONView.as_view(template="dataset/view/data.jsonp")