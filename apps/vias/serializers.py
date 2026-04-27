from rest_framework import serializer
from .models import Via

class ViaSerializer(serializer.ModelSerializers):
    class Meta:
        model = Via
        fields = '__all__'