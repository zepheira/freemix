from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template.context import RequestContext
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from freemix.dataset import forms
from freemix.permissions import PermissionsRegistry
from freemix.dataset import models
import json

# Data Source Transaction Views
from freemix.views import OwnerListView, OwnerSlugPermissionMixin, JSONResponse

class DataSourceTransactionView(View):
    def redirect(self):
        status = self.transaction.status
        for key in models.TX_STATUS.keys():
            if status == models.TX_STATUS[key]:
                return getattr(self, key)()
        return HttpResponseServerError("Invalid transaction status for %s"%self.transaction.tx_id)

    def get(self, request, *args, **kwargs):
        tx_id = kwargs["tx_id"]
        user = request.user
        self.transaction = get_object_or_404(models.DataSourceTransaction, tx_id=tx_id)
        if not user.has_perm('datasourcetransaction.can_view', self.transaction):
            raise Http404

        return self.redirect()


class ProcessTransactionView(DataSourceTransactionView):

    def success(self):
        template_name="dataset/dataset_create.html"


        response = render_to_response(template_name, {
            "transaction": self.transaction,
            "dataurl": reverse('datasource_transaction_result', kwargs={'tx_id': self.transaction.tx_id}),
            "profileurl": reverse('datasource_transaction_result', kwargs={'tx_id': self.transaction.tx_id}),
            "cancel_url": reverse('upload_dataset', kwargs={})
        }, context_instance=RequestContext(self.request))

        return response

    def failure(self):
        response = render_to_response("dataset/transaction_failed.html", {
            "transaction": self.transaction
        }, context_instance = RequestContext(self.request))
        return response

    def cancelled(self):
        return  HttpResponseRedirect(reverse('dataset_upload'))

    def running(self):
        return HttpResponse("running")

    def pending(self):
        tx = self.transaction
        tx.run()
        return self.redirect()

    def scheduled(self):
        return self.pending()


class TransactionStatusView(DataSourceTransactionView):
    def success(self):
        return JSONResponse({
            "status": "success",
            "create_dataset_url": reverse('dataset_create',
                kwargs={'tx_id': self.transaction.tx_id}),
            "result_url": reverse('datasource_transaction_result',
                kwargs={'tx_id': self.transaction.tx_id})
        })


    def failure(self):
        return JSONResponse({
            "status": "failure",
            "result_url": reverse('datasource_transaction_result',
                kwargs={'tx_id': self.transaction.tx_id})
        })


    def cancelled(self):
        return JSONResponse({"status": "cancelled"})

    def running(self):
        return JSONResponse({"status": "running"})

    def pending(self):
        return JSONResponse({"status": "pending"})

    def scheduled(self):
        return JSONResponse({"status": "scheduled"})


class DataSourceTransactionResultView(View):

    def get(self, request, *args, **kwargs):
        tx_id = kwargs["tx_id"]

        tx = get_object_or_404(models.DataSourceTransaction, tx_id=tx_id)
        if not self.request.user.has_perm('datasourcetransaction.can_view', tx):
            raise Http404

        return JSONResponse(json.loads(tx.result))


#----------------------------------------------------------------------------------------------------------------------#
# Data Profile Views

class DataProfileJSONView(View):

    def get(self, request, *args, **kwargs):
        owner = kwargs["owner"]
        slug = kwargs["slug"]

        ds = get_object_or_404(models.Dataset, owner__username=owner, slug=slug)
        user = self.request.user

        if not user.has_perm("dataset.can_view", ds):
            raise Http404

        return JSONResponse(ds.profile)


class DataJSONView(View):
    def get(self, request, *args, **kwargs):
        owner = kwargs["owner"]
        slug = kwargs["slug"]

        ds = get_object_or_404(models.Dataset, owner__username=owner, slug=slug)
        user = self.request.user

        if not user.has_perm("dataset.can_view", ds):
            raise Http404

        return JSONResponse(ds.data)


dataset_list_by_owner = OwnerListView.as_view(template_name="dataset/dataset_list_by_owner.html",
                                               model=models.Dataset,
                                               permission = "dataset.can_view")

#----------------------------------------------------------------------------------------------------------------------#
# Dataset views

