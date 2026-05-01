from django.urls import path
from .mapa_api_views import MapaView

urlpatterns = [
    path('', MapaView.as_view(), name='mapa'),
]
