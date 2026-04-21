from rest_framework import serializers
from .models import Usuario
from apps.usuarios.services.usuario_service import UsuarioService


# serializer principal para leitura de usuários
class UsuarioSerializer(serializers.ModelSerializer):
    # campo extra apenas para exibição do tipo (ex: "Administrador")
    tipo_display = serializers.CharField(
        source='get_tipo_display', read_only=True
    )

    class Meta:
        model  = Usuario
        # campos expostos na api
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefone', 'tipo', 'tipo_display',
            'is_active', 'criado_em'
        ]
        # campos somente leitura (não podem ser alterados via api)
        read_only_fields = ['criado_em']


# serializer usado apenas na criação de usuários
class UsuarioCreateSerializer(serializers.ModelSerializer):
    # senha principal (não retorna na api)
    password  = serializers.CharField(write_only=True, min_length=8)
    # confirmação de senha
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = Usuario
        # campos permitidos na criação
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'telefone', 'password', 'password2'
        ]

    # validação personalizada para garantir que as senhas coincidem
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password2': 'as senhas não coincidem.'
            })
        return data

    # criação do usuário delegada para a camada de serviço
    def create(self, validated_data):
        # remove confirmação de senha antes de criar
        validated_data.pop('password2')

        # chama o service (regra de negócio centralizada)
        return UsuarioService.criar_usuario(validated_data)