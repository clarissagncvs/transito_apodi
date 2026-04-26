import pytest
from django.core.exceptions import ValidationError
from apps.usuarios.services import UsuarioService


@pytest.mark.django_db  # Permite acesso ao banco de dados de teste
class TestUsuarioService:

    def test_deve_lancar_erro_se_senhas_forem_diferentes(self):
        # Dados de entrada inválidos
        dados = {
            "username": "jose",
            "email": "jose@email.com",
            "password1": "senha123",
            "password2": "senha_diferente"
        }

        # Verifica se a exceção correta é levantada
        with pytest.raises(ValidationError) as excinfo:
            UsuarioService.criar_usuario(dados)

        assert "as senhas não coincidem" in str(excinfo.value)

    def test_criar_usuario_com_sucesso(self, mailoutbox):
        dados = {
            "username": "maria",
            "email": "maria@email.com",
            "password1": "senha123",
            "password2": "senha123"
        }

        usuario = UsuarioService.criar_usuario(dados)

        # Verificações (Assertions)
        assert usuario.username == "maria"
        assert usuario.is_active is False
        assert len(mailoutbox) == 1  # Verifica se o e-mail foi enviado
