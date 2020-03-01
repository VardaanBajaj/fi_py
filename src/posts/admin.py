from django.contrib import admin

# Register your models here.
from .models import Post
from .forms import PostModelForm

# admin.site.register(Post)

class PostModelAdmin(admin.ModelAdmin):
    # form=PostModelForm
    class Meta:
        model=Post


admin.site.register(Post, PostModelAdmin)
