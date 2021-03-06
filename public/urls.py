from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from public import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^myaccount/$', views.myaccount, name='myaccount'),
    url(r'^myaccount/(?P<tab>\w+)/$', views.myaccount, name='myaccount'),
    url(r'^item_registration_confirmation/(?P<pk>\w+)/$', views.item_registration_confirmation, name='item_registration_confirmation'),
    url(r'^edit_personal_details/$', views.edit_personal_details, name='edit_personal_details'),
    url(r'^register$', views.register, name='register'),
    url(r'^accounts/confirm/(?P<activation_key>\w+)/', views.register_confirm, name='reister_confirm'),
    url(r'^email-sent/', views.validation_sent, name='validation_sent'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', views.ajax_auth, name='ajax-auth'),
    url(r'^email/$', views.require_email, name='require_email'),
    url(r'^item_registration/$', views.item_registration, name='item_registration'),
)
