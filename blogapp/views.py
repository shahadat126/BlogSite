from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from .forms import PostCreatForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def Home(request):
    try:
        return render(request,"blogapp/base.html")
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})


def posts_list_view(request):
    try:
        posts = Post.objects.all()
            
        posts_summary_list= []
        for post  in posts:
            posts_summary_list.append(
                {
                    'id': post.id,
                    'title' : post.title,
                    'content' : post.content[:100]
                } 
                )
        return render(request,"blogapp/post_list_view.html",{'posts_summary_list':posts_summary_list})
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})
def post_details_view(request,pk):
    try:
        posts= Post.objects.get(id=pk)
        return render(request,"blogapp/post_details_view.html",{'posts':posts})
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})
    
def post_create(request):
    try:
        form= PostCreatForm()
        if request.method == "POST":
            form= PostCreatForm(request.POST)
            if form.is_valid():
                Post.objects.create(
                    title = request.POST.get('title'),
                    content = request.POST.get('content'),
                    category = form.cleaned_data['category'],
                    author = request.user,
                )
        return render(request,'blogapp/post_create.html',{'form':form})
            
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})