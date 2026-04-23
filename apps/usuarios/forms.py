from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


# classes css padrão para reutilização nos campos
CSS = 'form-control'
CSS_SEL = 'form-select'


# form de registro baseado no usercreationform do django
class RegistroForm(UserCreationForm):

    # campo email obrigatório com input customizado
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': CSS,
            'placeholder': 'E-mail'
        })
    )

    class Meta:
        model = Usuario

        # campos exibidos no formulário de cadastro
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'telefone', 'password1', 'password2'
        ]

        # customização visual dos campos
        widgets = {
            'username': forms.TextInput(attrs={
                'class': CSS,
                'placeholder': 'Nome de usuário'
            }),
            'first_name': forms.TextInput(attrs={
                'class': CSS,
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': CSS,
                'placeholder': 'Sobrenome'
            }),
            'telefone': forms.TextInput(attrs={
                'class': CSS,
                'placeholder': 'Telefone'
            }),
        }

    # personalização dinâmica dos campos de senha
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adiciona classe css e placeholder no campo senha
        self.fields['password1'].widget.attrs.update({
            'class': CSS,
            'placeholder': 'Senha'
        })

        # adiciona classe css e placeholder no campo confirmação
        self.fields['password2'].widget.attrs.update({
            'class': CSS,
            'placeholder': 'Confirme a senha'
        })


# form simples para login
class LoginForm(forms.Form):

    # campo de usuário
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': CSS,
            'placeholder': 'Nome de usuário'
        })
    )

    # campo de senha (input oculto)
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': CSS,
            'placeholder': 'Senha'
        })
    )


# form para o próprio usuário editar seu perfil
class PerfilForm(forms.ModelForm):
    # não inclui o campo "tipo" por segurança

    class Meta:
        model = Usuario

        # campos permitidos para o usuário comum
        fields = ['first_name', 'last_name', 'email', 'telefone', 'foto']

        # customização visual
        widgets = {
            'first_name': forms.TextInput(attrs={'class': CSS}),
            'last_name': forms.TextInput(attrs={'class': CSS}),
            'email': forms.EmailInput(attrs={'class': CSS}),
            'telefone': forms.TextInput(attrs={'class': CSS}),
        }


# form usado pelo admin para editar usuários
class UsuarioAdminForm(forms.ModelForm):
    # admin pode alterar tudo, inclusive tipo e status

    class Meta:
        model = Usuario

        # campos disponíveis para o admin
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'telefone', 'tipo', 'is_active', 'foto'
        ]

        # customização visual dos campos
        widgets = {
            'username': forms.TextInput(attrs={'class': CSS}),
            'first_name': forms.TextInput(attrs={'class': CSS}),
            'last_name': forms.TextInput(attrs={'class': CSS}),
            'email': forms.EmailInput(attrs={'class': CSS}),
            'telefone': forms.TextInput(attrs={'class': CSS}),
            'tipo': forms.Select(attrs={'class': CSS_SEL}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }