from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'shop'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.signin, name='login'),
    url(r'^logout/$', views.signout, name="logout"),
    url(r'^seller/$', views.seller_view_item, name='seller-view-item'),
    url(r'^seller/add-item/$', views.seller_add_item, name='seller-add-item'),
    url(r'^customer/(?P<slug>.*)/$', views.order_details, name='order-details'),
    url(r'^customer/$', views.customer_order, name='customer-order'),
]
