from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    url(r'^$', views.ProductsListView.as_view(), name='index'),
    url(r'^buy-product/(?P<pk>\d+)/$', views.BuyProduct.as_view(), name="buy_product"),
    url(r'^update-product/(?P<pk>\d+)/$', views.UpdateProduct.as_view(), name="update_product"),
    url(r'^delete-product/(?P<primary_key>\d+)/$', views.deleteProduct, name="delete_product"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^cart/$',views.display_cart_items,name='my_cart')

]
