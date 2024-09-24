"""
URL configuration for todowoo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.welcome, name='welcomePage'),                # welcome page where shows first
    
    # Auth:
    path('signup/', views.signupuser, name='signupuser'),       # this is for the sign up page where the user register themselves as a new user
    path('logout/', views.logoutuser, name='logoutuser'),       # this is for logout user
    path('login/', views.loginuser, name='loginuser'),          # this is for login user
    # todo:
    path('current/', views.userTodos, name='userTodosPage'),    # this is for after we logged in into the page after signed up
    path('create/', views.createToDo, name='createToDo'),             # new task page
    path('todo/<int:todo_pk>', views.view_todo, name='viewTodo'),   # Whenever we want to do something with one object we have to mention its id and pk
    path('todo/<int:todo_pk>/complete', views.complete_todo, name='completeTodo'),  # Whenever we want to do something with one object we have to mention its id and pk
    path('todo/<int:todo_pk>/delete', views.delete_todo, name='deleteTodo'),    # Whenever we want to do something with one object we have to mention its id and pk
    path('completed', views.completed, name='completedTodosPage'),
    path('todo/<int:todo_pk>/undo', views.undo_completed_todo, name='undoTodo'),

]
