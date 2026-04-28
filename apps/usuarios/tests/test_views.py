import pytest
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario


@pytest.mark.django_db
class TestUsuarioViews:

    def test_acesso_home_exige_login(self, client): # Mudei o nome para fazer sentido
        url = reverse('home')
        response = client.get(url)
        
        # O teste agora passa se houver um redirecionamento
        assert response.status_code == 302
        # Opcional: verificar se ele está mandando para a página de login
        assert '/login/' in response.url

    def test_login_com_sucesso(self, client):
        """Testa o fluxo completo de login"""
        # Criamos o usuário no banco
        user = Usuario.objects.create_user(username="jose", password="123")
        url = "/usuarios/login/"

        # Simula o POST do formulário
        response = client.post(url, {"username": "jose", "password": "123"})
        assert int(client.session['_auth_user_id']) == user.id

        # Após login, deve redirecionar para a home
        assert response.status_code == 302
        assert response.url == reverse("home")

    def test_logout_redireciona_para_login(self, client):
        """Testa se o logout encerra a sessão corretamente"""
        url = reverse("apps.usuarios:logout")
        response = client.get(url)
        assert response.status_code == 302
        assert "login" in response.url

    def test_bloqueio_usuario_comum_em_area_admin(self, client):
        """Garante que usuários comuns recebam 403 (PermissionDenied) na lista de usuários"""
        # Criamos um cidadão comum
        user = Usuario.objects.create_user(username="cidadao", password="123", tipo="CIDADAO")
        client.force_login(user)  # Loga o usuário

        url = reverse("usuarios:lista")
        response = client.get(url)

        # O decorator admin_required deve subir um PermissionDenied (403)
        assert response.status_code == 403

    def test_acesso_admin_na_lista_usuarios(self, client):
        """Garante que o administrador consiga ver a lista"""
        # Criamos um admin
        admin = Usuario.objects.create_user(username="admin", password="123", tipo="ADMIN")
        client.force_login(admin)

        url = reverse("usuarios:lista")
        response = client.get(url)

        assert response.status_code == 200
        assert "page_obj" in response.context  # Verifica se enviou a lista pro template

    def test_verificacao_codigo_fluxo(self, client):
        """Testa o preenchimento do código de ativação"""
        user = Usuario.objects.create_user(
            username="new_user",
            codigo_verificacao="123456",
            codigo_expira_em=timezone.now() + timezone.timedelta(hours=1),
            is_active=False
        )

        # Colocamos o ID na sessão simulando o fluxo do registro
        session = client.session
        session['usuario_verificando_id'] = user.id
        session.save()

        url = reverse("usuarios:verificar_codigo")
        response = client.post(url, {"codigo": "123456"})

        user.refresh_from_db()
        assert user.is_active is True
        assert response.status_code == 302  # Redireciona para login
