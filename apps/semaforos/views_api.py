from rest_framework.viewsets import ModelViewSet 
from .models import Semaforo
from .serializers import SemaforoSerializer

class SemaforoViewSet(ModelViewSet):
    queryset = Semaforo.objects.all().order_by("codigo")
    serializer_class = SemaforoSerializer