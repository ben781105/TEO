from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Post
from .serializers import PostSerializer,ContentSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def postView(request):
    category =request.query_params.get('category', None)
    if category:
        posts = Post.objects.filter(category=category)
    else:    
        posts = Post.objects.all()
    
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def post_home(request):
    posts = Post.objects.filter(is_home = True)
    serializer = PostSerializer(posts,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def content(request,slug):
    posts = Post.objects.get(slug=slug)
    serializer = ContentSerializer(posts)
    return Response(serializer.data)

@api_view(['GET'])
def postsbytags(request,tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    serializer = ContentSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def comments(request):
   
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Comment submitted successfully.',
            'comment': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

