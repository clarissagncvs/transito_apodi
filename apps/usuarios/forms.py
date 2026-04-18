from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


# Formulário de registro de usuário (cadastro)
class RegistroForm(UserCreationForm):
    # Adiciona o campo de email como obrigatório
    email = forms.EmailField(required=True)

    # Classe interna Meta define configurações do formulário
    class Meta:
        # Define qual modelo será usado (seu model personalizado Usuario)
        model = Usuario

        # Define os campos que aparecerão no formulário
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'telefone', 'password1', 'password2'
        ]

        # Define os nomes amigáveis que aparecem no HTML
        labels = {
            'username':   'Nome de usuário',
            'first_name': 'Nome',
            'last_name':  'Sobrenome',
            'telefone':   'Telefone',
        }

    # Sobrescreve o método save para customizar o salvamento
    def save(self, commit=True):
        # Cria o usuário, mas ainda não salva no banco
        user = super().save(commit=False)

        # Adiciona o email manualmente ao usuário
        user.email = self.cleaned_data['email']

        # Se commit=True, salva no banco de dados
        if commit:
            user.save()

        # Retorna o usuário criado
        return user


# Formulário de login (não usa ModelForm, é manual)
class LoginForm(forms.Form):
    # Campo de usuário
    username = forms.CharField(
        label='Usuário',  # Nome que aparece no formulário
        widget=forms.TextInput(
            attrs={'placeholder': 'Seu usuário'}  # Texto dentro do input
        )
    )

    # Campo de senha
    password = forms.CharField(
        label='Senha',  # Nome exibido
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Sua senha'}  # Input tipo senha (oculta texto)
        )
    )