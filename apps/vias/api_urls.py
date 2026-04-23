#api rest de vias
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ViaViewSet

# from .views_api import OcorrenciaViewSet, AlertaViewSet

router = DefaultRouter()
# router.register(r'ocorrencias', OcorrenciaViewSet)  ❌ comenta
# router.register(r'alertas', AlertaViewSet)   

router.register(r'', ViaViewSet, basename='via')

urlpatterns = [
    path('', include(router.urls)),
]
#O DefaultRouter gera automaticamente todas essas rotas: