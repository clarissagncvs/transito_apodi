from rest_framework import serializers
from .models import Semaforo


class SemaforoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semaforo
        fields = [
            "id",
            "codigo",
            "via",
            "latitude",
            "longitude",
            "status",
            "ativo",
            "criado_em",
            "atualizado_em"
        ]
        read_only_fields = ["criado_em", "atualizado_em"]
