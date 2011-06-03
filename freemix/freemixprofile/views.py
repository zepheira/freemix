from django.contrib.auth.decorators import login_required

import os

from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.http import *
from django.views.defaults import *
from django.views.generic.base import View
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve, reverse

from django.contrib.auth.models import User
from . import models
from freemix.utils import get_site_url

from freemix.dataprofile.models import DataProfile

from freemix.utils import get_user
from freemix.utils.views import ListView
import json
import uuid


def validate_user(user, username=None):
    if username:
        return user.is_authenticated() and user.username == username
    else:
        return user.is_authenticated()


class DataviewsListView(ListView):
    template = "dataview/list/dataview_list_by_user.html"

    def get_queryset(self, request, username, other_user):
        return models.Freemix.objects.filter(user=get_user(username))

    def extra_context(self, request, username):
        return {"other_user": get_user(username)}
dataviews_by_user = DataviewsListView()


class DataviewsByDatasetListView(ListView):
    template = "dataview/list/dataview_list_by_dataset.html"

    def get_queryset(self, request, username, slug, dataset):
        return models.Freemix.objects.filter(data_profile=dataset)

    def extra_context(self, request, username, slug):
        other_user = get_user(username)
        return {"dataset": get_object_or_404(DataProfile, slug=slug,
                                             user=other_user)}
dataviews_by_dataset = DataviewsByDatasetListView()


def create_view_json(data_set_url, canvas="three-column",
    template_name="dataview/profile.js"):
    view, args, kwargs = resolve(data_set_url)
    user = get_object_or_404(User, username=kwargs["username"])
    data_profile = get_object_or_404(DataProfile, slug=kwargs["slug"],
            user=user)

    profile_contents = data_profile.get_dict()
    return json.dumps({
        "dataProfile": data_set_url,
        "theme": "smoothness",
        "properties": [],
        "facets": {},
        "views": {
            "views": [{
                   "id": str(uuid.uuid4()),
                   "type": "list",
                   "name": "List"}]},
        "dataProfiles": {data_set_url: profile_contents},
        "text": {"title": profile_contents["label"]},
        "canvas": canvas})


def process_freemixes(request, username):
    if request.method == 'GET':
        if request.GET.__contains__("build"):
            response = build_freemix(request, username)
        else:
            response = dataviews_by_user(request, username=username)
    elif request.method == 'POST' or request.method == 'PUT':
        response = create_exhibit(request, username)
    else:
        response = HttpResponseForbidden(_("Invalid Request"))
    return response


def process_freemix(request, username, slug, jsonp=False):
    if request.method == 'GET':
        if request.GET.__contains__("format"):
            if request.REQUEST["format"] == 'json':
                response = get_freemix_metadata(request, username, slug, jsonp)
            else:
                response = HttpResponseNotFound()

        elif request.GET.__contains__("build"):
            response = build_freemix(request, username, slug)
        else:
            response = view_freemix(request, username, slug)
    elif request.method == 'POST':
        response = create_exhibit(request, username, slug)
    elif request.method == 'PUT':
        response = update_freemix(request, username, slug)
    elif request.method == 'DELETE':
        response = delete_freemix(request, username, slug)
    return response


def freemix_metadata(request, username, slug, jsonp=False):
    if request.method == 'GET':
        return get_freemix_metadata(request, username, slug, jsonp)
    else:
        return process_freemix(request, username, slug, jsonp)


def get_metadata(username, slug):
    user = get_user(username)
    freemix = get_object_or_404(models.Freemix, slug=slug, user=user)
    metadata = freemix.json
    profile = freemix.data_profile
    metadata["canvas"] = freemix.canvas.slug
    metadata["theme"] = freemix.theme.slug
    if freemix.title or freemix.description:
        metadata["text"] = metadata.get("text", {})
        metadata["text"]["title"] = getattr(freemix, "title", None)
        metadata["text"]["subtitle"] = getattr(freemix, "description", None)
    metadata["dataProfiles"] = {}
    metadata["dataProfiles"][profile.get_profile_url()] = profile.get_dict()
    return metadata


def get_freemix_metadata(request, username, slug, jsonp=False,
                         template_name="dataview/profile.js"):
    try:
        if jsonp:
            response = render_to_response(template_name, {
                    "json": json.dumps(get_metadata(username, slug)),
                }, context_instance=RequestContext(request))
            response['Content-Type'] = "application/javascript"
        else:
            response = HttpResponse(json.dumps(get_metadata(username, slug)))
            response['Content-Type'] = "application/json"
        return response

    except (IOError, os.error), why:
        msg = _("ERROR: Cannot read data view metadata.  Please tell a "
                  "systems administrator.\n")
        response = HttpResponseForbidden(msg)
    return response


