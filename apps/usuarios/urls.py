from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'apps.usuarios'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', views.registrar, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
]

#from django.urls import path importa a função path usada para definir urls
#from django.contrib.auth.views import LogoutView importa view pronta do django para logout
#from . import views importa as funções views do app, nesse caso, do usuário
#urlpatterns = [] define as rotas do app
#path(...) sao as rotasS