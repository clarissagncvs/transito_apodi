# rotas web de ocorrencias
from django.urls import path

from . import views

app_name = "ocorrencias"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("status/", views.status, name="status"),
    path("<int:pk>/atualizar-status/", views.atualizar_status, name="atualizar_status"),
    # path('registra/', views.registra, name='registra'),
    # path('<int:pk>/', views.detalhe, name='detalhe'),
    # path('<int:pk>/status/', views.atualizar_status, name='atualizar_status'),
]

# O <int:pk> captura o número da URL e passa para a view como parâmetro.
# Então /ocorrencias/5/ chama views.detalhe(request, pk=5).
