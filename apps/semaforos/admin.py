from django.contrib import admin
from django.utils.html import format_html
from .models import Semaforo


@admin.register(Semaforo)
class SemaforoAdmin(admin.ModelAdmin):
    """Configuração do painel administrativo para os Semáforos de Apodi."""



    # Otimiza a consulta da FK 'via' para evitar o problema de N+1 consultas
    list_select_related = ["via"]

    # Colunas exibidas na listagem principal
    list_display = [
        "codigo",
        "via",
        "badge_status",
        "ativo",
    ]

    # Filtros laterais para facilitar a gestão
    list_filter = ["status", "ativo", "via", "criado_em"]

    # Campos pesquisáveis (pesquisa pelo código ou pelo nome da via relacionada)'
    search_fields = ["codigo", "via__nome"]

    # Ordenação padrão (por código)
    ordering = ["codigo"]

    # Permite alterar o status e ligar/desligar sem precisar entrar no registro
    list_editable = ["status", "ativo"]

    # Organização do formulário de edição/criação em blocos
    fieldsets = (
        ("Identificação Básica", {
            "fields": ("codigo", "via")
        }),
        ("Coordenadas Geográficas", {
            "fields": ("latitude", "longitude"),
            "description": "Localização precisa para o sistema de monitoramento regional."
        }),
        ("Estado de Operação", {
            "fields": ("status", "ativo"),
        }),
        ("Informações de Registro", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",),  # Deixa este bloco recolhido por padrão
        }),
    )

    # Método para exibir o status com um badge colorido (estilo Pills)
    def badge_status(self, obj):
        cores = {
            "VERDE": ("#dcfce7", "#15803d"),     
            "AMARELO": ("#fef3c7", "#92400e"),   
            "VERMELHO": ("#fee2e2", "#991b1b"),  
            "APAGADO": ("#f3f4f6", "#374151"),   
            "MANUTENCAO": ("#dbeafe", "#1d4ed8"), 
        }

        
        bg, txt = cores.get(obj.status, ("#f3f4f6", "#374151"))

        return format_html(
            '<span style="background:{}; color:{}; padding:3px 12px; '
            'border-radius:20px; font-size:11px; font-weight:700; '
            'text-transform:uppercase;">{}</span>',
            bg,
            txt,
            obj.get_status_display(),
        )

    badge_status.short_description = "Status Atual"