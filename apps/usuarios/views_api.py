# Django REST Framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# locais
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer


class UsuarioViewSet(ModelViewSet):
    """
    API para gerenciamento de usuários
    """
    queryset = Usuario.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]

    # define serializer dinamicamente
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer