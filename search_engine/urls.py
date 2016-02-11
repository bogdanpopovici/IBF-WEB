from django.conf.urls import patterns, url, include
from search_engine.views import CustomSearchView

urlpatterns = patterns('',
    url(r'^$', CustomSearchView.as_view(), name='custom_search'),
)
