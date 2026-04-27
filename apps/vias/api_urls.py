from django.urls import path
from .views_api import ViaViews

urlpatterns = [
    path('vias/', ViaViews.as_view(), name='vias'),
]