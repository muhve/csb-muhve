from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
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

    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()

    #     if obj.user != request.user:
    #         return self.handle_permission_denied()
    #     return super().dispatch(request, *args, **kwargs)
    # def handle_permission_denied(self):
    #     redirect_url = reverse_lazy('task_list')
    #     return HttpResponseRedirect(redirect_url)

class TaskNew(generic.CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = "my_broken_app/task_new.html"

class TaskListView(generic.ListView):
    model = Task
    template_name = "my_broken_app/task_list.html"

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user, done=False)
        return queryset

class CompletedTaskListView(generic.ListView):
    model = Task
    template_name = "my_broken_app/completed_task_list.html"

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user, done=True)
        return queryset

def add_task(request):
    if request.method == 'POST':
        todo_title = request.POST.get("title")
        todo_desc = request.POST.get("description")
        Task.objects.create(title=todo_title, description=todo_desc, user=request.user, done=False)
        return redirect("task_list")
    
def complete_task(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.done = True
        task.save()
        return redirect("task_list")

def delete_task(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect("task_list")