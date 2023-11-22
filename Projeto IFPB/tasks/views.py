from django.shortcuts import render, redirect
from .forms import CategoryForm, TaskForm
from django.contrib import messages
from .models import Task, Category
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required


@login_required(login_url='/contas/login')
def add_category(request):
    template_name = 'categories/add_category.html'
    if request.method == 'POST':
        form = CategoryForm(request.user.profile, request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user.profile
            f.save()
            messages.success(request, 'Categoria adicionada com sucesso')
            return redirect('tasks:add_category')
    else:
        form = CategoryForm(request.user)
        return render(request, template_name, context={'form': form})


@login_required(login_url='/contas/login')
def edit_category(request, id_category):
    template_name = 'categories/edit_category.html'
    category = Category.objects.get(pk=id_category, owner=request.user.profile)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria editada com sucesso!')
            return redirect('tasks:list_categories')
        else:
            messages.error(request, "Formulário não válido!")
            return redirect('tasks:list_categories')

    else:
        form = CategoryForm(instance=category, user=request.user)

    return render(request, template_name, context={'form': form})


@login_required(login_url='/contas/login')
def list_categories(request):
    template_name = 'categories/list_categories.html'
    categories = Category.objects.filter(owner=request.user.profile)
    context = {'categories': categories}
    return render(request, template_name, context)


@login_required(login_url='/contas/login')
def delete_category(request, id_category):
    category = Category.objects.get(pk=id_category, owner=request.user.profile)
    category.delete()
    messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('tasks:list_categories')


# Task ---------------------------------------------------------------------

@login_required(login_url='/contas/login')
def add_task(request):
    context = {}
    template_name = 'tasks/add_task.html'
    if request.method == 'POST':
        form = TaskForm(request.user.profile, request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user.profile
            f.save()
            form.save_m2m()
            messages.success(request, 'Tarefa adicionada com sucesso.')
    form = TaskForm(user=request.user.profile)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login')
def edit_task(request, id_task):
    template_name = 'tasks/edit_task.html'
    task = Task.objects.get(id=id_task, owner=request.user.profile)
    if request.method == 'POST':
        form = TaskForm(request.user.profile, request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:list_tasks')
    else:
        form = TaskForm(request.user.profile, instance=task)
    context = {
        'task': task,
        'form': form
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login')
def list_tasks(request):
    template_name = 'tasks/list_tasks.html'
    tasks = Task.objects.filter(owner=request.user.profile)
    now = timezone.now().date() - timedelta(days=1)
    context = {
        'tasks': tasks,
        "today": now,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login')
def delete_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user.profile:
        task.delete()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta tarefa.')
        return (redirect('core:home'))
    return (redirect('tasks:list_tasks'))


@login_required(login_url='/contas/login')
def complete_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user.profile:
        task.completed = True
        task.save()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta tarefa.')
        return (redirect('core:home'))
    return (redirect('tasks:list_tasks'))


@login_required(login_url='/contas/login')
def not_complete_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user.profile:
        task.completed = False
        task.save()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta tarefa.')
        return (redirect('core:home'))
    return (redirect('tasks:list_tasks'))


@login_required(login_url='/contas/login')
def show_task(request, id_task):
    task = Task.objects.get(id=id_task)
    context = {
        'task': task,
    }
    return render(request, 'tasks/show_task.html', context)