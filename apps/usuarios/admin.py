from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Usuario


# registra o model usuario no admin com customizações
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    # campos somente leitura (não podem ser editados)
    readonly_fields = ['criado_em']

    # otimiza consultas quando houver relacionamentos (boa prática)
    list_select_related = True

    # colunas exibidas na listagem do admin
    list_display = [
        'username', 'nome_completo', 'email',
        'badge_tipo', 'telefone', 'is_active', 'criado_em'
    ]

    # filtros laterais no admin
    list_filter = ['tipo', 'is_active', 'criado_em']

    # campos pesquisáveis no topo
    search_fields = ['username', 'first_name', 'last_name', 'email']

    # ordenação padrão (mais recentes primeiro)
    ordering = ['-criado_em']

    # permite edição rápida direto na lista
    list_editable = ['is_active']

    # adiciona campos personalizados na edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        ('trânsito apodi', {
            'fields': ('tipo', 'telefone', 'foto')
        }),
    )

    # adiciona campos extras ao criar novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('trânsito apodi', {
            'fields': ('tipo', 'telefone', 'foto')
        }),
    )

    # método para exibir nome completo (fallback para username)
    def nome_completo(self, obj):
        return obj.get_full_name() or '—'
    nome_completo.short_description = 'nome completo'

    # exibe um badge colorido baseado no tipo de usuário
    def badge_tipo(self, obj):
        cores = {
            'CIDADAO': ('#dcfce7', '#15803d'),
            'AGENTE':  ('#dbeafe', '#1d4ed8'),
            'ADMIN':   ('#fef3c7', '#92400e'),
        }

        # define cor padrão caso não encontre o tipo
        bg, txt = cores.get(obj.tipo, ('#f3f4f6', '#374151'))

        # retorna html seguro com estilo inline
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg, txt, obj.get_tipo_display()
        )
    badge_tipo.short_description = 'tipo'