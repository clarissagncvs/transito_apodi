import pytest
from apps.usuarios.models import Usuario


@pytest.mark.django_db
class TestUsuarioModel:

    def test_deve_retornar_representacao_string_correta(self):
        """Testa o método __str__ do modelo"""
        usuario = Usuario.objects.create(
            username="lucas_apodi",
            first_name="Lucas",
            tipo="AGENTE"
        )
        # O esperado é: Nome (Tipo amigável)
        assert str(usuario) == "Lucas (Agente de Trânsito)"

    def test_propriedades_de_tipo_devem_ser_booleanas_corretas(self):
        """Testa as propriedades is_agente e is_admin_transito"""
        agente = Usuario(username="agente01", tipo=Usuario.Tipo.AGENTE)
        admin = Usuario(username="admin01", tipo=Usuario.Tipo.ADMIN)
        cidadao = Usuario(username="user01", tipo=Usuario.Tipo.CIDADAO)

        assert agente.is_agente is True
        assert agente.is_admin_transito is False
        assert admin.is_admin_transito is True
        assert admin.is_agente is False

        assert cidadao.is_agente is False
        assert cidadao.is_admin_transito is False

    def test_valor_default_tipo_deve_ser_cidadao(self):
        """Verifica se o tipo padrão é CIDADAO ao criar novo usuário"""
        usuario = Usuario.objects.create(username="novo_user")
        assert usuario.tipo == Usuario.Tipo.CIDADAO
