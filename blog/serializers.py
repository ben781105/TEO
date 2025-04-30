from rest_framework import serializers
from .models import Post,Comment
from taggit.serializers import (TagListSerializerField, TaggitSerializer)

class PostSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()    
    class Meta:
        model = Post
        fields = ['id','image','excerpt','slug','formatted_date','content','author','category','title','created_at','modified_at']
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime('%B %d, %Y') 

class ContentSerializer(TaggitSerializer,serializers.ModelSerializer):
    related_posts = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = ['id','image','excerpt','slug','formatted_date','content','author','category','title','created_at','modified_at','related_posts','tags']

    def get_related_posts(self,post):
        related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)
        serializer = PostSerializer(related_posts,many=True)
        
        return serializer.data
    def get_formatted_date(self, obj):
        return obj.created_at.strftime('%B %d, %Y') 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','post','name','email', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']