class DatasetView(OwnerSlugPermissionMixin, DetailView):

    model = models.Dataset
    object_perm="dataset.can_view"
    template_name= "dataset/dataset_summary.html"

    def get_context_data(self, **kwargs):
        context = super(DatasetView, self).get_context_data(**kwargs)
        context["can_edit"] = self.request.user.has_perm("dataset.can_edit", self.get_object())
        context["can_delete"] = self.request.user.has_perm("dataset.can_delete", self.get_object())
        context["can_build_view"] = self.request.user.is_authenticated()

        return context

class DatasetSummaryView(DatasetView):
    template_name="dataset/dataset_summary.html"

    def delete(self, request, *args, **kwargs):
        ds = self.get_object()

        if request.user.has_perm("dataset.can_delete", ds):
            for exhibit in ds.exhibits.filter(~Q(user__username=self.kwargs["owner"])):
                exhibit.dataset = None
                exhibit.save()
            ds.delete()
            return HttpResponse(_("%(file_id)s deleted") % {'file_id': ds.get_absolute_url()})
        return HttpResponseForbidden()


class DatasetDetailView(DatasetView):
    template_name="dataset/dataset_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        filter = PermissionsRegistry.get_filter("exhibit.can_view", self.request.user)
        context["exhibits"] = self.object.exhibits.filter(filter)
        return context


class DatasetCreateFormView(CreateView):
    form_class = forms.CreateDatasetForm
    template_name = "dataset/create/dataset_metadata_form.html"

    def get_success_url(self):
        owner = getattr(self.object.owner, "username", None)
        return reverse('dataset_create_success',
                       kwargs={"owner": owner,
                               "slug": self.object.slug})

    def get_context_data(self, **kwargs):
        ctx = super(DatasetCreateFormView, self).get_context_data(**kwargs)
        ctx["tx_id"] = self.kwargs["tx_id"]
        return ctx

    def get_form_kwargs(self):
        kwargs = super(DatasetCreateFormView, self).get_form_kwargs()
        kwargs["owner"] = self.request.user
        source = get_object_or_404(models.DataSourceTransaction, tx_id=self.kwargs["tx_id"]).source
        kwargs["datasource"] = source
        return kwargs

    def get_initial(self):
        initial = dict(super(DatasetCreateFormView, self).get_initial())
        source = get_object_or_404(models.DataSourceTransaction, tx_id=self.kwargs["tx_id"]).source
        if source:
            source = source.get_concrete()
        if hasattr(source, "title"):
            initial["title"] = getattr(source, "title")
        return initial

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class DatasetDetailEditView(OwnerSlugPermissionMixin, UpdateView):
    form_class = forms.EditDatasetDetailForm
    object_perm="dataset.can_edit"
    model = models.Dataset
    template_name = "dataset/edit/dataset_metadata_form.html"

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, "dataset/detail/dataset_metadata.html", {
                "can_edit": True,
                "object": self.object,
                "is_saved": True
            })

class DatasetProfileEditView(OwnerSlugPermissionMixin, View):
    object_perm="dataset.can_edit"
    template_name="dataset/dataset_update.html"

    def get(self, request, *args, **kwargs):
        dataset = self.get_object()

        response = render(request, self.template_name, {
            "dataset": dataset,
            "dataurl": reverse('dataset_data_json', kwargs={'owner': dataset.owner.username,
                                                                  'slug': dataset.slug}),
            "profileurl": reverse('dataset_profile_json', kwargs={'owner': dataset.owner.username,
                                                                  'slug': dataset.slug}),
            "cancel_url": reverse('dataset_summary', kwargs={'owner': dataset.owner.username,
                                                                  'slug': dataset.slug}),

        })

        return response

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.raw_post_data)
            if not data.has_key("properties") or not data.has_key("items"):
                return HttpResponseServerError("Invalid Request")
            ds = self.get_object()
            ds.profile = {"properties": data["properties"]}
            ds.data = {"items": data["items"]}
            ds.save()
            return render(request, "dataset/edit/success.html", {
                "owner": ds.owner.username,
                "slug": ds.slug
            })

        except Exception, ex:
            return HttpResponseServerError("Invalid Request")


    def get_queryset(self):
        return models.Dataset.objects.all()
