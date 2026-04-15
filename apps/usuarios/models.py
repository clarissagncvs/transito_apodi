from django.contrib.auth.models import AbstractUser
from django.db import models
class Usuario(AbstractUser):

    class Tipo(models.TextChoices):
        CIDADAO = 'CIDADAO', 'Cidadão'
        AGENTE = 'AGENTE', 'Agente de Trânsito'
        ADMIN = 'ADMIN', 'Administrador'

#AbstractUser já traz username, password, email, first_name, last_name, is_active_, date_joined e os métodos de autenticação, só faltando adicionar os tipos
#CharField é um modelo de campo de string projetado para armazenar textos curtos a médios
#a classe Usuario herda AbstractUser, fornecendo a implementação completa do modelo de usuário padrão, servindo como base para criar modelos de usuários personalizados sem redefinir toda a lógica de autenticação
#a classe Tipo herda models.TextChoices, permitindo definir escolhar para campos de modelo de forma classe-based
    tipo = models.CharField(
    max_length=10,
    choices=Tipo.choices,
    default=Tipo.CIDADAO
    )
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(
        upload_to='usuarios/', blank=True, null=True
    )
    

#max_length define o tanto de caracteres que serão aceitos no nome do usuário
#choices=Tipo.choices diz que o valor armazenado na variável choice deve ser algum dos tipos registrados na classe
#default=Tipo.CIDADAO diz que se nenhuma informação for colocada o tipo de usuário padrão será CIDADAO
#telefone = models.CharField(max_length=20, blank=True) define um campo onde o número de telefone tem um limite de caracteres e permite que o campo seja deixado vazio nos formulários
#o campo foto = models.ImageField(upload_to='usuarios/', blank=True, null=True) armazena as imagens salvas na pasta usuarios/ dentro de um diretório de mídia, permitindo que o upload seja opcional tando no BD como no formulário

@property
def is_agente(self):
    return self.tipo == self.Tipo.AGENTE

@property
def is_admin_transito(self):
    return self.tipo == self.Tipo.ADMIN

def __str__(self):
    return f'{self.username} ({self.get_tipo_display()})'

#o uso do @property transforma métodos em atributos de acesso, permitindo que funções como is_agente e is_admin_transito sejam acessadas como se fossem variáveis (ex: obj.is_agente) em vez de serem chamadas com parênteses, encapsulando a lógica de verificação de condições, como comparar self.tipo com self.Tipo.AGENTE

