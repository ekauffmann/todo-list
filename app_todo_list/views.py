from django.shortcuts import render, redirect, HttpResponse
from models import Task

# Create your views here.
def showTaskView(request):
    tasks = Task.objects.all()
    return render(request, 'show_tasks.html', {'tasks' : tasks})
    
def submitTask(request):
    if request.method == "POST":
        text = request.POST.get('text', '')
        task = Task(text=text)
        task.save()
    return redirect('/showtask')
    
def checkTask(request):
    if request.method == "POST":
        id = request.POST.get('id', 0)
        task = Task.objects.get(pk = id)
        Task.objects.filter(pk = id).update(state = 1)
        task.refresh_from_db()
    return redirect('/showtask')