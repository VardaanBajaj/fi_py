from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect

from .models import Post
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .forms import PostModelForm
# Create your views here.
class RepostView(View):
    def get(self, request, pk, *args, **kwargs):
        post=get_object_or_404(Post, pk=pk)
        if request.user.is_authenticated():
            new_post=Post.objects.repost(request.user, post)
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(post.get_absolute_url())

class PostCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
    # queryset=Post.objects.all()
    form_class=PostModelForm
    template_name='posts/create_view.html'
    # success_url=reverse_lazy("post:list")
    # login_url="/admin/"

class PostUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset=Post.objects.all()
    form_class=PostModelForm
    template_name='posts/update_view.html'
    # success_url="/post/"

class PostDeleteView(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    model=Post #queryset=Post.objects.all()
    template_name='posts/delete_confirm.html'
    success_url=reverse_lazy("post:list")

class PostDetailView(DetailView):
    template_name="posts/detail_view.html"
    queryset=Post.objects.all()

class PostListView(LoginRequiredMixin, ListView):

    def get_queryset(self, *args, **kwargs):
        qs=Post.objects.all()
        # print(self.request.GET)
        query=self.request.GET.get('q', None)
        if query is not None:
            qs=qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context=super(PostListView, self).get_context_data(*args, **kwargs)
        context['create_form']=PostModelForm()
        context['create_url']=reverse_lazy("post:create")
        return context

    template_name="posts/list_view.html"



# def post_detail_view(request, id=1):
#     obj=Post.objects.get(id=id) #get from db
#     print(obj)
#     context={
#         "object": obj
#     }
#     return render(request, "posts/detail_view.html", context)
#
# def post_list_view(request):
#     queryset=Post.objects.all()
#     print(queryset)
#
#     for obj in queryset:
#         print(obj.content)
#     context={
#     "object_list": queryset
#     }
#     return render(request, "posts/list_view.html", context)
