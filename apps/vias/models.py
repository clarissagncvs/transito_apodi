from django.db import models


class Via(models.Model):
    """Representa uma via pública monitorada pelo sistema."""

    # tipos de vias disponiveis
    class Tipo(models.TextChoices):
        AVENIDA = "AVENIDA", "Avenida"
        RUA = "RUA", "Rua"
        RODOVIA = "RODOVIA", "Rodovia"

    nome = models.CharField(max_length=150, verbose_name="nome da via")

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.RUA,
        verbose_name="tipo de via",
    )

    bairro = models.CharField(max_length=100, blank=True, verbose_name="bairro")

    # Coordenadas para integração com mapas
    latitude_inicial = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude_inicial = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    latitude_final = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude_final = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "via"
        verbose_name_plural = "vias"
        ordering = ["nome"]


def __str__(self):
    return f"{self.get_tipo_display()} {self.nome}"
