from rest_framework.viewsets import ModelViewSet 
from .models import Via
from .serializers import ViaSerializer

class ViaViewSet(ModelViewSet):
    queryset = Via.objects.all().order_by("id")
    serializer_class = ViaSerializer