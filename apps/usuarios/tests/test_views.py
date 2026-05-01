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
        """Testa a criação do usuário no banco APÓS a confirmação do código"""

        # 1. Preparamos a sessão com os dados crus (Exatamente como a View espera)
        session = client.session
        session['usuario_verificando_id'] = True
        session['dados_registro_pendente'] = {
            'username': 'usuario_teste',
            'email': 'teste@email.com',
            'password': 'SenhaDificil123',
            'codigo': '123456'  # Código como STRING
        }
        session.save()

        # 2. Fazemos o POST para a URL correta
        url = reverse("apps.usuarios:verificar_codigo")
        # Enviamos o código como string
        response = client.post(url, {"codigo": "123456"})

        # 3. Se retornar 200 aqui, o print abaixo vai nos dizer o porquê no terminal
        if response.status_code == 200:
            msgs = [m.message for m in response.context['messages']]
            print(f"\n--- MENSAGEM DE ERRO DA VIEW: {msgs} ---")

        # 4. Verificações finais
        assert response.status_code == 302
        assert response.url == "/usuarios/login/"

        # Verifica se o usuário nasceu no banco de dados
        from django.contrib.auth import get_user_model
        User = get_user_model()
        assert User.objects.filter(username='usuario_teste').exists()
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
