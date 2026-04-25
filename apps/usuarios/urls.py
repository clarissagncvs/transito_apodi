from django.urls import path

from . import views

app_name = "apps.usuarios"

urlpatterns = [
    # autenticação
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cadastro/", views.registrar, name="cadastro"),
    path("perfil/", views.perfil, name="perfil"),
    # CRUD — somente admin
    path("gerenciar/", views.usuario_lista, name="lista"),
    path("gerenciar/novo/", views.usuario_criar, name="criar"),
    path("gerenciar/<int:pk>/", views.usuario_detalhe, name="detalhe"),
    path("gerenciar/<int:pk>/editar/", views.usuario_editar, name="editar"),
    path("gerenciar/<int:pk>/deletar/", views.usuario_deletar, name="deletar"),
    path("gerenciar/<int:pk>/toggle/", views.usuario_toggle_ativo, name="toggle"),
]
