from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from staticpages import views

urlpatterns = patterns('',
    url(r'^contact_page/$', views.contact_page, name='contact_page'),
    url(r'^accessibility_support/$', views.accessibility_support, name='accessibility_support'),
    url(r'^terms_conditions/$', views.terms_conditions, name='terms_conditions'),
    url(r'^site_map/$', views.site_map, name='site_map'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^our_strategy/$', views.our_strategy, name='our_strategy'),
    url(r'^why_our_services/$', views.why_our_services, name='why_our_services'),
    url(r'^register_tutorial/$', views.register_tutorial, name='register_tutorial'),
    url(r'^search_tutorial/$', views.search_tutorial, name='search_tutorial'),
    url(r'^return_item/$', views.return_item, name='return_item'),
    url(r'^common_tips/$', views.common_tips, name='common_tips'),
)
