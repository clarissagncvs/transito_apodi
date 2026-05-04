from rest_framework import serializers
from .models import Ocorrencia


class OcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocorrencia
        fields = [
            "id",
            "tipo",
            "descricao",
            "status",
            "via",
            "semaforo",
            "latitude",
            "longitude",
            "usuario",
            "criado_em",
            "atualizado_em"
        ]
        read_only_fields = ["criado_em", "atualizado_em"]
