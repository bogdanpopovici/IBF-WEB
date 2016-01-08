#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from core import settings


urlpatterns = [
	url(r'^', include('public.urls', namespace="public")),
	url(r'^android_module/', include('android_module.urls', namespace="android_module")),
	url(r'^paypal/', include('paypalapp.urls', namespace="paypal")),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', auth_views.login, name='login' ),
	url(r'^logout/$', auth_views.logout_then_login, name='logout' ),
	url(r'^password_change/$', auth_views.password_change, name='password_change'),
	url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
	url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'public/password_reset_form.html'}, name='password_reset'),
	url(r'^password_reset/done/$', auth_views.password_reset_done,{'template_name': 'public/password_reset_done.html'}, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm,{'template_name': 'public/password_reset_confirm.html'}, name='password_reset_confirm'),
	url(r'^reset/done/$', auth_views.password_reset_complete,{'template_name': 'public/password_reset_complete.html'}, name='password_reset_complete'),
	url(r'', include('social.apps.django_app.urls', namespace='social')),
	url(r'^search/', include('search_engine.urls', namespace="search")),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
