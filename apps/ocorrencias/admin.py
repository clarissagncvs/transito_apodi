from django.contrib import admin
from django.utils.html import format_html
from .models import Ocorrencia


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):

    # Campos somente leitura
    readonly_fields = ["criado_em", "atualizado_em"]

    # Otimiza as consultas para não pesar no banco de dados (especialmente SQLite)
    list_select_related = ["via", "semaforo", "usuario"]

    list_display = [
        "id",
        "badge_tipo",
        "status",
        "badge_status",
        "via",
        "usuario_link",
        "criado_em",
    ]

    list_editable = ["status"]

    # Filtros laterais
    list_filter = ["status", "tipo", "criado_em", "via"]

    search_fields = ["descricao", "via__nome", "usuario__username"]

    ordering = ["-criado_em"]

    fieldsets = (
        ("Informações do Incidente", {
            "fields": ("tipo", "status", "descricao", "usuario", "horario_incidente")
        }),
        ("Localização Detalhada", {
            "fields": ("via", "semaforo", "latitude", "longitude"),
        }),
        ("Registro de Tempo", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),

    )

    # Badge para o Tipo (Acidente, Obra, etc)
    def badge_tipo(self, obj):
        cores = {
            "ACIDENTE": ("#fee2e2", "#991b1b"),
            "SEMAFORO_DEFEITO": ("#ffedd5", "#9a3412"),
            "CONGESTIONAMENTO": ("#f3e8ff", "#6b21a8"),
            "OBRA": ("#fef9c3", "#854d0e"),
            "EVENTO": ("#2797c4ff", "#868685c1"),
            "OUTRO": ("#f3f4f6", "#374151"),
        }
        bg, txt = cores.get(obj.tipo, ("#f3f4f6", "#374151"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg, txt, obj.get_tipo_display()
        )
    badge_tipo.short_description = "Tipo"

    # Badge Visual para a Situação (Apenas leitura)
    def badge_status(self, obj):
        cores = {
            "ABERTA": ("#fef2f2", "#dc2626"),
            "EM_ANDAMENTO": ("#fffbeb", "#d97706"),
            "RESOLVIDA": ("#f0fdf4", "#16a34a"),
            "ENCERRADA": ("#f9fafb", "#000000"),
        }
        bg, txt = cores.get(obj.status, ("#f3f4f6", "#374151"))
        return format_html(
            '<div style="width:12px;height:12px;border-radius:50%;'
            'background:{};display:inline-block;margin-right:5px"></div>',
            txt
        )
    badge_status.short_description = "Status Visual"

    def usuario_link(self, obj):
        if obj.usuario:
            return obj.usuario.get_full_name() or obj.usuario.username
        return "Anônimo"
    usuario_link.short_description = "Relatado por"
