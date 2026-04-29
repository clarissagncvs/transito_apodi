import pytest
from django.urls import reverse
from django.utils import timezone
from django.core import mail
from apps.usuarios.models import Usuario

# ==============================================================================
# FIXTURES GLOBAIS
# Estas funções criam os dados base que serão usados por todas as classes abaixo.
# ==============================================================================


@pytest.fixture
def admin_user(db, django_user_model):
    """Cria um usuário administrador para os testes"""
    return django_user_model.objects.create_user(
        username='admin_test',
        password='password123',
        email='admin@teste.com',
        tipo="ADMIN"
    )


@pytest.fixture
def common_user(db, django_user_model):
    """Cria um usuário comum (Cidadão)"""
    return django_user_model.objects.create_user(
        username='joao',
        password='password123',
        email='joao@teste.com',
        tipo='CIDADAO'
    )

# ==============================================================================
# TESTES DE AUTENTICAÇÃO E ACESSO GERAL
# ==============================================================================


@pytest.mark.django_db
class TestUsuarioViews:

    def test_acesso_home_com_usuario_logado(self, client, common_user):
        """Verifica se a home carrega para usuário autenticado"""
        client.force_login(common_user)
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_login_com_sucesso(self, client, db):
        """Testa o fluxo completo de login via POST"""
        user = Usuario.objects.create_user(username="jose", password="123")
        url = "/usuarios/login/"
        response = client.post(url, {"username": "jose", "password": "123"})

        assert int(client.session['_auth_user_id']) == user.id
        assert response.status_code == 302
        assert response.url == reverse("home")

    def test_logout_redireciona_para_login(self, client):
        """Testa se o logout encerra a sessão corretamente"""
        url = reverse("apps.usuarios:logout")
        response = client.get(url)
        assert response.status_code == 302
        assert "login" in response.url

    def test_bloqueio_usuario_comum_em_area_admin(self, client, common_user):
        """Garante que usuários comuns recebam 403 na lista de usuários"""
        client.force_login(common_user)
        url = reverse("apps.usuarios:lista")
        response = client.get(url)
        assert response.status_code == 403

    def test_acesso_admin_na_lista_usuarios(self, client, admin_user):
        """Garante que o administrador consiga ver a lista"""
        client.force_login(admin_user)
        url = reverse("apps.usuarios:lista")
        response = client.get(url)
        assert response.status_code == 200
        assert "page_obj" in response.context

    def test_verificacao_codigo_fluxo(self, client, db):
        """Testa o preenchimento do código de ativação de conta"""
        user = Usuario.objects.create_user(
            username="new_user",
            codigo_verificacao="123456",
            codigo_expira_em=timezone.now() + timezone.timedelta(hours=1),
            is_active=False
        )
        session = client.session
        session['usuario_verificando_id'] = user.id
        session.save()

        url = reverse("apps.usuarios:verificar_codigo")
        response = client.post(url, {"codigo": "123456"})

        user.refresh_from_db()
        assert user.is_active is True
        assert response.status_code == 302

# ==============================================================================
# TESTES DE EDIÇÃO DE NÍVEL DE ACESSO (ADMIN)
# ==============================================================================


@pytest.mark.django_db
class TestEditarTipoUsuarioView:

    def test_deve_carregar_formulario_corretamente_para_admin(self, client, admin_user, common_user):
        """Verifica se o formulário de edição abre para o admin"""
        client.login(username='admin_test', password='password123')
        url = reverse('apps.usuarios:editar', kwargs={'pk': common_user.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert common_user.username in response.content.decode()

    def test_deve_alterar_tipo_usuario_com_sucesso(self, client, admin_user, common_user):
        """Verifica se a alteração de tipo é salva no banco"""
        client.login(username='admin_test', password='password123')
        url = reverse('apps.usuarios:editar', kwargs={'pk': common_user.pk})
        dados = {
            'username': common_user.username,
            'email': common_user.email,
            'tipo': 'AGENTE'
        }
        response = client.post(url, data=dados)
        assert response.status_code == 302
        common_user.refresh_from_db()
        assert common_user.tipo == 'AGENTE'

    def test_usuario_comum_nao_pode_acessar_edicao(self, client, common_user):
        """Bloqueia usuários não-admin de acessarem a edição de outros"""
        client.force_login(common_user)
        url = reverse('apps.usuarios:editar', kwargs={'pk': common_user.pk})
        response = client.get(url)
        assert response.status_code == 403

# ==============================================================================
# TESTES DE SOLICITAÇÃO DE MUDANÇA (E-MAIL)
# ==============================================================================


@pytest.mark.django_db
class TestSolicitarMudancaTipoView:

    def test_solicitacao_envia_email_para_admins(self, client, common_user, admin_user):
        """Verifica se o e-mail de solicitação é disparado"""
        client.force_login(common_user)
        url = reverse('apps.usuarios:solicitar_mudanca')
        response = client.get(url)  # Ajustado para GET conforme o link do perfil

        assert response.status_code == 302
        assert len(mail.outbox) == 1
        assert admin_user.email in mail.outbox[0].to
        assert common_user.username in mail.outbox[0].body

    def test_solicitacao_exibe_mensagem_de_sucesso(self, client, common_user, admin_user):
        """Verifica se a mensagem de confirmação aparece na tela"""
        client.force_login(common_user)
        url = reverse('apps.usuarios:solicitar_mudanca')
        response = client.get(url, follow=True)

        messages = [m.message for m in response.context['messages']]
        assert any("enviada com sucesso" in m.lower() for m in messages)
