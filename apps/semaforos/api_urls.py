#api rest de semaforos
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import SemaforoViewSet

router = DefaultRouter()
router.register(r'', SemaforoViewSet, basename='semaforo')

urlpatterns = [
    path('', include(router.urls)),
]