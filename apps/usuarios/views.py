from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import Usuario
from django.views.decorators.http import require_POST

# View da página inicial
def home(request):
    # Renderiza o template home/home.html quando acessar a rota da home
    return render(request, 'home/home.html')


# View de login
def login_view(request):
    # Se o usuário já estiver autenticado (logado),
    # redireciona direto para home
    if request.user.is_authenticated:
        return redirect('home')

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
                # Se não existir, vai para 'home'
                next_url = request.GET.get('next', 'home')

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
    return redirect('apps.usuarios:login')


# View de registro (cadastro)
def registrar(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, f'Bem-vindo, {user.username}!')

            return redirect('home')

        else:
            print(form.errors)  # 👈 DEBUG IMPORTANTE

    else:
        form = RegistroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


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
        return redirect('apps.usuarios:perfil')

    # Se for GET, só mostra os dados do usuário
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('apps.usuarios:login')

# Comentário padrão do Django (pode remover se quiser)
# Create your views here.
# Create your views here.
