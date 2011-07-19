from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext_lazy as _

from django.http import *
from django.views.generic.base import View
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import  reverse

from . import models
from freemix.canvas.models import Canvas
from freemix.dataset.models import Dataset
from freemix.permissions import PermissionsRegistry
from freemix.utils import get_site_url

from freemix.utils import get_user
from freemix.utils.views import LegacyListView, JSONResponse
import json
import uuid


def validate_user(user, username=None):
    if username:
        return user.is_authenticated() and user.username == username
    else:
        return user.is_authenticated()


class DataviewsListView(LegacyListView):
    template = "exhibit/list/dataview_list_by_user.html"

    def get_queryset(self, request, username, other_user):
        perm_filter = PermissionsRegistry.get_filter("exhibit.can_view", request.user)
        return models.Freemix.objects.filter(user=get_user(username)).filter(perm_filter)

    def extra_context(self, request, username):
        return {"other_user": get_user(username)}
dataviews_by_user = DataviewsListView()


class ExhibitsByDatasetListView(LegacyListView):
    template = "exhibit/list/dataview_list_by_dataset.html"

    def get_queryset(self, request, *args, **kwargs):
        perm_filter = PermissionsRegistry.get_filter("exhibit.can_view", request.user)

        return models.Freemix.objects.filter(dataset=kwargs["dataset"]).filter(perm_filter)

    def extra_context(self, request, *args, **kwargs):
        return {"dataset": get_object_or_404(Dataset, slug=kwargs["slug"],
                                             owner__username=kwargs["owner"])}
exhibits_by_dataset = ExhibitsByDatasetListView()


class StockExhibitProfileJSONView(View):
    """Generate the default profile description of an exhibit for a particular dataset and canvas
    """
    def get(self, request, *args, **kwargs):
        owner = kwargs["owner"]
        slug = kwargs["slug"]
        canvas = request.GET.get("canvas", "three-column")

        ds = get_object_or_404(models.Dataset, owner__username=owner, slug=slug)
        user = self.request.user

        if not user.has_perm("dataset.can_view", ds):
            raise Http404

        return JSONResponse({
            "theme": "smoothness",
            "properties": [],
            "facets": {},
            "views": {
                "views": [{
                    "id": str(uuid.uuid4()),
                    "type": "list",
                    "name": "List"}]},
            "text": {"title": ds.title},
            "canvas": canvas})


def process_freemixes(request, username):
    if request.method == 'GET':
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
                response = get_exhibit_profile(request, username, slug, jsonp)
            else:
                response = HttpResponseNotFound()

        else:
            response = exhibit_display(request, username, slug)
    elif request.method == 'POST':
        response = create_exhibit(request, username, slug)
    elif request.method == 'PUT':
        response = update_exhibit(request, username, slug)
    elif request.method == 'DELETE':
        response = delete_exhibit(request, username, slug)
    return response


def exhibit_profile(request, username, slug, jsonp=False):
    if request.method == 'GET':
        return get_exhibit_profile(request, username, slug, jsonp)
    else:
        return process_freemix(request, username, slug, jsonp)


def get_metadata(username, slug):
    user = get_user(username)
    exhibit = get_object_or_404(models.Freemix, slug=slug, user=user)
    metadata = exhibit.json
    metadata["canvas"] = exhibit.canvas.slug
    metadata["theme"] = exhibit.theme.slug
    if exhibit.title or exhibit.description:
        metadata["text"] = metadata.get("text", {})
        metadata["text"]["title"] = getattr(exhibit, "title", None)
        metadata["text"]["subtitle"] = getattr(exhibit, "description", None)
    return metadata


def get_exhibit_profile(request, username, slug, jsonp=False,
                         template_name="exhibit/profile.js"):
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


class NewExhibitEditorView(View):

    template_name="exhibit/exhibit_edit.html"

    def setup(self):
        self.dataset_args = {"owner": self.kwargs["owner"], "slug": self.kwargs["slug"]}
        self.dataset = get_object_or_404(Dataset,owner__username=self.kwargs["owner"], slug=self.kwargs["slug"])

    def get_profile_url(self):
        return reverse("exhibit_profile_template", kwargs=self.dataset_args)

    def get_dataset_profile_url(self):
        return reverse("dataset_profile_json", kwargs=self.dataset_args)

    def get_data_url(self):
        return reverse("dataset_data_json", kwargs=self.dataset_args)

    def get_canvas(self):
        return self.request.GET.get("canvas", "three-column")

    def check_permissions(self):
        return self.request.user.has_perm("dataset.can_view", self.dataset)

    def get(self, request, *args, **kwargs):
        self.setup()

        if not self.check_permissions():
            raise Http404()

        return render(request, self.template_name, {
            "exhibit_profile_url": self.get_profile_url(),
            "dataset_profile_url": self.get_dataset_profile_url(),
            "data_url": self.get_data_url(),
            "canvas": self.get_canvas(),
            "owner": request.user.username
        })


    def post(self, request, *args, **kwargs):
        self.setup()
        user = request.user

        if not self.check_permissions():
            raise Http404()

        contents = json.loads(self.request.raw_post_data)
        exhibit = models.create_exhibit(user, self.dataset, contents)
        return url_response(exhibit.get_absolute_url())


