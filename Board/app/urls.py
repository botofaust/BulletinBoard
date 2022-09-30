from django.urls import path
from .views import PostView, index_view, PostList, PostCreate

urlpatterns = [
    path('posts/create', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>', PostView.as_view()),
    path('posts', PostList.as_view(), name='post_list'),
    path('', index_view, name='index'),
]
