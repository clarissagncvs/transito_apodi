from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model  = Usuario
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'telefone', 'password1', 'password2'
        ]
        labels = {
            'username':   'Nome de usuário',
            'first_name': 'Nome',
            'last_name':  'Sobrenome',
            'telefone':   'Telefone',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Seu usuário'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Sua senha'})
    )