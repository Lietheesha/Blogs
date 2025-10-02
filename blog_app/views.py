from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .models import *
from .models import Comment, Post

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return JsonResponse({"success":False,"messages":"Please fill the fields"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "messages": "Login successful"})
            return redirect("home")
        else:
            return JsonResponse({"success": False, "messages": "Invalid username or password"}) 
    else:
        return render(request, "authenticate/login.html")
    
@login_required(login_url="login") 
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, "app/home.html", {"posts": posts})

class AddView(CreateView):
    model = Post
    template_name = "app/add.html"
    fields = ["title", "content"]
    success_url = '/home/'  # Redirect to home after adding

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success":True})
        return redirect("home") 

class PostDetailView(DetailView):
    model = Post
    template_name = "app/detail.html"
    context_object_name = "post"

class EditView(UpdateView):
    model = Post
    template_name = "app/edit.html"
    fields = ["title", "content"]
    success_url = "/home/"

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs.get("pk"), user=self.request.user)
    
class DeleteView(DeleteView):
    model = Post
    template_name = "app/delete.html"
    context_object_name = "post"
    success_url = "/home/"

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs.get("pk"), user=self.request.user)
    
def my_blogs(request):
    posts = Post.objects.filter(user=request.user)
    if posts.exists() or not posts:
        return render(request, "app/my_blogs.html", {"posts": posts})
    
class CustomLogoutView(LogoutView):
    template_name = "authenticate/logout.html"
    http_method_names = ['get', 'post'] 
    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

def comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        if not content:
            return JsonResponse({"success": False, "message": "Comment cannot be empty."})
        post = get_object_or_404(Post, id=post_id)
        Comment.objects.create(user=request.user, post=post, content=content)
        return JsonResponse({"success": True, "message": "Comment added successfully."})
    return JsonResponse({"success": False, "message": "Invalid request method. "})

@login_required
def like(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "liked": liked,
            "likes_count": post.likes.count()
        })