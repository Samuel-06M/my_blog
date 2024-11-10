from django import forms
from .models import BlogPost, Post

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content')
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']