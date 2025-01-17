from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,AddrecordForm
from .models import Record

# Create your views here.
# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request,"you have been sucessfully logged out")
    return redirect('home')


def home(request):

    records=Record.objects.all()
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

        return render(request,'home.html',{'records':records})


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

def customer_record(request,pk):
    if request.user.is_authenticated:
        #lookup user records
        customer_record=Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record}) 
    else:
        messages.success(request,"you have to be logged in for viewing that record")
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"record has been deleted sucessfully")
        return redirect('home')
    else:
        messages.success(request,"you must be logged in for deleting record")
        return redirect('home')



def add_record(request):
    form=AddrecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=="POST":
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record added")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"you must be logged in to add record")
        return redirect('home')


def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=AddrecordForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Records has been updated")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"you must be logged in for updating record")
        return redirect('home')

        


