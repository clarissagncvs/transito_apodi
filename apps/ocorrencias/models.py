from django.db import models
from django.conf import settings
from apps.vias.models import Via
from apps.semaforos.models import Semaforo

<<<<<<< models_afins

class Ocorrencia(models.Model):
    """Registro de ocorrência de trânsito reportada por cidadão ou agente."""

    class Tipo(models.TextChoices):
        ACIDENTE = "ACIDENTE", "Acidente"
        SEMAFORO_DEFEITO = "SEMAFORO_DEFEITO", "Semáforo com Defeito"
        CONGESTIONAMENTO = "CONGESTIONAMENTO", "Congestionamento de via"
        OBRA = "OBRA", "Obra na Via"
        OUTRO = "OUTRO", "Outro"

    class Situacao(models.TextChoices):
        ABERTA = "ABERTA", "Aberta"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em Andamento"
        RESOLVIDA = "RESOLVIDA", "Resolvida"
        CANCELADA = "CANCELADA", "Cancelada"

    # Tipo e descrição
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        verbose_name="tipo de ocorrência",
    )

    descricao = models.TextField(verbose_name="descrição")

    # Situação atual
    situacao = models.CharField(
        max_length=15,
        choices=Situacao.choices,
        default=Situacao.ABERTA,
        verbose_name="situação",
    )

    # Localização — via é obrigatória; semáforo é opcional
    via = models.ForeignKey(
        Via,
        on_delete=models.PROTECT,
        related_name="ocorrencias",
        verbose_name="via",
    )

    semaforo = models.ForeignKey(
        Semaforo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ocorrencias",
        verbose_name="semáforo relacionado",
    )

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # Quem reportou (cidadão ou agente)
    reportado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ocorrencias_reportadas",
        verbose_name="reportado por",
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ocorrência"
        verbose_name_plural = "ocorrências"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"[{self.get_situacao_display()}] {self.get_tipo_display()} — {self.via} ({self.criado_em:%d/%m/%Y})"
=======
from django.db import models
from django.conf import settings
from apps.vias.models import Via

class Ocorrencia(models.Model):
    class Tipo(models.TextChoices):
        ACIDENTE        = 'ACIDENTE',        'Acidente'
        CONGESTIONAMENTO= 'CONGESTIONAMENTO', 'Congestionamento'
        BURACO          = 'BURACO',          'Buraco na via'
        SEMAFORO        = 'SEMAFORO',        'Semáforo com defeito'
        ALAGAMENTO      = 'ALAGAMENTO',      'Alagamento'
        OBRA            = 'OBRA',            'Obra / interdição'

#o ciclo de status de uma ocorrência(aberta->em atendimento->fechada)
    class Status(models.TextChoices):
        ABERTA         = 'ABERTA',         'Aberta'
        EM_ATENDIMENTO = 'EM_ATENDIMENTO', 'Em atendimento'
        ENCERRADA      = 'ENCERRADA',      'Encerrada'

#define o tipo de ocorrência e o usuário dá detalhes da situação
    tipo      = models.CharField(
        max_length=20, 
        choices=Tipo.choices)
    verbose_name='Tipo de ocorrência',
    descricao = models.TextField()
    status    = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ABERTA
    )

    #detalha em qual via está a ocorrência
    via = models.ForeignKey(
        Via, 
        on_delete=models.SET_NULL,
        null=True,
        verbose_name = 'Via/Rua'
    )
    
    #Detalhes do usuário que fez a ocorrência
    usuario   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
        verbose_name = 'Registrada por'
    )
#informa a localização da via com ocorrências
    latitude  = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

#imagem e data/hora da via com ocorrência
    foto      = models.ImageField(upload_to='ocorrencias/', blank=True, verbose_name= 'Foto da ocorrência')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
    #nome amigável no admin
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'
    # Ordena as ocorrências da mais recente para a mais antiga
        ordering = ['-criado_em']
    #representação textual de quando se 'imprime' uma ocorrência
    def __str__(self):
        return f'{self.get_tipo_display()} - {self.get_status_display()}'
>>>>>>> master
