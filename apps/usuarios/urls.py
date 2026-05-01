from django.urls import path

from . import views

app_name = "apps.usuarios"

urlpatterns = [
    # autenticação
    path("login/", views.login_view, name="login"),
    path("verificar-codigo/", views.verificar_codigo, name="verificar_codigo"),
    path('reenviar-codigo/',   views.reenviar_codigo,  name='reenviar_codigo'),
    path("logout/", views.logout_view, name="logout"),
    path("cadastro/", views.registrar, name="cadastro"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/editar-usuario/<int:pk>/", views.editar_usuario, name="editar_usuario"),  # mudei aqui (aiane)
    path("perfil/editar-email/<int:pk>/", views.editar_email, name="editar_email"),  # mudei aqui (aiane)
    path("configuracoes/", views.configuracoes, name="configuracoes"),

    # CRUD — somente admin
    path("gerenciar/", views.lista_usuarios, name="lista"),
    path("gerenciar/novo/", views.usuario_criar, name="criar"),
    path("gerenciar/<int:pk>/", views.usuario_detalhe, name="detalhe"),
    path("gerenciar/<int:pk>/editar/", views.usuario_editar, name="editar"),
    path("gerenciar/<int:pk>/deletar/", views.usuario_deletar, name="deletar"),
    path("gerenciar/<int:pk>/toggle/", views.usuario_toggle_ativo, name="toggle"),
    path('solicitar-mudanca/', views.solicitar_mudanca_tipo, name='solicitar_mudanca'),
    path('atualizar-tipo/<int:user_id>/<str:novo_tipo>/', views.editar_tipo_usuario, name='atualizar_tipo'),
]
