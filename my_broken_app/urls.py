from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name="my_broken_app/index.html"), name="login"),
    path("login/", LoginView.as_view(template_name="my_broken_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="my_broken_app/logout.html"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/completed', views.CompletedTaskListView.as_view(), name='completed_task_list'),
    path('tasks/new', views.TaskNew.as_view(), name='task_new'),
    path('tasks/create', views.add_task, name='task_create'),
    path('tasks/complete/<int:pk>', views.complete_task, name='task_complete'),
    path('tasks/delete/<int:pk>', views.delete_task, name='task_delete'),
]
