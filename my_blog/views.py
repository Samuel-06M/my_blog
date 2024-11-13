from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Post, Comment
from django.shortcuts import redirect
from .forms import BlogPostForm, PostForm, LoginForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
                messages.error(request, 'Please correct the error below.')
                
            
    else:
            form = AuthenticationForm()
            
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')   

def user_signup(request):
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_login')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})
            
    
def home(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'blog_posts': blog_posts})

def post_detail(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    comments = blog_post.comments.all()
    comment_form = CommentForm()
    
    if request.method =='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = blog_post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', post_id=blog_post.id)

    return render(request, 'post_detail.html', {
     'blog_post':blog_post, 
     'comments': comments, 
     'comment_form': comment_form
     })

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
    
    if blog_post.author != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
            form = BlogPostForm(instance=blog_post)
    return render(request, 'edit_post.html', {'form': form, 'blog_post': blog_post})

@login_required
def delete_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    
    if blog_post.author !=request.user:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('home')
    
    if request.method == 'POST':
        blog_post.delete()
        messages.success(request, "The post was deleted successfully.")
        return redirect('home')
    
    return render(request, 'confirm_delete.html', {'blog_post': blog_post})

def search(request):
    query = request.GET.get('q')
    if not request.user.is_authenticated:
        
        return redirect('user_login')
    
    results = BlogPost.objects.filter(title_icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})
        