class ExhibitEditorView(View):
    template_name="exhibit/exhibit_edit.html"

    def setup(self):
        self.exhibit = get_object_or_404(models.Freemix, user__username=self.kwargs["username"],
                                         slug=self.kwargs["slug"])
        self.dataset = self.exhibit.dataset
        self.dataset_args = {"owner": self.dataset.owner.username, "slug": self.dataset.slug}

    def get_profile_url(self):
        return reverse("exhibit_profile", kwargs={"username": self.kwargs["username"],
                                                       "slug": self.kwargs["slug"]})
    def get_dataset_profile_url(self):
        return reverse("dataset_profile_json", kwargs=self.dataset_args)

    def get_data_url(self):
        return reverse("dataset_data_json", kwargs=self.dataset_args)

    def get_canvas(self):
        return self.exhibit.canvas.slug

    def check_permissions(self):
        return self.request.user.has_perm("exhibit.can_edit", self.exhibit)

    def get(self, request, *args, **kwargs):
        self.setup()

        if not self.check_permissions():
            raise Http404()

        return render(request, self.template_name, {
            "exhibit_profile_url": self.get_profile_url(),
            "dataset_profile_url": self.get_dataset_profile_url(),
            "data_url": self.get_data_url(),
            "canvas": self.get_canvas(),
            "owner": request.user.username
        })


    def post(self, request, *args, **kwargs):
        self.setup()
        user = request.user

        if not self.check_permissions():
            raise Http404()

        contents = json.loads(self.request.raw_post_data)
        self.exhibit.update_profile(contents)
        url = self.exhibit.get_absolute_url()
        return url_response(self.exhibit.get_absolute_url())

def exhibit_display(request, username, slug, template_name="exhibit/exhibit_display.html"):
    user = get_user(username)
    exhibit = get_object_or_404(models.Freemix, user=user, slug=slug)
    if not request.user.has_perm("exhibit.can_view", exhibit):
        return forbidden_response(username)

    if not exhibit.dataset_available(request.user):
        return forbidden_response(username)

    metadata = get_metadata(username, slug)
    response = render_to_response(template_name, {
        "username": username,
        "slug": slug,
        "owner": username,
        "exhibit": exhibit,
        "metadata": json.dumps(metadata),
        "canvas": exhibit.canvas.slug,
        "theme": exhibit.theme.slug,
        "freemix_title": exhibit.title,
        "owner_user": user,
        "data_profile": exhibit.dataset},
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
    exhibit = models.create_exhibit(user, contents, slug)
    if not exhibit.dataset_available(request.user):
        return forbidden_response(username)
    url = exhibit.get_absolute_url()

    return url_response(url)
create_exhibit = login_required(create_exhibit)


def update_exhibit(request, username, slug):

    exhibit = get_object_or_404(models.Freemix, user__username=username, slug=slug)
    if not request.user.has_perm("exhibit.can_edit", exhibit):
        return forbidden_response(username)
    contents = json.loads(request.raw_post_data)
    exhibit.update_profile(contents)
    url = exhibit.get_absolute_url()
    return url_response(url)
update_exhibit = login_required(update_exhibit)

def delete_exhibit(request, username, slug):

    exhibit = get_object_or_404(models.Freemix, slug=slug, user__username=username)


    exhibit_url =  exhibit.get_absolute_url()
    exhibit.delete()
    request.user.message_set.create(message=_("The data view at %s "
                                          "has been deleted") % exhibit_url)
    return HttpResponse(_("%(slug)s deleted") % {'slug': slug})
delete_exhibit = login_required(delete_exhibit)



def exhibit_history(request):
    return HttpResponse("<html><body></body></html>")


class EmbeddedExhibitView(View):
    """Generate the javascript necessary to embed an exhibit on an external site
    """
    # The
    template_name = "exhibit/embed/show.js"

    # The template to display when an exhibit is not found
    not_found_template_name = "exhibit/embed/none.js"

    no_data_template_name = "exhibit/embed/no_dataset.js"

    def not_found_response(self, request, where):
        """Returns a trivial response when the desired exhibit is not found
        """
        response = render_to_response(self.not_found_template_name, {
            "where": where,
        }, context_instance=RequestContext(request))

        response['Content-Type'] = "application/javascript"
        return response

    def no_dataset_response(self, request, where):
        """Returns a trivial response when the desired dataset is not found
        """
        response = render_to_response(self.no_data_template_name, {
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

        if not exhibit.dataset_available(self.request.user):
            return self.no_dataset_response(request, where)
        
        metadata = get_metadata(username, slug)

        canvas = exhibit.canvas
        canvas_html = render_to_string(canvas.location, {}).replace("\n", " ")
        profile = exhibit.dataset
        data = profile.data
        response = render_to_response(self.template_name, {
            "data": json.dumps(data),
            "metadata": json.dumps(metadata),
            "data_profile": json.dumps(profile.profile),
            "where": where,
            "permalink": get_site_url(reverse("exhibit_detail",
                                              kwargs={'username': username,
                                                      'slug': slug})),
            "canvas": canvas_html}, context_instance=RequestContext(request))
        response['Content-Type'] = "application/javascript"
        return response

class CanvasChooserView(View):
    template_name = "canvas/chooser.html"

    def get(self, request, *args, **kwargs):
        obj_list = Canvas.objects.filter(enabled=True)
        ds = get_object_or_404(Dataset, owner__username = kwargs["owner"],slug = kwargs["slug"])
        return render(request, self.template_name, {
            "canvases": obj_list,
            "base_url": reverse("exhibit_create_editor", kwargs={"owner": kwargs["owner"],
                                                                 "slug":kwargs["slug"]})
        })

