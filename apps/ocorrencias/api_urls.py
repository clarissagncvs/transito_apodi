from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views_api import AlertaViewSet, OcorrenciaViewSet

router = DefaultRouter()

# a ordem do register importa — o alertas precisa vir antes do '' porque o router
# testa as rotas em sequência e o '' vazio engoleria tudo se viesse primeiro.

# Registra rotas para alertas (/alertas/)
router.register(r"alertas", AlertaViewSet, basename="alerta")
router.register(r"", OcorrenciaViewSet, basename="ocorrencia")

urlpatterns = [
    path("", include(router.urls)),
]
