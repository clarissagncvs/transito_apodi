# Importa o módulo de administração do Django
from django.contrib import admin

# Importa a classe padrão de administração de usuários do Django
from django.contrib.auth.admin import UserAdmin

# Importa o modelo Usuario criado por você
from .models import Usuario


# Registra o modelo Usuario no painel admin do Django
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    # Define quais campos aparecem na lista de usuários no admin
    list_display = ['username', 'email', 'tipo', 'is_active']

    # Adiciona filtros laterais no admin
    list_filter = ['tipo', 'is_active']

    # Permite buscar usuários pelo username ou email
    search_fields = ['username', 'email']


    # Define como os campos aparecem na tela de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        (
            'Trânsito Apodi',  # Título da seção personalizada
            {
                'fields': ('tipo', 'telefone', 'foto')  # Campos extras do seu model
            }
        ),
    )

