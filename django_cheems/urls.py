"""
URL configuration for django_cheems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from hello import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('display/', views.display, name='inicio'),
    path('logs/', views.logs, name='logs'),
    path('index/', views.index, name='index'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('usuarios/<int:id_user>/',
         views.historial_ordenes, name='historial_ordenes'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ordenes/<int:id_work_order>/estado/',
         views.cambiar_estado, name='cambiar_estado')
]
