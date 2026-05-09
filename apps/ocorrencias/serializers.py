from rest_framework import serializers
from .models import Ocorrencia
from apps.vias.serializers import ViaSerializer


class OcorrenciaSerializer(serializers.ModelSerializer):
    via_detalhe = ViaSerializer(source='via', read_only=True)

    class Meta:
        model = Ocorrencia
        fields = [
            "id",
            "tipo",
            "descricao",
            "status",
            "via",
            "via_detalhe",
            "semaforo",
            "latitude",
            "longitude",
            "usuario",
            "horario_incidente",
            "criado_em",
            "atualizado_em"
        ]

    read_only_fields = ["criado_em", "atualizado_em"]
