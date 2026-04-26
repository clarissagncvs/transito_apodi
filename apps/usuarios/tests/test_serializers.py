import pytest
from apps.usuarios.serializers import UsuarioSerializer, UsuarioCreateSerializer
from apps.usuarios.models import Usuario

@pytest.mark.django_db
class TestUsuarioSerializers:

    def test_usuario_serializer_saida_correta(self):
        """Verifica se o serializer de leitura entrega o tipo_display correto"""
        usuario = Usuario.objects.create(
            username="agente_apodi", 
            tipo="AGENTE", 
            first_name="Marcos"
        )
        serializer = UsuarioSerializer(instance=usuario)
        
        # O campo 'tipo_display' deve vir do get_tipo_display do model
        assert serializer.data["tipo_display"] == "Agente de Trânsito"
        assert serializer.data["username"] == "agente_apodi"

    def test_usuario_create_serializer_validacao_senhas(self):
        """Verifica se o serializer da API barra senhas diferentes"""
        dados_invalidos = {
            "username": "novo_user",
            "email": "novo@email.com",
            "password": "senha123",
            "password2": "senha_errada"
        }
        serializer = UsuarioCreateSerializer(data=dados_invalidos)
        
        assert serializer.is_valid() is False
        assert "password2" in serializer.errors
        assert "as senhas não coincidem" in str(serializer.errors["password2"][0])

    def test_usuario_create_serializer_senha_muito_curta(self):
        """Verifica se o min_length=8 da senha é respeitado"""
        dados = {
            "username": "user",
            "password": "123", # Curta demais
            "password2": "123"
        }
        serializer = UsuarioCreateSerializer(data=dados)
        assert serializer.is_valid() is False
        assert "password" in serializer.errors

    def test_usuario_create_serializer_chama_service(self, mocker):
        """
        Garante que o serializer chama o UsuarioService.criar_usuario.
        Usamos 'mocker' para não criar um usuário real no banco aqui.
        """
        # Mockamos o service para apenas verificar se ele foi chamado
        mock_service = mocker.patch("apps.usuarios.services.usuario_service.UsuarioService.criar_usuario")
        
        dados_validos = {
            "username": "api_user",
            "email": "api@email.com",
            "password": "password123",
            "password2": "password123"
        }
        
        serializer = UsuarioCreateSerializer(data=dados_validos)
        if serializer.is_valid():
            serializer.save()

        # Verifica se o serializer passou os dados para o service corretamente
        assert mock_service.called
