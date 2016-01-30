from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from ibfAPI import views

urlpatterns = patterns('',
    url(r'^reject_match/$', views.reject_match, name='reject_match'),
    url(r'^reply_to_notification/$', views.reply_to_notification, name = "reply_to_notification"),
    url(r'^respond_to_repatriation/$', views.respond_to_repatriation, name = "respond_to_repatriation"),
    url(r'^notify/$', views.notify, name='notify'),
    url(r'^repatriate_item/$', views.repatriate_item, name='repatriate_item'),
    url(r'^notifications_job/$', views.notifications_job, name='notifications_job'),
	url(r'^item_pre_registration/$', views.item_pre_registration, name='item_pre_registration'),
    url(r'^username_check/$', views.username_check, name='username_check'),
    url(r'^email_check/$', views.email_check, name='email_check'),
)
