from django.db import models
from django.conf import settings
from vias.models import Via
from semaforos.models import Semaforo
 
 
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
