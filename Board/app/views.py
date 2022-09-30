from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from .models import Post, Category, Comment


class PostList(ListView):
    model = Post
    template_name = 'app/posts.html'
    paginate_by = 10


class PostView(DetailView):
    model = Post
    template_name = 'app/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.select_related('post').filter(post=context['object'])
        return context


class PostCreate(CreateView):
    model = Post
    template_name = "app/create_post.html"

def index_view(request):
    Category.standard_values()
    return render(request, 'index.html')
