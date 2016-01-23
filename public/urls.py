from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from public import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^terms_conditions/$', views.terms_conditions, name='terms_conditions'),
    url(r'^site_map/$', views.site_map, name='site_map'),
    url(r'^myaccount/$', views.myaccount, name='myaccount'),
    url(r'^edit_personal_details/$', views.edit_personal_details, name='edit_personal_details'),
    url(r'^register$', views.register, name='register'),
    url(r'^accounts/confirm/(?P<activation_key>\w+)/', views.register_confirm, name='reister_confirm'),
    url(r'^reply_to_notification/$', views.reply_to_notification, name = "reply_to_notification"),
    url(r'^email-sent/', views.validation_sent, name='validation_sent'),
    url(r'^notify/$', views.notify, name='notify'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', views.ajax_auth, name='ajax-auth'),
    url(r'^email/$', views.require_email, name='require_email'),
    url(r'^item_registration/$', views.item_registration, name='item_registration'),
	url(r'^item_pre_registration/$', views.item_pre_registration, name='item_pre_registration'),
    url(r'^username_check/$', views.username_check, name='username_check'),
    url(r'^email_check/$', views.email_check, name='email_check'),
)
