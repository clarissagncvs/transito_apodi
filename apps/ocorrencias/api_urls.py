from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views_api import OcorrenciaViewSet

router = DefaultRouter()

router.register(r"", OcorrenciaViewSet, basename="ocorrencia")

urlpatterns = [
    path("", include(router.urls)),
]
