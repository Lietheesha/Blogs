from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .models import *

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")   
    else:
        return render(request, "authenticate/login.html")
    
@login_required(login_url='login') 
def home(request):
    posts = Post.objects.all().order_by('date_posted')
    return render(request, "app/home.html", {"posts": posts})

class AddView(CreateView):
    model = Post
    template_name = "app/add.html"
    fields = ["title", "content"]
    success_url = '/home/'  # Redirect to home after adding

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
