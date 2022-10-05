from django.urls import path
from .views import PostView, PostList, PostCreate, PostDelete, PostEdit, index_view, accept_comment, delete_comment, \
    CategoryList, category_subscribe, category_unsubscribe

urlpatterns = [
    path('posts/create', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('posts/<int:pk>', PostView.as_view(), name='post_detail'),
    path('posts', PostList.as_view(), name='post_list'),
    path('categories', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', category_subscribe, name='category_subscribe'),
    path('categories/<int:pk>/unsubscribe', category_unsubscribe, name='category_unsubscribe'),
    path('', index_view, name='index'),
    path('comments/<int:pk>/accept', accept_comment, name='accept_comment'),
    path('comments/<int:pk>/delete', delete_comment, name='delete_comment'),
]
