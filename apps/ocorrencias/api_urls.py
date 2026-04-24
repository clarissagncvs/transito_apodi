# api rest de ocorrencias
from django.urls import (
    path,
    include,
)  # Importa funções para criar rotas e incluir outras URLs
from rest_framework.routers import (
    DefaultRouter,
)  # Importa o roteador automático do Django REST Framework
from .views_api import (
    OcorrenciaViewSet,
    AlertaViewSet,
)  # Importa os ViewSets da API (lógica das rotas)

# from .views_api import OcorrenciaViewSet, AlertaViewSet

router = (
    DefaultRouter()
)  # Cria um roteador que gera URLs automaticamente para os ViewSets

# router.register(r'ocorrencias', OcorrenciaViewSet)
# router.register(r'alertas', AlertaViewSet)


router.register(
    r"alertas", AlertaViewSet, basename="alerta"
)  # Registra rotas para alertas (/alertas/)
router.register(
    r"", OcorrenciaViewSet, basename="ocorrencia"
)  # Registra rotas principais (/), ou seja, ocorrências

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # Inclui todas as rotas geradas automaticamente pelo router
]
# a ordem do register importa — o alertas precisa vir antes do '' porque o router testa as rotas em sequência e o '' vazio engoleria tudo se viesse primeiro.
