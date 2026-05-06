from django.db import models
from django.conf import settings
from apps.vias.models import Via
from apps.semaforos.models import Semaforo


class Ocorrencia(models.Model):
    """Registro de ocorrência de trânsito reportada por cidadão ou agente."""

    class Tipo(models.TextChoices):
        ACIDENTE = "ACIDENTE", "Acidente"
        SEMAFORO_DEFEITO = "SEMAFORO_DEFEITO", "Semáforo com Defeito"
        CONGESTIONAMENTO = "CONGESTIONAMENTO", "Congestionamento"
        OBRA = "OBRA", "Obra / Interdição"
        EVENTO = "EVENTO", "Evento"
        OUTRO = "OUTRO", "Outro"

    class Status(models.TextChoices):
        ABERTA = "ABERTA", "Aberta"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em Andamento"
        RESOLVIDA = "RESOLVIDA", "Resolvida"
        ENCERRADA = "ENCERRADA", "Encerrada"

    # Campos principais
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        verbose_name="Tipo de ocorrência"
    )
    descricao = models.TextField(verbose_name="Descrição")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTA,
        verbose_name="Situação"
    )

    # Localização
    via = models.ForeignKey(
        Via,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ocorrencias",
        verbose_name="Via/Rua"
    )
    semaforo = models.ForeignKey(
        Semaforo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ocorrencias",
        verbose_name="Semáforo relacionado"
    )

    # hora da ocorrencia
    horario_incidente = models.TimeField(
        verbose_name="Horário do ocorrido",
        null=True,
        blank=True
    )

    # Coordenadas (DecimalField é melhor para GPS)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ocorrencias_reportadas",
        verbose_name="Registrada por"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.get_tipo_display()} — {self.via}"
