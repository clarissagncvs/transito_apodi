# rotas web de semaforos
from django.urls import path
from . import views

app_name = "semaforos"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("<int:pk>/", views.detalhe, name="detalhe"),
    path("<int:pk>/estado/", views.atualizar_estado, name="atualizar_estado"),
]
