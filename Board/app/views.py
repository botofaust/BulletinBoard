from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import NewPostForm
from .models import Post, Category, Comment


class PostList(ListView):
    model = Post
    template_name = 'app/post_list.html'
    paginate_by = 10


class PostView(DetailView):
    model = Post
    template_name = 'app/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.select_related('post').filter(post=context['object'])
        return context


class PostCreate(CreateView):
    model = Post
    template_name = 'app/post_create.html'
    form_class = NewPostForm


class PostEdit(UpdateView):
    model = Post
    template_name = 'app/post_edit.html'
    form_class = NewPostForm


class PostDelete(DeleteView):
    model = Post
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy('post_list')


def index_view(request):
    Category.standard_values()
    return render(request, 'index.html')
