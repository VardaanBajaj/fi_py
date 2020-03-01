from django.conf.urls import url
# from django.contrib import admin

from django.views.generic.base import RedirectView
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, RepostView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/"), name='list'),
    url(r'^search/$', PostListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'), # regex matches only digits
    url(r'^(?P<pk>\d+)/repost$', RepostView.as_view(), name='repost'), # regex matches only digits
    # class based views have pk built into them, hence they are very powerful than function based views
    url(r'^create/$', PostCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteView.as_view(), name='delete')
]
