from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


# model customizado de usuário baseado no abstractuser do django
class Usuario(AbstractUser):

    # enum para tipos de usuário (melhor que usar string solta)
    class Tipo(models.TextChoices):
        CIDADAO = 'CIDADAO', 'Cidadão'
        AGENTE  = 'AGENTE',  'Agente de Trânsito'
        ADMIN   = 'ADMIN',   'Administrador'

    # define o tipo do usuário no sistema
    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.CIDADAO,
        verbose_name='tipo de usuário'
    )

    # telefone opcional com validação de 10 ou 11 dígitos numéricos
    telefone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\d{10,11}$', 'telefone inválido')]
    )

    # imagem de perfil do usuário (armazenada em /media/usuarios/)
    foto = models.ImageField(
        upload_to='usuarios/',
        blank=True,
        null=True,
        verbose_name='foto de perfil'
    )

    # data automática de criação do usuário
    criado_em = models.DateTimeField(auto_now_add=True)

    # propriedade auxiliar para verificar se é agente
    @property
    def is_agente(self):
        return self.tipo == self.Tipo.AGENTE

    # propriedade auxiliar para verificar se é admin do sistema de trânsito
    @property
    def is_admin_transito(self):
        return self.tipo == self.Tipo.ADMIN

    class Meta:
        # nome amigável no admin
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

        # ordenação padrão: mais recentes primeiro
        ordering = ['-criado_em']

    # representação textual do objeto (usado no admin e logs)
    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_tipo_display()})'