import pytest
from django.contrib.admin.sites import AdminSite
from apps.usuarios.models import Usuario
from apps.usuarios.admin import UsuarioAdmin

@pytest.mark.django_db
class TestUsuarioAdmin:

    @pytest.fixture
    def admin_site(self):
        return AdminSite()

    @pytest.fixture
    def usuario_admin(self, admin_site):
        return UsuarioAdmin(Usuario, admin_site)

    def test_nome_completo_exibe_fallback_quando_vazio(self, usuario_admin):
        """Verifica se exibe '—' quando o usuário não tem nome preenchido"""
        user = Usuario.objects.create(username="test_user")
        assert usuario_admin.nome_completo(user) == "—"

    def test_nome_completo_exibe_nome_corretamente(self, usuario_admin):
        """Verifica se exibe o nome completo corretamente"""
        user = Usuario.objects.create(username="test_user", first_name="Jose", last_name="Apodi")
        assert usuario_admin.nome_completo(user) == "Jose Apodi"

    def test_badge_tipo_retorna_html_valido(self, usuario_admin):
        """Verifica se o badge de tipo gera a tag span com as cores corretas"""
        user_admin = Usuario.objects.create(username="admin_user", tipo="ADMIN")
        user_agente = Usuario.objects.create(username="agente_user", tipo="AGENTE")
        
        html_admin = usuario_admin.badge_tipo(user_admin)
        html_agente = usuario_admin.badge_tipo(user_agente)

        # Verifica se as cores definidas no seu admin.py aparecem no HTML
        assert "background:#fef3c7" in html_admin  # Cor de fundo do ADMIN
        assert "background:#dbeafe" in html_agente # Cor de fundo do AGENTE
        assert "font-weight:600" in html_admin

    def test_configuracao_admin_campos_listados(self, usuario_admin):
        """Verifica se as colunas configuradas no list_display estão corretas"""
        campos_esperados = [
            "username", "nome_completo", "email", 
            "badge_tipo", "telefone", "is_active", "criado_em"
        ]
        for campo in campos_esperados:
            assert campo in usuario_admin.list_display
