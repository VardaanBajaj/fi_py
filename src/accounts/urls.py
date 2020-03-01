from django.conf.urls import url
from .views import UserDetailView, UserFollowView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # url(r'^post/', include('posts.urls', namespace='post')),
    # url(r'^api/post/', include('posts.api.urls', namespace='post-api')),
]
