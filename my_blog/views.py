from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from .models import Post

def home(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'blog_posts': blog_posts})

def post_detail(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'post_detail.html', {'blog_post':blog_post})