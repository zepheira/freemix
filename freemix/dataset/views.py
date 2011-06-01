from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from freemix.utils.views import JSONResponse
from freemix.dataset.models import DataSourceTransaction, TX_STATUS
import json

class DataSourceTransactionView(View):
    def redirect(self):
        status = self.transaction.status
        for key in TX_STATUS.keys():
            if status == TX_STATUS[key]:
                return getattr(self, key)()
        return HttpResponseServerError("Invalid transaction status for %s"%self.transaction.tx_id)

    def get(self, request, *args, **kwargs):
        tx_id = kwargs["tx_id"]
        user = request.user
        self.transaction = get_object_or_404(DataSourceTransaction, tx_id=tx_id)
        if not user.has_perm('datasourcetransaction.can_view', self.transaction):
            raise Http404

        return self.redirect()


class ProcessTransactionView(DataSourceTransactionView):

    def success(self):
        template_name="dataset/edit/build.html"


        response = render_to_response(template_name, {
            "transaction": self.transaction,
            "publishurl": reverse('dataset_publish', kwargs={'tx_id': self.transaction.tx_id}),
            "profileurl": reverse('datasource_transaction_result', kwargs={'tx_id': self.transaction.tx_id}),
        }, context_instance=RequestContext(self.request))

        return response

    def failure(self):
        return HttpResponseRedirect(reverse('datasource_transaction_result',
                kwargs={'tx_id': self.transaction.tx_id}))

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

        tx = get_object_or_404(DataSourceTransaction, tx_id=tx_id)
        if not self.request.user.has_perm('datasourcetransaction.can_view', tx):
            raise Http404

        return JSONResponse(json.loads(tx.result))