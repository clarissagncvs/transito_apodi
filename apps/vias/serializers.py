from rest_framework import serializers
from .models import Via

class ViaSerializer(serializers.ModelSerializers):
    class Meta:
        model = Via
        fields = '__all__'