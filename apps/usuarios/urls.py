# Importa a função path, usada para definir rotas (URLs) no Django
from django.urls import path

# Importa uma view pronta do Django para fazer logout de usuários
from django.contrib.auth.views import LogoutView

# Importa todas as funções do arquivo views.py do app atual
from . import views


# Define um namespace para esse conjunto de URLs
# Isso permite usar nomes como: 'usuarios:login', 'usuarios:perfil'
app_name = 'apps.usuarios'


# Lista de rotas do aplicativo
urlpatterns = [

    # Rota raiz do app (ex: /usuarios/)
    # Chama a função home definida em views.py
    path('', views.home, name='home'),

    # Rota de login (ex: /usuarios/login/)
    # Chama a view personalizada de login
    path('login/', views.login_view, name='login'),

    # Rota de logout (ex: /usuarios/logout/)
    # Usa a view pronta do Django (não precisa criar função)
    path('logout/', LogoutView.as_view(), name='logout'),

    # Rota de registro de usuário (ex: /usuarios/registro/)
    path('registro/', views.registrar, name='registro'),

    # Rota do perfil do usuário (ex: /usuarios/perfil/)
    # Geralmente protegida com login_required
    path('perfil/', views.perfil, name='perfil'),
]