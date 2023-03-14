from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,Addform
from . models import Record
# Create your views here.
def home(request):
    records=Record.objects.all()
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
             login(request,user)
             messages.success(request,"You Have Been Login Sucessfully!...")
             return redirect('home')
        else:
            messages.success(request,"There was an error while Logging in. Please Try again!...")
            return redirect('home')
    return render(request,'home.html',{'records':records})


def logout_user(request):
    logout(request)
    messages.success(request,"You Have been Loged Out!.....")
    return redirect('home')

def register_user(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            messages.success(request,"You have been sucessfully registered! Welcome!...")
            return redirect('home')
    else:
        form=SignUpForm()
        return render(request,'register.html',{'form':form})    
    return render(request,'register.html',{'form':form})


def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,'You must be Logged in to view this page!...')
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Record has been deleted sucessfully!...')
        return redirect('home')

def add_record(request):
    form=Addform(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record=form.save()
                messages.success(request,'Record Added...')
                return redirect('home')
        return render(request,'addrecord.html',{'form':form})
    else:
        messages.success(request,'You must be logged in ....')
        return redirect('home')
    
def update_record(request,pk):
    if request.user.is_authenticated:
        current_user=Record.objects.get(id=pk)
        form=Addform(request.POST or None,instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request,'Record has been updated..!')
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,'You must be Logged in...!')
        return redirect('home')