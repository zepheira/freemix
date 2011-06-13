from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext_lazy as _
from freemix.utils.views import JSONResponse
from freemix.dataset import models
import json

# Data Source Transaction Views
from freemix.views import OwnerListView

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
        template_name="dataset/dataset_edit.html"


        response = render_to_response(template_name, {
            "transaction": self.transaction,
            "publishurl": reverse('dataset_publish', kwargs={'tx_id': self.transaction.tx_id}),
            "profileurl": reverse('datasource_transaction_result', kwargs={'tx_id': self.transaction.tx_id}),
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

class DatasetResourceView(DetailView):

    template_name="dataset/dataset_detail.html"

    def get_object(self, queryset=None):
        owner = self.kwargs["owner"]
        slug = self.kwargs["slug"]
        return get_object_or_404(models.Dataset, owner__username=owner, slug=slug)

    def delete(self, request, *args, **kwargs):
        ds = self.get_object()

        if request.user.has_perm("dataset.can_delete", ds):
            for exhibit in ds.exhibits.filter(~Q(user__username=self.kwargs["owner"])):
                exhibit.dataset = None
                exhibit.save()
            ds.delete()
            return HttpResponse(_("%(file_id)s deleted") % {'file_id': ds.get_absolute_url()})
        return HttpResponseForbidden()
