from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ViaViewSet

router = DefaultRouter()
router.register(r'', ViaViewSet, basename='via')

urlpatterns = [
    path('', include(router.urls)),
]
