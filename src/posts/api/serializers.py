from django.utils.timesince import timesince
from rest_framework import serializers

from accounts.api.serializers import UserDisplaySerializer
from posts.models import Post

class ParentPostModelSerializer(serializers.ModelSerializer):
    user=UserDisplaySerializer(read_only=True)
    date_display=serializers.SerializerMethodField()
    timesince=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    did_like=serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields=[ 'id', 'user', 'content', 'timestamp', 'timesince', 'date_display', 'parent', 'likes', 'did_like', 'reply']

    def get_did_like(self, obj):
            request=self.context.get("request")
            try:
                user=request.user
                if user.is_authenticated():
                    if user in obj.liked.all():
                        return True
            except:
                pass
            return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_is_repost(self, obj):
        if obj.parent:
            return True
        return False


class PostModelSerializer(serializers.ModelSerializer):
    parent_id=serializers.CharField(write_only=True, required=False)
    user=UserDisplaySerializer(read_only=True)
    date_display=serializers.SerializerMethodField()
    timesince=serializers.SerializerMethodField()
    parent=ParentPostModelSerializer(read_only=True)
    likes=serializers.SerializerMethodField()
    did_like=serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields=['parent_id', 'user', 'content', 'timestamp', 'timesince', 'date_display', 'id', 'parent', 'likes', 'did_like', 'reply']

    def get_did_like(self, obj):
            request=self.context.get("request")
            try:
                user=request.user
                if user.is_authenticated():
                    if user in obj.liked.all():
                        return True
            except:
                pass
            return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_is_repost(self, obj):
        if obj.parent:
            return True
        return False
