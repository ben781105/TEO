from django.urls import path
from .views import postView, content,postsbytags,comments,post_home


urlpatterns = [
path('post',postView, name='post'),
path( 'homepost',post_home,name='homepost'),
path('content/<slug:slug>/',content,name='content'),
path('postsbytags/tag/<str:tag>/',postsbytags,name='postsbytags'),
path('comments/',comments,name='comments'),
]