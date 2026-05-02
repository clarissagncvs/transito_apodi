from rest_framework import serializers
from .models import Via


class ViaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Via
        fields = [
            "id",
            "tipo",
            "nome",
            "bairro",
            "latitude_inicial",
            "longitude_inicial",
            "latitude_final",
            "longitude_final",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["criado_em", "atualizado_em"]
