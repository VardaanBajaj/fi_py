from django.conf.urls import url

from django.views.generic.base import RedirectView
from .views import PostListAPIView, PostCreateAPIView, RepostAPIView, LikeToggleAPIView, PostDetailAPIView

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url="/"), name='list'),
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/repost$', RepostAPIView.as_view(), name='repost'), # regex matches only digits
    url(r'^(?P<pk>\d+)/like$', LikeToggleAPIView.as_view(), name='like'),
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'), # regex matches only digits
    # # class based views have pk built into them, hence they are very powerful than function based views
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    # url(r'^(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name='update'),
    # url(r'^(?P<pk>\d+)/delete/$', PostDeleteView.as_view(), name='delete')
]
