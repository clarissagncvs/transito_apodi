from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import Usuario


def login_view(request):
    # se já está logado, manda direto pro perfil
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                # redireciona para onde o usuário queria ir
                # antes de ser mandado pro login
                next_url = request.GET.get('next', 'perfil')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da conta.')
    return redirect('usuarios:login')


def registrar(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # loga automaticamente após o registro
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            return redirect('perfil')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil(request):
    if request.method == 'POST':
        # atualiza só os campos permitidos
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name  = request.POST.get('last_name',  user.last_name)
        user.telefone   = request.POST.get('telefone',   user.telefone)
        if request.FILES.get('foto'):
            user.foto = request.FILES['foto']
        user.save()
        messages.success(request, 'Perfil atualizado.')
        return redirect('usuarios:perfil')

    return render(request, 'usuarios/perfil.html', {'usuario': request.user})

# Create your views here.
