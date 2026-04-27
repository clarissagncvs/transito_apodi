from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Via
from .serializers import ViaSerializer

class ViaViews(APIView):
    def get(self, request):
        vias = Via.objects.all()
        serializer = ViaSerializer(vias, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ViaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)