from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# importações de modelos e serializadores
from .models import Via
from apps.semaforos.models import Semaforo
from apps.ocorrencias.models import Ocorrencia
from .serializers import ViaSerializer
from apps.semaforos.serializers import SemaforoSerializer
from apps.ocorrencias.serializers import OcorrenciaSerializer


class MapaView(APIView):

    # o mapa atualiza a cada 30 segundos com esse decorator
    @method_decorator(cache_page(30))
    def get(self, request):
        vias = Via.objects.all()
        semaforos = Semaforo.objects.all()
        ocorrencias = Ocorrencia.objects.filter(
        status__in=['ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', 'ENCERRADA']
        )
        
        return Response({
            "vias": ViaSerializer(vias, many=True).data,
            "semaforos": SemaforoSerializer(semaforos, many=True).data,
            "ocorrencias": OcorrenciaSerializer(ocorrencias, many=True).data,
        })
