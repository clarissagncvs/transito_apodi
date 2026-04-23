# Importa a classe base AppConfig, usada para configurar apps no Django
from django.apps import AppConfig


# Define a classe de configuração do app "usuarios"
class UsuariosConfig(AppConfig):

    # Define o tipo padrão de chave primária automática para os models
    # BigAutoField = inteiro grande (64 bits), evita limite baixo de IDs
    default_auto_field = "django.db.models.BigAutoField"

    # Nome do app (caminho completo do módulo Python)
    # Isso permite que o Django localize corretamente o app
    name = "apps.usuarios"
