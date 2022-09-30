from django.urls import path
from .views import PostView, index_view, PostList

urlpatterns = [
    path('posts/<int:pk>', PostView.as_view()),
    path('posts', PostList.as_view(), name='post_list'),
    path('', index_view)
]
