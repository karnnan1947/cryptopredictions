from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import users
from . forms import FeedbackForm

# Create your views here.
def signout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request,'index.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='/account')
def homes(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Automatically assign the logged-in user
            feedback.save()
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
