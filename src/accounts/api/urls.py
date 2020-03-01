from django.conf.urls import url
# from django.contrib import admin

from django.views.generic.base import RedirectView
from posts.api.views import PostListAPIView

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/post/$', PostListAPIView.as_view(), name='list'),

]
