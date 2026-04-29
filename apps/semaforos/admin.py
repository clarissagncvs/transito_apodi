from django.contrib import admin
from django.utils.html import format_html
from .models import Semaforo


@admin.register(Semaforo)
class SemaforoAdmin(admin.ModelAdmin):

    # Otimização de consulta para a Via relacionada
    list_select_related = ["via"]

    list_display = [
        "codigo",
        "via",
        "badge_status",
        "status",  # Campo original para edição rápida
        "ativo",
        "atualizado_em",
    ]

    # Permite alterar o status e ativar/desativar direto na lista
    list_editable = ["status", "ativo"]

    # Filtros e buscas
    list_filter = ["status", "ativo", "via"]
    search_fields = ["codigo", "via__nome"]

    # Organização do formulário
    fieldsets = (
        ("Identificação Técnica", {
            "fields": ("codigo", "ativo")
        }),
        ("Estado do Dispositivo", {
            "fields": ("status", "via")
        }),
        ("Geolocalização", {
            "fields": ("latitude", "longitude"),
            "classes": ("collapse",)
        }),
        ("Metadados", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),
    )

    def badge_status(self, obj):
        cores = {
            "VERDE": ("#dcfce7", "#15803d"),
            "AMARELO": ("#fef9c3", "#854d0e"),
            "VERMELHO": ("#fee2e2", "#991b1b"),
            "APAGADO": ("#f3f4f6", "#374151"),
            "MANUTENCAO": ("#fef3c7", "#92400e"),
        }

        bg, txt = cores.get(obj.status, ("#f3f4f6", "#374151"))

        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg, txt, obj.get_status_display(),
        )

    badge_status.short_description = "Sinalização Atual"
