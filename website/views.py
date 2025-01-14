from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request,"you have been sucessfully logged out")
    return redirect('home')


def home(request):
    #check to see if logging in
    if request.method =='POST':
        username=request.POST['user_name']
        password=request.POST['password']

        #Authenticate

        user=authenticate(request,username=username,password=password)


        if user is not None:
            login(request, user)
            messages.success(request,"You have been logged in sucessfully")
            return redirect('home')
        else:
            messages.success(request,"There have been error")
            return redirect('home')
    else:

        return render(request,'home.html',{})


def register_user(request):

    if request.method =='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            #Authenticate and login
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"you have been sucessfully registered welcome!!")
            return redirect('home')
        
    else:
        form=SignUpForm()
        return render(request,'register.html',{'form':form})
    
    return render(request,'register.html',{'form':form}) 