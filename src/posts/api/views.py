from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


from posts.models import Post

from .pagination import StandardResultsPagination
from .serializers import PostModelSerializer

class LikeToggleAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        post_qs=Post.objects.filter(pk=pk)
        message="Not allowed"

        if request.user.is_authenticated:
            is_liked=Post.objects.like_toggle(request.user, post_qs.first())
            return Response({"liked": is_liked})
        return Response({"message": message}, status=400)

class RepostAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        post_qs=Post.objects.filter(pk=pk)
        message="Not allowed"
        if post_qs.exists() and post_qs.count()==1:
            if request.user.is_authenticated():
                new_post=Post.objects.repost(request.user, post_qs.first())
                if new_post is not None:
                    data=PostModelSerializer(post_qs.first()).data
                    return Response(data)
            message="Try after 24 hrs"
        return Response({"message": message}, status=400)

class PostDetailAPIView(generics.ListAPIView):
    queryset=Post.objects.all()
    serializer_class=PostModelSerializer
    permission_classes=[permissions.AllowAny]
    pagination_class=StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        post_id=self.kwargs.get("pk")
        qs=Post.objects.filter(pk=post_id)
        if qs.exists() and qs.count()==1:
            parent_obj=qs.first()
            qs1=parent_obj.get_children()
            qs=(qs|qs1).distinct().extra(select={"parent_id_null": "parent_id IS NULL"})
        return qs.order_by("-parent_id_null", "-pk")


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class=PostModelSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostListAPIView(generics.ListAPIView):
    serializer_class=PostModelSerializer
    pagination_class=StandardResultsPagination


    def get_serializer_context(self, *args, **kwargs):
        context=super(PostListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request']=self.request
        return context
    def get_queryset(self, *args, **kwargs):
        requested_user=self.kwargs.get("username")

        if requested_user:
            # qs1=Post.objects.filter(user__in=my_follow)
            qs=Post.objects.filter(user__username=requested_user).order_by("-pk")
            # qs=(qs1 | qs2).distinct().order_by("-pk")
            # print(self.request.GET)

        else:
            my_follow=self.request.user.profile.get_following()
            qs1=Post.objects.filter(user__in=my_follow)
            qs2=Post.objects.filter(user=self.request.user)
            qs=(qs1 | qs2).distinct().order_by("-pk")
            # print(self.request.GET)
        query=self.request.GET.get('q', None)
        if query is not None:
            qs=qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )
        return qs

class SearchPostAPIView(generics.ListAPIView):
    queryset=Post.objects.all().order_by("-pk")
    serializer_class=PostModelSerializer
    pagination_class=StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context=super(SearchPostAPIView, self).get_serializer_context(*args, **kwargs)
        context['request']=self.request
        return context

    def get_queryset(self, *args, **kwargs):
        qs=self.queryset
        query=self.request.GET.get('q', None)
        # if request.user.is_authenticated():
        if query is not None:
            qs=qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )
        return qs
