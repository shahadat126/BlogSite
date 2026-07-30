from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.
def register_view(request):
    if request.method == "POST":
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            #login(request,user)
            messages.success(request,"registration successful")
            return redirect('accounts:user_login')
    else:
        forms=RegistrationForm()
    return render(request,"accounts/register.html",{"form":forms})    

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username= username,password=password)
        if user is not None:
            login(request,user)
            return redirect('blogapp:posts_list')
        else:
            messages.error(request,"Invalid username or password")
    return render(request,"accounts/login.html")

def Logout(request):
    logout(request)
    return redirect('accounts:user_login')
