from django.shortcuts import render,redirect
from .models import Post,Category,Comment
from django.contrib.auth.models import User
from .forms import PostCreatForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count
# Create your views here.
def Home(request):
    try:
        return render(request,"blogapp/base.html")
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})


def posts_list_view(request):
    try:
        query = request.GET.get('query','')
        category_id = request.GET.get('category_id','')
        status = request.GET.get('status','')
        posts = Post.objects.select_related('category','author')
        
        if query:
            posts = posts.filter(
                Q(title__icontains = query)|
                Q(content__icontains=query)|
                Q(author__username__icontains = query)
            )
        
        if category_id:
            posts = posts.filter(category__id = category_id)
        
        if status:
            posts = posts.filter(status = status)
            
        posts_summary_list= []
        for post  in posts:
            posts_summary_list.append(
                {
                    'id': post.id,
                    'title' : post.title,
                    'content' : post.content[:100],
                    'category' : post.category_id,
                    'created' : post.created
                } 
                )
        my_posts = None
        my_categories= None
        if request.user.is_authenticated:
            my_posts = Post.objects.filter(author=request.user).aggregate(total_posts= Count('id'))   
            
            my_categories= Category.objects.annotate(post_count= Count('posts')) 
            
            
        return render(request,"blogapp/post_list_view.html",{
            'posts_summary_list':posts_summary_list,
            'categories': Category.objects.all(),
            'status_choices' : Post.STATUS_CHOICES,
            'query' : query,
            'selected_category':category_id,
            'selected_status' : status,
            'my_posts': my_posts,
            'my_categories' : my_categories,
            'total_result': len(posts_summary_list)
            
            
            })
    except Exception as e:
        return render(request,'blogapp/error.html',{'error':e})
# def post_details_view(request,pk):
    # try:
    #     posts= Post.objects.get(id=pk)
    #     return render(request,"blogapp/post_details_view.html",{'posts':posts})
def post_details_view(request,pk):
    try:
        post = Post.objects.get(id=pk)
        parent_comments = post.comments.filter(parent__isnull=True).prefetch_related('replies')

        form = CommentForm()
        if request.method == "POST" and request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent = Comment.objects.get(id=parent_id)
                comment.save()
                return redirect('blogapp:post_details',pk=post.id)
        return render(
            request,
            'blogapp/post_details_view.html',
            {
                'post':post,
                'parent_comments':parent_comments,
                'form':form
            }
        )
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