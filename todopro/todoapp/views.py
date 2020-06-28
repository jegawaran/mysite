from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from userdetailapp.models import Project
import requests
import json

# Create your views here.

def home(request):
    projects = Project.objects.all()
    news_url = requests.get('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=88a21b7e651a4648951f42048899dd78')
    api = json.loads(news_url.content)
    return render(request,'todoapp/home.html',{'projects':projects,'api':api})


def signupuser(request):
    if request.method == 'GET':
        return render(request,'todoapp/signupuser.html',{'form':UserCreationForm})
    else:
        #create user
        print(request)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'],email=request.POST['email'],first_name=request.POST['first_name'],last_name=request.POST['last_name'])
                user.save()
                login(request,user)
                return redirect('currentpage')
            except IntegrityError:
                return render(request,'todoapp/signupuser.html',{'form':UserCreationForm,'error':'integrity Error'})
        else:
            return render(request,'todoapp/signupuser.html',{'form':UserCreationForm,'error':'Password did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request,'todoapp/loginuser.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todoapp/loginuser.html',{'form':AuthenticationForm,'error':'username or password did not match'})
        else:
            login(request,user)
            return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todoapp/createtodo.html',{'form':TodoForm})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentpage')
        except ValueError:
            return render(request,'todoapp/createtodo.html',{'form':TodoForm,'error':'length is crieteria '})

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return render(request,'todoapp/logoutuser.html',{'logout':request.user.username})

@login_required
def currentpage(request):
    todo = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todoapp/currentpage.html',{'todos':todo})

@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        title = "Edit Todo"
        return render(request,'todoapp/viewtodo.html',{'todo':todo,'form':form,'title':title})
    else:
        form = TodoForm(request.POST,instance=todo)
        form.save()
        return redirect('currentpage')

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentpage')

@login_required
def todoDelete(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        #todo.datecompleted = timezone.now()
        todo.delete()
        return redirect('currentpage')

@login_required
def completedtodo(request):
    todo = Todo.objects.filter(user=request.user,datecompleted__isnull=False)
    return render(request,'todoapp/completedtodo.html',{'todo':todo})
