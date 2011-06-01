"""Views for managing datasets and their associated JSON description files, as
   well as JSON representations of transformed data.
"""
from django.utils.translation import ugettext_lazy as _

from django.http import *
from django.views.defaults import *
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.base import View, TemplateView

from freemix.utils import get_user
from freemix.utils import get_site_url

from .decorators import is_user
from freemix.freemixprofile.models import Freemix
from .models import DataProfile, DataFile
from .models import create_dataset

from freemix.transform.forms import FileUploadForm, URLUploadForm
import json

from freemix.utils.views import RESTResource, JSONResponse, JSONView, ListView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DatasetListView(ListView):
    """
    Returns a list of datasets for a particular user on GET.
    """
    template = "dataset/list/dataset_list_by_user.html"

    def get_queryset(self, request, username, other_user):
        return DataProfile.objects.filter(user__username=username)

    def extra_context(self, request, username):
        return {"other_user": get_user(username)}

datasets_by_user = DatasetListView()

def get_data_profile(username, slug):
    return get_object_or_404(DataProfile, slug=slug, user__username=username)


class CreateDatasetView(RESTResource):
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
        url = data_profile.get_url_path()


        return HttpResponse("<span><a href='%s'>%s</a></span>" %
                            (url, get_site_url(url)))

    def extract_content(self, request):
        """
        Defines how the JSON document will be extracted from the incoming
        request
        """
        return request.raw_post_data

    @method_decorator(login_required)
    def POST(self, request, username):
        """
        Creates a new dataset on POST.  Expects to be able to extract the
        profile describing the new dataset by calling self.extract_content()
        """
        user = request.user
        contents = json.loads(self.extract_content(request))
        return self.create_dataset(user, contents)

    def PUT(self, *args, **kwargs):
        """
        Creates a new dataset.  Same behavior as POST
        """
        return self.POST(*args, **kwargs)

publish_dataset = CreateDatasetView()

class DatasetMetadataView(RESTResource):
    """
    Read, update, delete the profile for a particular dataset,
    identified by a username and slug
    """

    def GET(self, request, username, slug):
        """
        Return the profile JSON for the requested dataset
        """
        return JSONResponse(get_data_profile(username, slug).get_dict())

    @method_decorator(login_required)
    @method_decorator(is_user)
    def PUT(self, request, username, slug):
        """
        Updates the dataset profile.  Expects a JSON document.
        """
        contents = json.loads(request.raw_post_data)
        profile = get_data_profile(username, slug)

        profile.update_profile(contents)
        url = profile.get_url_path()

        return HttpResponse("<span><a href='%s'>%s</a></span>"
        % (url, get_site_url(url)))

    def POST(self, *args, **kwargs):
        self.PUT(*args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(is_user)
    def DELETE(self, request, username, slug):
        """
        Deletes the dataset and notifies the owners of all data views that
        reference this profile
        """
        profile = get_data_profile(username, slug)

        # Get children freemixes
        freemixes = Freemix.objects.filter(data_profile=profile)
        # send messages to the owners of each freemix
        profile_url = profile.get_url_path()
        for freemix in freemixes:
            if freemix.user:
                freemix_url = freemix.get_url_path()
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

dataset_profile = DatasetMetadataView()

class DatasetView(DatasetMetadataView):
    """
    Overrides the metadata view to display the HTML viewer for a dataset on GET
    """

    def GET(self, request, username, slug,
            template_name="dataset/view/view.html"):
        profile = get_data_profile(username, slug)

        response = render_to_response(template_name, {
            "profile": profile,
            "username": username,
            "slug": slug,
            "user": request.user,
            }, context_instance=RequestContext(request))

        return response

dataset_view = DatasetView()

@login_required
@is_user
def edit_dataset(request, username, slug,
                 template_name="dataset/edit/build.html"):
    """
    Renders the editor for an existing dataset
    """

    profile = get_data_profile(username, slug)


    response = render_to_response(template_name, {
        "username": username,
        "slug": slug,
        "publishurl": profile.get_url_path(),
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
    

class DataFileView(RESTResource):
    """
    Provides a somewhat RESTful interface for managing JSON files associated
    with a particular dataset
    """

    def __init__(self, filekey="data.json",
                 jsonp_template="dataset/data.js"):
        self.filekey = filekey
        self.jsonp_template = jsonp_template

    def get_json(self, username, slug):
        profile = get_data_profile(username, slug)
        data = get_object_or_404(DataFile, name=self.filekey,
                                 data_profile=profile)
        return data.json

    def GET(self, request, username, slug, jsonp=False):
        file_json = self.get_json(username, slug)
        if jsonp:
            response = JSONResponse(file_json, self.jsonp_template,
                                    file_name=self.filekey)
        else:
            response = JSONResponse(file_json)
        return response

    @method_decorator(login_required)
    @method_decorator(is_user)
    def PUT(self, request, username, slug):
        contents = json.loads(request.raw_post_data)
        profile = get_data_profile(username, slug)

        profile.save_file(self.filekey, contents)
        url = request.build_absolute_uri(request.get_full_path())
        response = HttpResponse("<span><a href='%s'>%s</a></span>"
        % (url, url))

        return response

    def POST(self, request, *args, **kwargs):
        return self.PUT(request, *args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(is_user)
    def DELETE(self, request, username, slug):
        profile = get_data_profile(username, slug)
        file = get_object_or_404(DataFile, name=self.filekey,
                                 data_profile=profile)
        file.delete()
        response = HttpResponse(_("%(file_id)s deleted") % {'fileid': slug})
        return response

# Returns transformed data
transformed_data = DataFileView("data.json", "dataset/data.js")

# JSON representations of merged datasets
def get_merge_data(username, slug):
    return get_data_profile(username, slug).merge_data()

merged_dataset = JSONView(get_merge_data)

def get_everything(username, slug):
    return get_data_profile(username, slug).everything()

everything_json = JSONView(get_everything)
editor_jsonp = JSONView(get_everything, "dataset/edit/data.jsonp")
viewer_jsonp = JSONView(get_everything, "dataset/view/data.jsonp")
