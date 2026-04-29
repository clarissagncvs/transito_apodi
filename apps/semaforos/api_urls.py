# api rest de semaforos
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import SemaforoViewSet

# from .views_api import OcorrenciaViewSet

router = DefaultRouter()

# router.register(r'ocorrencias', OcorrenciaViewSet)  ❌ comenta

router.register(r"", SemaforoViewSet, basename="semaforo")

urlpatterns = [
    path("", include(router.urls)),
]
