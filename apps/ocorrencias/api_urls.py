from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import OcorrenciaViewSet

# Desativamos o trailing_slash ou usamos o SimpleRouter para evitar o registro duplo
router = DefaultRouter(trailing_slash=False)
router.register(r"lista", OcorrenciaViewSet, basename="ocorrencia")

# Pegamos as urls brutas sem passar pelo format_suffix_patterns
urlpatterns = [
    path("", include(router.get_urls())),  # Usamos get_urls() diretamente
]
