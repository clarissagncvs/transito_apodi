from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatters = [
    path('token/', obtain_auth_token, name='token'),
]
#cria o endpoint POST /api/usuarios/token/. O time de front envia username e password e recebe o token para usar nas próximas requisições.