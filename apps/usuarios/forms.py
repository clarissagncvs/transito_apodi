import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Usuario

# classes css padrão para reutilização nos campos
CSS = "form-control"
CSS_SEL = "form-select"


# form de registro baseado no usercreationform do django
class RegistroForm(UserCreationForm):

    # campo email obrigatório com input customizado
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": CSS, "placeholder": "E-mail"}),
    )

    class Meta:
        model = Usuario

        # campos exibidos no formulário de cadastro
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

        # customização visual dos campos
        widgets = {
            "username": forms.TextInput(
                attrs={"class": CSS, "placeholder": "Nome de usuário"}
            ),
            "first_name": forms.TextInput(attrs={"class": CSS, "placeholder": "Nome"}),
            "last_name": forms.TextInput(
                attrs={"class": CSS, "placeholder": "Sobrenome"}
            ),
        }

    # personalização dinâmica dos campos de senha
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adiciona classe css e placeholder no campo senha
        self.fields["password1"].widget.attrs.update(
            {"class": CSS, "placeholder": "Senha"}
        )

        # adiciona classe css e placeholder no campo confirmação
        self.fields["password2"].widget.attrs.update(
            {"class": CSS, "placeholder": "Confirme a senha"}
        )

    # validações
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já foi cadastrado por algum usuário.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        user = self.instance  # Opcional: ajuda o validador de similaridade

        if p1:
            try:
                # Valida contra as regras do settings.py
                validate_password(p1, user)
            except ValidationError as e:
                # Adiciona o erro especificamente ao campo de senha
                self.add_error('password1', e)

        return cleaned_data


# form simples para login
class LoginForm(forms.Form):

    # campo de usuário
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={"class": CSS, "placeholder": "Nome de usuário"}),
    )

    # campo de senha (input oculto)
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": CSS, "placeholder": "Senha"}),
    )


# form para o próprio usuário editar seu perfil
class PerfilForm(forms.ModelForm):
    # não inclui o campo "tipo" por segurança

    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "email"]

        # customização visual
        widgets = {
            "first_name": forms.TextInput(attrs={"class": CSS}),
            "last_name": forms.TextInput(attrs={"class": CSS}),
            "email": forms.EmailInput(attrs={"class": CSS}),
        }


# form usado pelo admin para editar usuários
class UsuarioAdminForm(forms.ModelForm):
    # admin pode alterar tudo, inclusive tipo e status

    class Meta:
        model = Usuario

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "tipo",
            "is_active",
        ]

        # customização visual dos campos
        widgets = {
            "username": forms.TextInput(attrs={"class": CSS}),
            "first_name": forms.TextInput(attrs={"class": CSS}),
            "last_name": forms.TextInput(attrs={"class": CSS}),
            "email": forms.EmailInput(attrs={"class": CSS}),
            "tipo": forms.Select(attrs={"class": CSS_SEL}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

# mudei aqui (aiane)

# Formulário para editar APENAS o nome (username) na pagina editar-usuario


class UsuarioUpdateNomeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(attrs={"class": CSS, "placeholder": "Novo nome de usuário"}),
        }

# Formulário para editar APENAS o e-mail na pagina editar-email


class UsuarioUpdateEmailForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": CSS, "placeholder": "Novo e-mail"}),
        }

    # Reutiliza a validação de email (AGORA ESTÁ DENTRO DA CLASSE, INDENTAÇÃO CORRIGIDA)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se o e-mail já existe, mas ignora o e-mail do próprio usuário atual
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este e-mail já está em uso por outra conta.")
        return email


class UsuarioUpdateTipoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['tipo']
