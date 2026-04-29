from django.contrib import admin
from django.utils.html import format_html
from .models import Via

# Registra o model Via no admin com customizações


@admin.register(Via)
class ViaAdmin(admin.ModelAdmin):

    # Colunas exibidas na listagem principal do admin
    list_display = [
        "nome",
        "badge_tipo",
        "bairro",
        "coordenadas_formatadas",
    ]

    list_filter = ["tipo", "bairro"]

    search_fields = ["nome", "bairro"]

    ordering = ["nome"]

    # Organização visual dos campos ao adicionar ou editar uma via
    fieldsets = (
        ("Identificação da Via", {
            "fields": ("nome", "tipo", "bairro")
        }),
        ("Integração de Mapas (Geolocalização)", {
            "fields": ("latitude", "longitude"),
            "description": "Insira as coordenadas exatas para exibição no mapa de monitoramento."
        }),
    )

    # Exibe um badge baseado no tipo da via
    def badge_tipo(self, obj):
        cores = {
            "RUA": ("#dcfce7", "#15803d"),
            "AVENIDA": ("#dbeafe", "#1d4ed8"),
            "RODOVIA": ("#fef3c7", "#92400e"),
        }

        # Define cor padrão cinza caso não encontre o tipo (fallback seguro)
        bg, txt = cores.get(obj.tipo, ("#f3f4f6", "#374151"))

        # Retorna HTML seguro com estilo inline
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg,
            txt,
            obj.get_tipo_display(),
        )

    badge_tipo.short_description = "Tipo de Via"

    # Formata a Latitude e a Longitude em uma unica linha para deixar mais limpo
    def coordenadas_formatadas(self, obj):
        if obj.latitude and obj.longitude:
            return f"Lat: {obj.latitude} / Lon: {obj.longitude}"
        return "Sem coordenadas"

    coordenadas_formatadas.short_description = "Coordenadas"
