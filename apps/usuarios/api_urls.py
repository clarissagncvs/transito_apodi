from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views_api import UsuarioViewSet

router = DefaultRouter()
router.register(r"", UsuarioViewSet, basename="usuario")

urlpatterns = [
    path("token/", obtain_auth_token, name="token"),
] + router.urls
