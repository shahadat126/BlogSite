from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
def Home(request):
    try:
        return render(request,"blogapp/base.html")
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})

@login_required
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