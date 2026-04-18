from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import Usuario

# View da página inicial
def home(request):
    # Renderiza o template home/home.html quando acessar a rota da home
    return render(request, 'home/home.html')


# View de login
def login_view(request):
    # Se o usuário já estiver autenticado (logado),
    # redireciona direto para o perfil
    if request.user.is_authenticated:
        return redirect('perfil')

    # Verifica se o formulário foi enviado (POST)
    if request.method == 'POST':
        # Cria o formulário com os dados enviados
        form = LoginForm(request.POST)

        # Verifica se os dados do formulário são válidos
        if form.is_valid():
            # Tenta autenticar o usuário com username e senha
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # Se o usuário existir (login correto)
            if user is not None:
                # Faz login do usuário
                login(request, user)

                # Pega a URL que o usuário tentou acessar antes do login
                # Se não existir, vai para 'perfil'
                next_url = request.GET.get('next', 'perfil')

                # Redireciona o usuário
                return redirect(next_url)
            else:
                # Caso login inválido, mostra mensagem de erro
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        # Se não for POST, cria formulário vazio
        form = LoginForm()

    # Renderiza a página de login com o formulário
    return render(request, 'usuarios/login.html', {'form': form})


# View de logout
def logout_view(request):
    # Desloga o usuário
    logout(request)

    # Mostra mensagem de sucesso
    messages.success(request, 'Você saiu da conta.')

    # Redireciona para a tela de login
    return redirect('usuarios:login')


# View de registro (cadastro)
def registrar(request):
    # Se já estiver logado, manda para o perfil
    if request.user.is_authenticated:
        return redirect('perfil')

    # Se o formulário foi enviado
    if request.method == 'POST':
        # Cria o formulário com dados e arquivos (ex: foto)
        form = RegistroForm(request.POST, request.FILES)

        # Verifica se está válido
        if form.is_valid():
            # Salva o usuário no banco
            user = form.save()

            # Loga automaticamente após cadastro
            login(request, user)

            # Mensagem de boas-vindas
            messages.success(
                request,
                f'Bem-vindo, {user.first_name or user.username}!'
            )

            # Redireciona para o perfil
            return redirect('perfil')
    else:
        # Formulário vazio se for GET
        form = RegistroForm()

    # Renderiza a página de registro
    return render(request, 'usuarios/registro.html', {'form': form})


# View de perfil (precisa estar logado)
@login_required
def perfil(request):
    # Se o usuário enviar atualização (POST)
    if request.method == 'POST':
        # Pega o usuário atual
        user = request.user

        # Atualiza os campos com os dados do formulário
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name  = request.POST.get('last_name',  user.last_name)
        user.telefone   = request.POST.get('telefone',   user.telefone)

        # Se tiver enviado uma foto nova
        if request.FILES.get('foto'):
            user.foto = request.FILES['foto']

        # Salva as alterações no banco
        user.save()

        # Mensagem de sucesso
        messages.success(request, 'Perfil atualizado.')

        # Redireciona para o próprio perfil
        return redirect('usuarios:perfil')

    # Se for GET, só mostra os dados do usuário
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})


# Comentário padrão do Django (pode remover se quiser)
# Create your views here.
# Create your views here.
