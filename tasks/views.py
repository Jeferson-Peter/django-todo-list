from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task
from django.utils import timezone

from dateutil.parser import parse


@login_required
def index(request):
    query = request.GET.get('q')
    if query:
        tasks_list = Task.objects.filter(user=request.user, content__icontains=query).order_by('-due_date')
    else:
        tasks_list = Task.objects.filter(user=request.user).order_by('-due_date')

    paginator = Paginator(tasks_list, 5)  # 5 tarefas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tasks/index.html', {'page_obj': page_obj})

@login_required
def add_task(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        if due_date:
            due_date = timezone.make_aware(parse(due_date), timezone.get_current_timezone())
        else:
            due_date = None
        Task.objects.create(content=content, category=category, priority=priority, due_date=due_date, user=request.user)
        messages.success(request, 'Tarefa adicionada com sucesso!')
    return redirect('index')
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Tarefa excluída com sucesso!')
    return redirect('index')


@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = True
    task.save()
    messages.success(request, 'Tarefa marcada como concluída!')
    return redirect('index')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.content = request.POST.get('content')
        task.save()
        messages.success(request, 'Tarefa editada com sucesso!')
        return redirect('index')
    return render(request, 'tasks/edit.html', {'task': task})
