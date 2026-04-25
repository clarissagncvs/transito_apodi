# api rest de ocorrencias
from django.urls import include, path

# Importa o roteador automático do Django REST Framework
from rest_framework.routers import DefaultRouter

# Importa os ViewSets da API (lógica das rotas)
from .views_api import AlertaViewSet, OcorrenciaViewSet

# Cria um roteador que gera URLs automaticamente para os ViewSets
router = DefaultRouter()

# a ordem do register importa — o alertas precisa vir antes do '' porque o router
# testa as rotas em sequência e o '' vazio engoleria tudo se viesse primeiro.

# Registra rotas para alertas (/alertas/)
router.register(r"alertas", AlertaViewSet, basename="alerta")

# Registra rotas principais (/), ou seja, ocorrências
router.register(r"", OcorrenciaViewSet, basename="ocorrencia")

urlpatterns = [
    # Inclui todas as rotas geradas automaticamente pelo router
    path("", include(router.urls)),
]
