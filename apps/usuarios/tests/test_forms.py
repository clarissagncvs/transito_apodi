import pytest
from apps.usuarios.forms import RegistroForm, LoginForm
from apps.usuarios.models import Usuario

@pytest.mark.django_db
class TestUsuarioForms:

    def test_registro_form_valido(self):
        """Testa se o formulário aceita dados corretos"""
        dados = {
            "username": "joao_apodi",
            "first_name": "Joao",
            "last_name": "Silva",
            "email": "joao@email.com",
            "telefone": "84999998888",
            "password1": "Senha@Forte123!",
            "password2": "Senha@Forte123!",
        }
        form = RegistroForm(data=dados)
        if not form.is_valid():
            print(f"\nERROS DO FORM: {form.errors.as_json()}")
        assert form.is_valid() is True

    def test_registro_form_email_duplicado(self):
        """Garante que não permite cadastrar e-mail que já existe"""
        # Criamos um usuário prévio
        Usuario.objects.create_user(username="antigo", email="teste@email.com", password="123")
        
        dados = {
            "username": "novo",
            "email": "teste@email.com", # Email já em uso
            "password1": "senha123",
            "password2": "senha123",
        }
        form = RegistroForm(data=dados)
        
        assert form.is_valid() is False
        assert "Este e-mail já foi cadastrado" in form.errors["email"][0]

    def test_registro_form_telefone_invalido(self):
        """Testa a validação do Regex customizado no clean_telefone"""
        dados = {
            "username": "user_fone",
            "email": "fone@email.com",
            "telefone": "123",  # Formato muito curto
            "password1": "senha123",
            "password2": "senha123",
        }
        form = RegistroForm(data=dados)
        
        assert form.is_valid() is False
        assert "Formato inválido" in form.errors["telefone"][0]

    def test_login_form_campos_obrigatorios(self):
        """Verifica se o form de login exige os campos"""
        form = LoginForm(data={})
        assert form.is_valid() is False
        assert "username" in form.errors
        assert "password" in form.errors
