from django.contrib import admin  # Importa o painel administrativo do Django
from django.urls import path, include  # path cria rotas e include permite importar URLs de outros apps
from django.conf import settings  # Permite acessar configurações do settings.py
from django.conf.urls.static import static  # Usado para servir arquivos de mídia em desenvolvimento
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),  # Rota para acessar o painel admin (/admin/)



    path('', include('apps.vias.urls')),  # Rota principal do site (/) usando as URLs do app vias
    path('ocorrencias/', include('apps.ocorrencias.urls')),  # Rotas web relacionadas a ocorrências
#    path('semaforos/', include('apps.semaforos.urls')),  # Rotas web relacionadas a semáforos
    path('', lambda request: HttpResponse("Página inicial")),
    path('usuarios/', include('apps.usuarios.urls')),  # Rotas web relacionadas a usuários

#    path('api/vias/', include('apps.vias.api_urls')),  # Endpoints da API REST para vias
#    path('api/ocorrencias/', include('apps.ocorrencias.api_urls')),  # Endpoints da API REST para ocorrências
#    path('api/semaforos/', include('apps.semaforos.api_urls')),  # Endpoints da API REST para semáforos
#    path('api/usuarios/', include('apps.usuarios.api_urls')),  # Endpoints da API REST para usuários
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve arquivos de mídia (ex: imagens) em desenvolvimento
