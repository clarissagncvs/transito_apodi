# Importa o modelo base de usuário do Django (já vem com autenticação pronta)
from django.contrib.auth.models import AbstractUser

# Importa o módulo de modelos do Django
from django.db import models


# Cria um modelo de usuário personalizado herdando do AbstractUser
class Usuario(AbstractUser):

    # Classe interna para definir os tipos de usuário (como enum)
    class Tipo(models.TextChoices):
        # Tipo cidadão
        CIDADAO = 'CIDADAO', 'Cidadão'

        # Tipo agente de trânsito
        AGENTE = 'AGENTE', 'Agente de Trânsito'

        # Tipo administrador
        ADMIN = 'ADMIN', 'Administrador'


    # Campo que armazena o tipo de usuário
    tipo = models.CharField(
        max_length=10,                # Limite de 10 caracteres
        choices=Tipo.choices,         # Só permite valores definidos na classe Tipo
        default=Tipo.CIDADAO          # Valor padrão é cidadão
    )


    # Campo para telefone (opcional)
    telefone = models.CharField(
        max_length=20,  # Limite de caracteres
        blank=True      # Permite deixar vazio no formulário
    )


    # Campo para foto do usuário
    foto = models.ImageField(
        upload_to='usuarios/',  # Pasta onde as imagens serão salvas
        blank=True,             # Não obrigatório no formulário
        null=True               # Pode ser nulo no banco de dados
    )


    # Propriedade que verifica se o usuário é agente
    @property
    def is_agente(self):
        # Retorna True se o tipo for AGENTE
        return self.tipo == self.Tipo.AGENTE


    # Propriedade que verifica se o usuário é administrador de trânsito
    @property
    def is_admin_transito(self):
        # Retorna True se o tipo for ADMIN
        return self.tipo == self.Tipo.ADMIN


    # Define como o objeto será exibido (ex: no admin do Django)
    def __str__(self):
        # Exibe username + tipo formatado (ex: "joao (Cidadão)")
        return f'{self.username} ({self.get_tipo_display()})'