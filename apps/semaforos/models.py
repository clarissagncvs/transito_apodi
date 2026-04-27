from django.db import models
from vias.models import Via


class Semaforo(models.Model):
    """Representa um semáforo físico instalado em uma via."""

    class Status(models.TextChoices):
        VERDE = "VERDE", "Verde"
        AMARELO = "AMARELO", "Amarelo"
        VERMELHO = "VERMELHO", "Vermelho"
        APAGADO = "APAGADO", "Apagado"
        MANUTENCAO = "MANUTENCAO", "Em Manutenção"

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="código do semáforo",
        help_text="Código único de identificação",
    )

    via = models.ForeignKey(
        Via,
        on_delete=models.PROTECT,
        related_name="semaforos",
        verbose_name="via",
    )

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.VERDE,
        verbose_name="status atual",
    )

    ativo = models.BooleanField(default=True, verbose_name="ativo")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "semáforo"
        verbose_name_plural = "semáforos"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} ({self.get_status_display()}) — {self.via}"
    # Localização
    via = models.ForeignKey(
        Via,
        on_delete=models.PROTECT,
        related_name="semaforos",
        verbose_name="via",
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    # Status atual
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.VERDE,
        verbose_name="status atual",
    )
    ativo = models.BooleanField(default=True, verbose_name="ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "semáforo"
        verbose_name_plural = "semáforos"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} ({self.get_status_display()}) — {self.via}"
