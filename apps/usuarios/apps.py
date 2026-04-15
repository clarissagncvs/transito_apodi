from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'

#esse código define uma classe de configuração (AppConfig) para um aplicativo Django chamado usuarios, especificando que o tipo de chave primária automática padrão deve ser BigAutoField.
#a linha default_auto_field = 'django.db.models.BigAutoField' configura explicitamente o campo de chave primária implícito como um inteiro de 64 bits
#o atributo name = 'apps.usuarios' fornece o caminho de importação completo do aplicativo Python, o que é essencial para que o Django identifique corretamente o módulo e o inclua na lista INSTALLED_APPS.