def build_freemix(request, username, slug=None,
                  template_name="dataview/edit/build.html"):
    # Get a URL from the query string representing a data file's metadata.
    # Return the Builder, with URLs for the freemix/profile and
    # freemix/publish links.

    if request.method == 'GET':
        if validate_user(request.user, username):
            canvas = "three-column"
            if slug:
                user = models.get_user(username)
                freemix = get_object_or_404(models.Freemix,
                                            slug=slug,
                                            user=request.user)
                canvas = freemix.canvas.slug
                publishUrl = freemix.get_url_path()
                data_profile = None
            elif "data_profile" in request.GET:
                if "canvas" in request.GET:
                    canvas = request.GET["canvas"]
                publishUrl = reverse("freemix_root",
                                     kwargs={"username": username})
                data_profile = request.GET["data_profile"]
            else:
                return HttpResponseForbidden(_("Invalid Request"))

            return render_to_response(template_name, {
                "username": username,
                "slug": slug,
                "data_profile": data_profile,
                "publishurl": publishUrl,
                "canvas": canvas,
                "owner": username}, context_instance=RequestContext(request))
    return HttpResponseForbidden(_("Invalid Request"))
build_freemix = login_required(build_freemix)


def view_freemix(request, username, slug, template_name="dataview/view.html"):
    user = get_user(username)
    freemix = get_object_or_404(models.Freemix, user=user, slug=slug)

    metadata = get_metadata(username, slug)
    response = render_to_response(template_name, {
        "username": username,
        "slug": slug,
        "owner": username,
        "metadata": json.dumps(metadata),
        "canvas": freemix.canvas.slug,
        "theme": freemix.theme.slug,
        "freemix_title": freemix.title,
        "owner_user": user,
        "data_profile": freemix.data_profile},
                                  context_instance=RequestContext(request))
    return response


def forbidden_response(username):
    return HttpResponseForbidden(_("You do not seem to have the "
                                   "appropriate permissions to perform "
                                   "that request.  You must be logged in "
                                   "as %s\n") % username)


def url_response(url):
    return HttpResponse("<span><a href='%s'>%s</a></span>" % (url,
                                                              get_site_url(url)))


def create_exhibit(request, username, slug=None):
    if not validate_user(request.user, username):
        return forbidden_response(username)

    user = get_user(username)
    contents = json.loads(request.raw_post_data)
    freemix = models.create_exhibit(user, contents, slug)
    url = freemix.get_url_path()

    return url_response(url)
create_exhibit = login_required(create_exhibit)


def update_freemix(request, username, slug):
    if not validate_user(request.user, username):
        return forbidden_response(username)

    user = get_user(username)
    contents = json.loads(request.raw_post_data)

    freemix = get_object_or_404(models.Freemix, user=user, slug=slug)
    freemix.update_profile(contents)
    url = freemix.get_url_path()
    return url_response(url)
update_freemix = login_required(update_freemix)


def delete_freemix(request, username, slug):
    if not validate_user(request.user, username):
        return forbidden_response(username)

    user = models.get_user(username)
    freemix = get_object_or_404(models.Freemix, slug=slug, user=user)
    freemix_url = freemix.get_url_path()
    freemix.delete()
    request.user.message_set.create(message=_("The data view at %s "
                                              "has been deleted") % freemix_url)
    return HttpResponse(_("%(freemix_id)s deleted") % {'freemix_id': slug})
delete_freemix = login_required(delete_freemix)


def exhibit_history(request):
    return HttpResponse("<html><body></body></html>")


class EmbeddedExhibitView(View):
    """Generate the javascript necessary to embed an exhibit on an external site
    """
    # The
    template_name = "embed/show.js"

    # The template to display when an exhibit is not found
    not_found_template_name = "embed/none.js"

    def not_found_response(self, request, where):
        """Returns a trivial response when the desired exhibit is not found
        """
        response = render_to_response(self.not_found_template_name, {
            "where": where,
        }, context_instance=RequestContext(request))

        response['Content-Type'] = "application/javascript"
        return response

    def get(self, request, username, slug):
        where = request.GET.get('where', 'freemix-embed')
        try:
            exhibit = models.Freemix.objects.get(slug=slug,
                                                 user__username=username)
        except models.Freemix.DoesNotExist:
            return self.not_found_response(request, where)
        metadata = get_metadata(username, slug)

        canvas = exhibit.canvas
        canvas_html = render_to_string(canvas.location, {}).replace("\n", " ")
        profile = exhibit.data_profile
        data = profile.merge_data()
        response = render_to_response(self.template_name, {
            "data": json.dumps(data),
            "metadata": json.dumps(metadata),
            "where": where,
            "permalink": get_site_url(reverse("view-freemix",
                                              kwargs={'username': username,
                                                      'slug': slug})),
            "canvas": canvas_html}, context_instance=RequestContext(request))
        response['Content-Type'] = "application/javascript"
        return response
