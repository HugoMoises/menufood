"""
URL configuration for menufood project.

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
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from appmenu.views import login_view, cadastro, home, produtos, sobre, carrinho, criar_produto, editar_produto, deletar_produto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('home/', home, name='home'),
    path('produtos/', produtos, name='produtos'),
    path('sobre/', sobre, name='sobre'),
    path('carrinho/', carrinho, name='carrinho'),
    path('produtos/criar/', criar_produto, name='criar_produto'),
    path('produtos/editar/<int:id>/', editar_produto, name='editar_produto'),
    path('produtos/deletar/<int:id>/', deletar_produto, name='deletar_produto'),

]
