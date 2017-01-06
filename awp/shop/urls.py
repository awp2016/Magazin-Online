from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    url(r'^$', views.ProductsListView.as_view(), name='index'),
    url(r'^buyProduct/(?P<pk>\d+)/$', views.BuyProduct.as_view(), name="buy_product"),
    url(r'^deleteProduct/(?P<primary_key>\d+)/$', views.deleteProduct, name="delete_product"),

]
