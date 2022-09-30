from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from .forms import NewPostForm, NewCommentForm
from .models import Post, Comment


class PostList(ListView):
    model = Post
    template_name = 'app/post_list.html'
    paginate_by = 10


class PostView(DetailView):
    model = Post
    template_name = 'app/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewCommentForm()
        context['comments'] = Comment.objects.select_related('post').filter(post=context['object'])
        return context

    def post(self, request, pk):
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(pk=pk)
            comment.author = request.user
            comment.save()
        return HttpResponseRedirect(f'{pk}')


class PostCreate(CreateView):
    model = Post
    template_name = 'app/post_create.html'
    form_class = NewPostForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        response = super(PostCreate, self).form_valid(form)
        return response


class PostEdit(UpdateView):
    model = Post
    template_name = 'app/post_edit.html'
    form_class = NewPostForm


class PostDelete(DeleteView):
    model = Post
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy('post_list')


def index_view(request):
    return render(request, 'index.html')


def logout_view(request):
    if request.method == 'GET':
        return render(request, 'logout.html')
    else:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
