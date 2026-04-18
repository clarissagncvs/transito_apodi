# Importa a função path para definir rotas (URLs)
from django.urls import path

# Importa a view pronta do Django REST Framework que gera token de autenticação
from rest_framework.authtoken.views import obtain_auth_token

# Lista de URLs (rotas) da aplicação
urlpatters = [
    # Define a rota 'token/'
    # Quando um POST for feito nessa URL com username e password,
    # o Django retorna um token de autenticação
    path('token/', obtain_auth_token, name='token'),
]

# OBS:
# Essa URL cria um endpoint de autenticação via token.
# Exemplo de uso:
# POST /api/usuarios/token/
# Body:
# {
#   "username": "usuario",
#   "password": "senha"
# }
#
# Resposta:
# {
#   "token": "abc123..."
# }
#
# Esse token deve ser usado nas próximas requisições no header:
# Authorization: Token abc123...