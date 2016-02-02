from django.conf.urls import patterns, url, include
from android_module import views

urlpatterns = patterns('',
    url(r'^upload_item/$', views.upload_item, name='upload_item'),
    url(r'^login_user/$', views.login_user, name='login_user'),
)
