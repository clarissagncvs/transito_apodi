from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo', 'is_active']
    list_filter = ['tipo', 'is_active']
    search_fields = ['username', 'email']

    fieldsets = UserAdmin.fieldsets + (
        ('Trânsito Apodi', {'fields': ('tipo', 'telefone', 'foto')})
    )

#from django.contrib import admin importa o sistema de admin do django
#from django.contrib.auth.admin import UserAdmin from importa uma classe pronta do django que gerencia usuarios
#from .models import Usuario importa o models de usuário criado
#@admin.register(Usuario) registra o modelo Usuario no painel admin
#class UsuarioAdmin(UserAdmin): cria um admin customizado para o usuario e herda coisas de UserAdmin
#list_display = ['username', 'email', 'tipo', 'is_active'] define as colunas que aparecem na listagem do admin
#list_filter = ['tipo', 'is_active'] cria filtros 
#search_fields = ['username', 'email'] permite buscar o usuário pelo nome e pelo email
#fieldsets = UserAdmin.fieldsets + (('Trânsito Apodi', {'fields': ('tipo', 'telefone', 'foto')})) define como os campos aparecem no formilário de edição no admin


