from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def render_login(request):
    return render(request,'todoapp/render_login.html')

def doLogin(request):
    if request.method != 'POST':
        return HttpResponse('METHOD NOT ALLOWED')
    
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = authenticate(request,username=username,password=password)

        if user_obj is not None:
            login(request,user_obj)
            messages.success(request,f'Welcome {username}')
            return redirect('todoapp:dashboard')
        else:
            messages.error(request,'USERNAME OR PASSWORD IS INVALID')
            return redirect('todoapp:render_login')
        
def register(request):

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        form.save()
        return redirect('todoapp:render_login')

    return render(request,'todoapp/register.html',{'form':form})



@login_required
def dashboard(request):
    
    #query task item based on login user
    task_items = Task.objects.filter(task_user=request.user.id)
    id = request.user.id
    form = TaskForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.task_user = request.user
            todo_item.save()
            return redirect('todoapp:dashboard')

    #querying pending task    
    task_pending = Task.objects.filter(task_user=request.user,task_status = False).count()
        

    context = {
        'tasks':task_items,
        'form':form,
        'id':id,
        'task_pending':task_pending
    }

    
    return render(request,'todoapp/dashboard.html',context=context)

@login_required
def update(request,id):
    task = Task.objects.get(pk=id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('todoapp:dashboard')
    else:
        form = TaskForm(instance=task)


    return render(request,'todoapp/update-form.html',{'form':form})


def done(request,id):
    task = Task.objects.get(pk=id)
    task.task_status = True
    task.save()
    return redirect('todoapp:dashboard')

def undone(request,id):
    task = Task.objects.get(pk=id)
    task.task_status = False
    task.save()
    return redirect('todoapp:dashboard')

def delete_task(request,id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('todoapp:dashboard')

def doLogout(request):
    logout(request)
    return redirect('todoapp:render_login')
