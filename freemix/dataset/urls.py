from django.conf.urls.defaults import url, patterns
from freemix.dataset.views import  ProcessTransactionView, DataSourceTransactionResultView


urlpatterns = patterns('',
    url(r'^tx/(?P<tx_id>[a-f0-9-]+)/$', ProcessTransactionView.as_view(), name='datasource_transaction'),
    url(r'^tx/(?P<tx_id>[a-f0-9-]+)/result.json$', DataSourceTransactionResultView.as_view(), name='datasource_transaction_result'),
    url(r'^tx/(?P<tx_id>[a-f0-9-]+)/publish$', DataSourceTransactionResultView.as_view(), name='dataset_publish'),

)