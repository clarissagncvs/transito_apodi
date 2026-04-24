from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #    path('mapa/',     views.mapa,       name='mapa'),
    #    path('dashboard/',views.dashboard,  name='dashboard'),
]
