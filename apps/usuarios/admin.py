from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    readonly_fields = ["criado_em"]
    list_select_related = True

    list_display = [
        "username",
        "nome_completo",
        "email",
        "badge_tipo",
        "is_active",
        "criado_em",
    ]

    list_filter = ["tipo", "is_active", "criado_em"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering = ["-criado_em"]
    list_editable = ["is_active"]

    fieldsets = UserAdmin.fieldsets + (
        ("trânsito apodi", {"fields": ("tipo",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("trânsito apodi", {"fields": ("tipo",)}),
    )

    def nome_completo(self, obj):
        return obj.get_full_name() or "—"

    nome_completo.short_description = "nome completo"

    def badge_tipo(self, obj):
        cores = {
            "CIDADAO": ("#dcfce7", "#15803d"),
            "AGENTE": ("#dbeafe", "#1d4ed8"),
            "ADMIN": ("#fef3c7", "#92400e"),
        }

        bg, txt = cores.get(obj.tipo, ("#f3f4f6", "#374151"))

        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:20px;font-size:11px;font-weight:600">{}</span>',
            bg, txt, obj.get_tipo_display(),
        )

    badge_tipo.short_description = "tipo"
