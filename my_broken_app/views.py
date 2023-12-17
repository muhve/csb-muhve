from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .models import Task


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "my_broken_app/register.html"

class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "my_broken_app/task_detail.html"

class TaskNew(generic.CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = "my_broken_app/task_new.html"

class TaskListView(generic.ListView):
    model = Task
    template_name = "my_broken_app/task_list.html"

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

def add_task(request):
    if request.method == 'POST':
        todo_title = request.POST.get("title")
        todo_desc = request.POST.get("description")
        task = Task.objects.create(title=todo_title, description=todo_desc, user=request.user, done=False)
        return redirect("task_list")