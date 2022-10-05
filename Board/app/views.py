from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect

from .filters import PostFilter
from .forms import NewPostForm, NewCommentForm
from .models import Post, Comment, Category
from .tasks import sent_email_about_accept


class PostList(ListView):
    model = Post
    template_name = 'app/post_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('app.create_post', )
    model = Post
    template_name = 'app/post_create.html'
    form_class = NewPostForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        response = super(PostCreate, self).form_valid(form)
        return response


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_post', )
    model = Post
    template_name = 'app/post_edit.html'
    form_class = NewPostForm


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('app.delete_post', )
    model = Post
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'app/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def index_view(request):
    return render(request, 'index.html')


@login_required
def accept_comment(request, pk):
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('index'))
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
        # тут бы надо в secure написать
    else:
        comment.accepted = True
        comment.save()
        sent_email_about_accept.delay(comment.pk)
    return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': comment.post.pk}))


@login_required
def delete_comment(request, pk):
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('index'))
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
        # тут бы надо в secure написать
    else:
        post_pk = comment.post.pk
        comment.delete()
    return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post_pk}))


@login_required
def category_subscribe(request, pk):
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('index'))
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
        # тут бы надо в secure написать
    else:
        category.subscribe(request.user)
    return HttpResponseRedirect(reverse('category_list'))


@login_required
def category_unsubscribe(request, pk):
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('index'))
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
        # тут бы надо в secure написать
    else:
        category.unsubscribe(request.user)
    return HttpResponseRedirect(reverse('category_list'))
