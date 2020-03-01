"""fi_py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from posts.api.views import SearchPostAPIView
from posts.views import PostListView
from .views import home, SearchView
from hashtags.api.views import TagPostAPIView

from accounts.views import UserRegisterView
from hashtags.views import HashTagView

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', PostListView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^tags/(?P<hashtag>.*)/$', HashTagView.as_view(), name="hashtag"),
    url(r'^post/', include('posts.urls', namespace='post')),
    url(r'^api/post/', include('posts.api.urls', namespace='post-api')),
    url(r'^api/search/', SearchPostAPIView.as_view(), name='search-api'),
    url(r'^api/tags/(?P<hashtag>.*)', TagPostAPIView.as_view(), name='tag-post-api'),

    url(r'^register/$', UserRegisterView.as_view(), name='register'),
    url(r'^', include('accounts.urls', namespace='profiles')),
    url(r'^api/', include('accounts.api.urls', namespace='profiles-api')),
]

if settings.DEBUG:
    urlpatterns+=(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
