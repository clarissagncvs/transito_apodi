from django.contrib import admin
from django.utils.html import format_html
from .models import Via


@admin.register(Via)
class ViaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'badge_tipo', 'bairro', 'coordenadas_formatadas')

    list_filter = ('tipo', 'bairro')
    search_fields = ('nome', 'bairro')

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'bairro')
        }),
        ('Geolocalização (Início da Via)', {
            'fields': ('latitude_inicial', 'longitude_inicial'),
            'classes': ('collapse',),
            'description': 'Coordenadas de onde a via começa.'
        }),
        ('Geolocalização (Fim da Via)', {
            'fields': ('latitude_final', 'longitude_final'),
            'classes': ('collapse',),
            'description': 'Coordenadas de onde a via termina.'
        }),
    )

    def badge_tipo(self, obj):
        cores = {
            "RUA": ("#dcfce7", "#15803d"),
            "AVENIDA": ("#dbeafe", "#1d4ed8"),
            "RODOVIA": ("#fef3c7", "#92400e"),
        }

        bg, txt = cores.get(obj.tipo, ("#f3f4f6", "#374151"))

        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg,
            txt,
            obj.get_tipo_display(),
        )

    badge_tipo.short_description = "Tipo de Via"

    def coordenadas_formatadas(self, obj):
        if obj.latitude_inicial and obj.longitude_inicial:
            return f"📍 Início: {obj.latitude_inicial} / {obj.longitude_inicial}"
        return "Sem coordenadas"

    coordenadas_formatadas.short_description = "Coordenadas"
