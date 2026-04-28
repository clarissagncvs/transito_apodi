from rest_framework.viewsets import ModelViewSet 
from .models import Ocorrencia
from .serializers import OcorrenciaSerializer

class ViaViewSet(ModelViewSet):
    queryset = Ocorrencia.objects.all().order_by("id")
    serializer_class = OcorrenciaSerializer