from django.urls import path
from .views import PostView, PostList, PostCreate, PostDelete, PostEdit, index_view, logout_view

urlpatterns = [
    path('posts/create', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('posts/<int:pk>', PostView.as_view(), name='post_detail'),
    path('posts', PostList.as_view(), name='post_list'),
    path('', index_view, name='index'),
    path('logout', logout_view, name='logout')
]
