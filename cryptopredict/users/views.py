from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import users

# Create your views here.
def signout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request,'index.html')

def homes(request):
    return render(request,'home.html')

def account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            print("userob",user)
            userloc=users.objects.create(
                user=user,
                name=username
            )
            messages.success(request,"registration success")
        except Exception as e:
            messages.error(request,"error ")
    else:
        if request.POST and 'login' in request.POST:
            context['login']=False
            username=request.POST['username']
            password=request.POST['password']
            print(username,password)
            user=authenticate(request,username=username,password=password)
            print(user)
            if user:
                login(request,user)
                acc={'user':username}
                return render(request,'home.html')
            else:
                messages.error(request,"invalid details")
    return render(request,'account.html',context)                        
