from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import  Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from freemix.dataset.forms import CreateDatasetForm
from . import models
from freemix.dataset.permissions import owner_filter

class DatasetCreateView(CreateView):
    form_class = CreateDatasetForm
    template_name = "dataset/dataset_create.html"
    
    def get_user(self):
        return self.request.user

    def get_form_kwargs(self, **kwargs):
        kwargs = super(DatasetCreateView, self).get_form_kwargs(**kwargs)
        kwargs['owner'] = self.get_user()
        return kwargs

    
class OwnerListView(ListView):

    def get_queryset(self):
        owner = get_object_or_404(User, username=self.kwargs.get("owner"))
        list = self.model.objects.filter(owner=owner)
        if hasattr(self, "query_filter"):
            list = list.filter(self.query_filter(self.request.user))
        return list
    
    def get_context_data(self, **kwargs):
        kwargs["owner"] = get_object_or_404(User,
                                            username=self.kwargs.get("owner"))
        return kwargs

    
class DatasetListView(OwnerListView):
    model = models.DataSet

    def query_filter(self, user):
        if user.is_authenticated():
            return Q(published=True)|owner_filter(user)
        return Q(published=True)


class OwnerSlugDetailView(DetailView):

    def filter_by_perm(self, obj):
        if hasattr(self, "object_perm") and \
            not self.request.user.has_perm(self.object_perm, obj):
                raise Http404
        return obj


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                 owner__username=self.kwargs.get("owner"),
                                 slug=self.kwargs.get("slug"))
        return self.filter_by_perm(obj)


class DatasetDetailView(OwnerSlugDetailView):
    model = models.DataSet
    context_object_name="dataset"
    object_perm = "dataset.can_view"
    