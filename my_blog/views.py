from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .models import Post
from .forms import BlogPostForm, PostForm
from django.contrib.auth.decorators import login_required



def home(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'blog_posts': blog_posts})

def post_detail(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'post_detail.html', {'blog_post':blog_post})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            
            return redirect('home')
    else:
            form = BlogPostForm()
            
    return render(request, 'add_post.html', {'form': form})

def edit_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
            form = BlogPostForm(instance=blog_post)
    return render(request, 'edit_post.html', {'form': form, 'blog_post': blog_post})
        