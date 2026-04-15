from django.urls import path
from . import views

urlpatterns = [
    path('',          views.index,      name='index'),
    path('mapa/',     views.mapa,       name='mapa'),
    path('dashboard/',views.dashboard,  name='dashboard'),
]
