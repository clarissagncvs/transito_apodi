# padrão python
from functools import wraps

# django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

# locais
from .models import Usuario
from .forms import LoginForm, RegistroForm, PerfilForm, UsuarioAdminForm
from .services.usuario_service import UsuarioService


# view da página inicial
def home(request):
    return render(request, 'home/home.html')


# login do usuário
def login_view(request):
    # redireciona se já estiver logado
    if request.user.is_authenticated:
        return redirect('mapa')

    # verifica envio do formulário
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            # autentica usuário
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            # se autenticado, faz login
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'mapa'))

            # erro de login
            messages.error(request, 'usuário ou senha incorretos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


# logout do usuário
def logout_view(request):
    logout(request)
    return redirect('apps.usuarios:login')


# registro de usuário
def registrar(request):
    # impede acesso se já estiver logado
    if request.user.is_authenticated:
        return redirect('mapa')

    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)

        if form.is_valid():
            # cria usuário via form
            user = form.save()

            # loga automaticamente
            login(request, user)

            messages.success(request, f'bem-vindo, {user.first_name or user.username}!')
            return redirect('mapa')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


# perfil do usuário logado
@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            # usa service para atualizar
            UsuarioService.atualizar_perfil(request.user, form.cleaned_data)

            messages.success(request, 'perfil atualizado com sucesso.')
            return redirect('apps.usuarios:perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'usuarios/perfil.html', {'form': form})


# decorator para exigir admin
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_transito:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


# lista de usuários
@login_required
@admin_required
def usuario_lista(request):
    # queryset inicial
    qs = Usuario.objects.all()

    # filtros
    tipo  = request.GET.get('tipo', '')
    busca = request.GET.get('q', '')
    ativo = request.GET.get('ativo', '')

    # aplica filtros via service
    qs = UsuarioService.filtrar_usuarios(qs, tipo, busca, ativo)

    # paginação
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'usuarios/lista.html', {
        'page_obj': page,
        'tipo_choices': Usuario.Tipo.choices,
        'filtro_tipo': tipo,
        'filtro_busca': busca,
        'filtro_ativo': ativo,
        'total': qs.count(),
    })


# criar usuário
@login_required
@admin_required
def usuario_criar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            # adiciona tipo manualmente
            data['tipo'] = request.POST.get('tipo', Usuario.Tipo.CIDADAO)

            # cria via service
            user = UsuarioService.criar_usuario(data)

            messages.success(request, f'usuário {user.username} criado com sucesso.')
            return redirect('apps.usuarios:lista')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/form.html', {
        'form': form,
        'titulo': 'novo usuário',
        'tipo_choices': Usuario.Tipo.choices,
        'btn_label': 'criar usuário',
    })


# editar usuário
@login_required
@admin_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST, request.FILES, instance=usuario)

        if form.is_valid():
            form.save()
            messages.success(request, 'usuário atualizado.')
            return redirect('apps.usuarios:lista')
    else:
        form = UsuarioAdminForm(instance=usuario)

    return render(request, 'usuarios/form.html', {
        'form': form,
        'titulo': f'editar — {usuario.username}',
        'usuario': usuario,
        'tipo_choices': Usuario.Tipo.choices,
        'btn_label': 'salvar alterações',
    })


# detalhe do usuário
@login_required
@admin_required
def usuario_detalhe(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/detalhe.html', {'usuario': usuario})


# deletar usuário
@login_required
@admin_required
def usuario_deletar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        try:
            # usa service para deletar
            UsuarioService.deletar_usuario(usuario, request.user)
            messages.success(request, f'usuário {usuario.username} removido.')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('apps.usuarios:lista')

    return render(request, 'usuarios/confirmar_delete.html', {'usuario': usuario})


# ativar ou desativar usuário
@login_required
@admin_required
def usuario_toggle_ativo(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    try:
        # usa service para alternar status
        UsuarioService.toggle_ativo(usuario, request.user)

        status = 'ativado' if usuario.is_active else 'desativado'
        messages.success(request, f'usuário {usuario.username} {status}.')
    except Exception as e:
        messages.error(request, str(e))

    return redirect('apps.usuarios:lista')