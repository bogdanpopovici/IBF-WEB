from django.conf.urls import patterns, url, include
from paypalapp import views

urlpatterns = patterns('',
    url(r'^payment/$', views.pay_premium, name='payment'),
    url(r'^paypal-ipn-standard-service/', include('paypal.standard.ipn.urls')),
)
