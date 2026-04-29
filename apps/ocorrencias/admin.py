from django.contrib import admin
from django.utils.html import format_html
from .models import Ocorrencia


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):

    # Campos somente leitura
    readonly_fields = ["criado_em", "atualizado_em"]

    # Otimiza as consultas ao banco de dados
    list_select_related = ["via", "semaforo", "usuario"]

    # Colunas exibidas na listagem
    list_display = [
        "id",
        "badge_tipo",
        "badge_status",
        "via",
        "usuario_link",
        "criado_em",
    ]

    list_filter = ["status", "tipo", "criado_em", "via"]

    # Pesquisa por descrição, nome da rua ou nome do usuário que relatou
    search_fields = ["descricao", "via__nome", "usuario__username", "usuario__first_name"]

    # Organiza pela data de criação
    ordering = ["-criado_em"]

    # Permite alterar a situação sem precisar entrar no detalhe da ocorrência
    list_editable = ["status"]

    # Formulário de edição
    fieldsets = (
        ("Informações do Incidente", {
            "fields": ("tipo", "status", "descricao", "usuario")
        }),
        ("Localização Detalhada", {
            "fields": ("via", "semaforo", "latitude", "longitude"),
            "description": "Selecione a via afetada ou o semáforo com defeito em Apodi."
        }),
        ("Registro de Tempo", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),
    )

    # Badge para o Tipo de Ocorrência
    def badge_tipo(self, obj):
        cores = {
            "ACIDENTE": ("#fee2e2", "#991b1b"),
            "SEMAFORO_DEFEITO": ("#ffedd5", "#9a3412"),
            "CONGESTIONAMENTO": ("#f3e8ff", "#6b21a8"),
            "OBRA": ("#fef9c3", "#854d0e"),
            "OUTRO": ("#f3f4f6", "#374151"),
        }
        bg, txt = cores.get(obj.tipo, ("#f3f4f6", "#374151"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg, txt, obj.get_tipo_display(),
        )
    badge_tipo.short_description = "Tipo"

    # Badge para o Status (Situação)
    def badge_status(self, obj):
        cores = {
            "ABERTA": ("#fef2f2", "#dc2626"),
            "EM_ANDAMENTO": ("#fffbeb", "#d97706"),
            "RESOLVIDA": ("#f0fdf4", "#16a34a"),
            "ENCERRADA": ("#f9fafb", "#4b5563"),
        }
        bg, txt = cores.get(obj.status, ("#f3f4f6", "#374151"))
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;'
            'border-radius:6px;font-size:10px;font-weight:bold;text-transform:uppercase">{}</span>',
            bg, txt, obj.get_status_display(),
        )
    badge_status.short_description = "Situação"

    # Exibe o usuário de forma mais amigável
    def usuario_link(self, obj):
        if obj.usuario:
            return obj.usuario.get_full_name() or obj.usuario.username
        return "Anônimo"
    usuario_link.short_description = "Relatado por"
