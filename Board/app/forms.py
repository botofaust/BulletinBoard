from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Post, Comment


class NewPostForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'category']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
