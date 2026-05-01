import pytest
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario

# ==============================================================================
# FIXTURES GLOBAIS
# ==============================================================================


@pytest.fixture
def admin_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='admin_test',
        password='password123',
        email='admin@teste.com',
        tipo="ADMIN",
        is_staff=True  # Importante para certas verificações de admin
    )


@pytest.fixture
def common_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='joao',
        password='password123',
        email='joao@teste.com',
        tipo='CIDADAO'
    )


@pytest.fixture
def other_user(db, django_user_model):
    """Cria um segundo usuário comum para testes de invasão de privacidade"""
    return django_user_model.objects.create_user(
        username='maria',
        password='password123',
        email='maria@teste.com',
        tipo='CIDADAO'
    )

# ==============================================================================
# TESTES DE AUTENTICAÇÃO E ACESSO GERAL
# ==============================================================================


@pytest.mark.django_db
class TestUsuarioViews:

    def test_acesso_home_com_usuario_logado(self, client, common_user):
        client.force_login(common_user)
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_login_com_sucesso(self, client, db):
        user = Usuario.objects.create_user(username="jose", password="123")
        url = "/usuarios/login/"
        response = client.post(url, {"username": "jose", "password": "123"})
        assert int(client.session['_auth_user_id']) == user.id
        assert response.status_code == 302

    def test_verificacao_codigo_fluxo(self, client, db):
        """Testa ativação via UsuarioService (chamado pela view)"""
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
        assert response.status_code == 302

        user.refresh_from_db()
        assert user.is_active is True
        # Verifica se limpou a sessão após sucesso
        assert 'usuario_verificando_id' not in client.session

# ==============================================================================
# NOVOS: TESTES DE EDIÇÃO DE PERFIL (NOME E E-MAIL)
# ==============================================================================


@pytest.mark.django_db
class TestEdicaoPerfilUsuario:

    def test_usuario_pode_editar_proprio_nome(self, client, common_user):
        client.force_login(common_user)
        url = reverse('apps.usuarios:editar_usuario', kwargs={'pk': common_user.pk})
        response = client.post(url, {'username': 'joao_novo_nome'})

        common_user.refresh_from_db()
        assert common_user.username == 'joao_novo_nome'
        assert response.status_code == 302

    def test_usuario_pode_editar_proprio_email(self, client, common_user):
        client.force_login(common_user)
        url = reverse('apps.usuarios:editar_email', kwargs={'pk': common_user.pk})
        response = client.post(url, {'email': 'novo@email.com'})

        common_user.refresh_from_db()
        assert common_user.email == 'novo@email.com'
        assert response.status_code == 302

    def test_bloqueio_edicao_de_perfil_alheio(self, client, common_user, other_user):
        """Segurança: João não pode editar o perfil da Maria"""
        client.force_login(common_user)
        # Tenta acessar a URL de edição da Maria
        url = reverse('apps.usuarios:editar_usuario', kwargs={'pk': other_user.pk})
        response = client.get(url)

        # Deve retornar 403 Forbidden devido à nossa trava na view
        assert response.status_code == 403

# ==============================================================================
# TESTES DE ADMINISTRAÇÃO
# ==============================================================================


@pytest.mark.django_db
class TestAdminViews:

    def test_busca_binaria_na_lista_admin(self, client, admin_user, common_user):
        """Verifica se o termo de busca funciona na listagem"""
        client.force_login(admin_user)
        url = reverse("apps.usuarios:lista")
        response = client.get(url, {'q': 'joao'})

        assert response.status_code == 200
        # O usuário 'joao' deve estar presente no contexto da página
        usuarios_na_pagina = response.context['page_obj'].object_list
        assert any(u.username == 'joao' for u in usuarios_na_pagina)

    def test_admin_altera_qualquer_usuario(self, client, admin_user, common_user):
        """Admin usa UsuarioAdminForm para mudar tipo de outro user"""
        client.force_login(admin_user)
        url = reverse('apps.usuarios:editar', kwargs={'pk': common_user.pk})
        dados = {
            'username': 'joao',
            'email': 'joao@teste.com',
            'tipo': 'AGENTE'
        }
        client.post(url, data=dados)
        common_user.refresh_from_db()
        assert common_user.tipo == 'AGENTE'
