from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.core import serializers
from datetime import date
from todolist.forms import CreateTaskForm
from todolist.models import Task

@login_required(login_url='/todolist/login/')
def show_todolist(request):
    data = Task.objects.filter(user=request.user)

    if request.method == "POST":
        id = request.POST.get('id')
        task = Task.objects.filter(pk=id).first()

        update_task = request.POST.get('update_task')
        delete_task = request.POST.get('delete_task')

        if update_task == "done":
            task.is_finished = True
            task.save()
            messages.success(request, 'Status Task berhasil diubah!')
        elif update_task == "not_done":
            task.is_finished = False
            task.save()
            messages.success(request, 'Status Task berhasil diubah!')
        
        if delete_task == "delete":
            try:
                task.delete()
                messages.success(request, 'Task berhasil dihapus!')
            except AttributeError:
                pass

    context = {
        'task_list': data,
        'current_user': request.COOKIES['current_user'],
    }
    return render(request, 'todolist.html', context)

@login_required(login_url='/todolist/login/')
def show_json(request):
    data = Task.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/todolist/login/')
def create_task(request):
    form = CreateTaskForm()

    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task_data = form.save(commit=False)
            task_data.user = request.user
            task_data.date = date.today()
            task_data.save()
            form.save_m2m()
            messages.success(request, 'Task berhasil ditambahkan!')
            return redirect('todolist:show_todolist')
        else:
            messages.info(request, 'Ada yang bermasalah, coba lagi!')
    
    context = {
        'form': form,
        'current_user': request.COOKIES['current_user'],
    }
    return render(request, 'create_task.html', context)

@login_required(login_url='/todolist/login/')
def add_task(request):
    form = CreateTaskForm()

    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task_data = form.save(commit=False)
            task_data.user = request.user
            task_data.date = date.today()
            task_data.save()
            form.save_m2m()
            return HttpResponse("Task Added", status=201)

    return HttpResponseNotFound()

@login_required(login_url='/todolist/login/')
def delete_task(request, id):
    if request.method == 'DELETE':
        task = Task.objects.filter(pk=id)
        task.delete()
        return HttpResponse("Task Deleted", status=204)
    
    return HttpResponseNotFound()

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat!')
            return redirect('todolist:login')
        else:
            messages.info(request, 'Ada yang bermasalah, coba lagi dan ikuti instruksi!')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse('todolist:show_todolist'))
            response.set_cookie('current_user', username)
            response.set_cookie('user_id', user.id)
            return response
        else:
            messages.info(request, 'Username atau password salah, coba lagi!')

    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('current_user')
    response.delete_cookie('user_id')
    return response