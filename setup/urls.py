"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin  # Importa o painel administrativo do Django
from django.urls import path, include  # path cria rotas e include permite importar URLs de outros apps
from django.conf import settings  # Permite acessar configurações do settings.py
from django.conf.urls.static import static  # Usado para servir arquivos de mídia em desenvolvimento
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),  # Rota para acessar o painel admin (/admin/)



#    path('', include('apps.vias.urls')),  # Rota principal do site (/) usando as URLs do app vias
#    path('ocorrencias/', include('apps.ocorrencias.urls')),  # Rotas web relacionadas a ocorrências
#    path('semaforos/', include('apps.semaforos.urls')),  # Rotas web relacionadas a semáforos
    path('', lambda request: HttpResponse("Página inicial")),
    path('usuarios/', include('apps.usuarios.urls')),  # Rotas web relacionadas a usuários

#    path('api/vias/', include('apps.vias.api_urls')),  # Endpoints da API REST para vias
#    path('api/ocorrencias/', include('apps.ocorrencias.api_urls')),  # Endpoints da API REST para ocorrências
#    path('api/semaforos/', include('apps.semaforos.api_urls')),  # Endpoints da API REST para semáforos
#    path('api/usuarios/', include('apps.usuarios.api_urls')),  # Endpoints da API REST para usuários
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve arquivos de mídia (ex: imagens) em desenvolvimento
