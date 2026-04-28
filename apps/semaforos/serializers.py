from rest_framework import serializers
from .models import Semaforo

class SemaforoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semaforo
        fields = '__all__'