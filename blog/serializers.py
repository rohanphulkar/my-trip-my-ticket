from rest_framework import serializers
from .models import Post, Comment ,Tag
from accounts.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user  = UserSerializer(many=False,read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_comments')
    tags = TagSerializer(many=True,read_only=True)
    slug = serializers.SlugField(read_only=True)
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'created_at', 'updated_at', 'image', 'tags', 'comments', 'slug']

    def get_image_url(self, obj):
        if obj.image:
            return f"https://mytripmyticket.co.in/{obj.image.url.replace('/media/','')}"
        return None
    
    def get_comments(self,obj):
        comments = Comment.objects.filter(post=obj.id)
        serializer = CommentSerializer(comments,many=True)
        return serializer.data
    
