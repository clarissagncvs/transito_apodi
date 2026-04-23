# 1. padrão Python
from functools import wraps

# 2. Django / terceiros
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

# 3. locais
from .models import Usuario
from .forms import LoginForm, RegistroForm, PerfilForm, UsuarioAdminForm
from .services.usuario_service import UsuarioService


def home(request):
    return render(request, 'home/home.html')


# ── autenticação ──────────────────────────────────────────────

# view de login
def login_view(request):
    # se já estiver logado, redireciona
    if request.user.is_authenticated:
        return redirect('mapa')

    # se for envio de formulário
    if request.method == 'POST':
        # cria o form com os dados enviados
        form = LoginForm(request.POST)

        # valida o formulário
        if form.is_valid():
            # autentica o usuário
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            # se autenticou corretamente
            if user:
                # faz login
                login(request, user)
                # redireciona para próxima página ou mapa
                return redirect(request.GET.get('next', 'mapa'))

            # mensagem de erro
            messages.error(request, 'Usuário ou senha incorretos.')
    else:
        # cria form vazio
        form = LoginForm()

    # renderiza tela de login
    return render(request, 'usuarios/login.html', {'form': form})


# view de logout
def logout_view(request):
    # encerra a sessão
    logout(request)
    # redireciona para login
    return redirect('apps.usuarios:login')


# view de registro
def registrar(request):
    # impede acesso se já estiver logado
    if request.user.is_authenticated:
        return redirect('mapa')

    # se envio de formulário
    if request.method == 'POST':
        # cria form com dados e arquivos
        form = RegistroForm(request.POST, request.FILES)

        # valida o form
        if form.is_valid():
            # salva usuário
            user = form.save()
            # loga automaticamente
            login(request, user)
            # mensagem de sucesso
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            # redireciona
            return redirect('mapa')
    else:
        # form vazio
        form = RegistroForm()

    # renderiza tela de cadastro
    return render(request, 'usuarios/cadastro.html', {'form': form})


# ── perfil ───────────────────────────────────────────────────

# exige login
@login_required
def perfil(request):
    # se envio de formulário
    if request.method == 'POST':
        # cria form com dados do usuário logado
        form = PerfilForm(request.POST, request.FILES, instance=request.user)

        # valida form
        if form.is_valid():
            # atualiza usando service
            UsuarioService.atualizar_perfil(request.user, form.cleaned_data)
            # mensagem de sucesso
            messages.success(request, 'Perfil atualizado com sucesso.')
            # redireciona
            return redirect('apps.usuarios:perfil')
    else:
        # form preenchido com dados atuais
        form = PerfilForm(instance=request.user)

    # renderiza página de perfil
    return render(request, 'usuarios/perfil.html', {'form': form})


# ── permissão admin ──────────────────────────────────────────

# decorator customizado para exigir admin_transito
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_transito:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


# ── lista de usuários ────────────────────────────────────────

@login_required
@admin_required
def usuario_lista(request):
    # pega todos os usuários
    qs = Usuario.objects.all()

    # pega filtros da url
    tipo  = request.GET.get('tipo', '')
    busca = request.GET.get('q', '')
    ativo = request.GET.get('ativo', '')

    # aplica filtros via service
    qs = UsuarioService.filtrar_usuarios(qs, tipo, busca, ativo)

    # pagina resultados
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))

    # renderiza lista
    return render(request, 'usuarios/lista.html', {
        'page_obj': page,
        'tipo_choices': Usuario.Tipo.choices,
        'filtro_tipo': tipo,
        'filtro_busca': busca,
        'filtro_ativo': ativo,
        'total': qs.count(),
    })


# ── criar usuário ────────────────────────────────────────────

@login_required
@admin_required
def usuario_criar(request):
    # se envio de formulário
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)

        # valida form
        if form.is_valid():
            # pega dados limpos
            data = form.cleaned_data

            # adiciona tipo manualmente
            data['tipo'] = request.POST.get('tipo', Usuario.Tipo.CIDADAO)

            # cria usuário via service
            user = UsuarioService.criar_usuario(data)

            # mensagem de sucesso
            messages.success(request, f'Usuário {user.username} criado com sucesso.')
            return redirect('apps.usuarios:lista')
    else:
        # form vazio
        form = RegistroForm()

    # renderiza form
    return render(request, 'usuarios/form.html', {
        'form': form,
        'titulo': 'Novo usuário',
        'tipo_choices': Usuario.Tipo.choices,
        'btn_label': 'Criar usuário',
    })


# ── editar usuário ───────────────────────────────────────────

@login_required
@admin_required
def usuario_editar(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)

    # se envio
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST, request.FILES, instance=usuario)

        # valida form
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado.')
            return redirect('apps.usuarios:lista')
    else:
        form = UsuarioAdminForm(instance=usuario)

    # renderiza form
    return render(request, 'usuarios/form.html', {
        'form': form,
        'titulo': f'Editar — {usuario.username}',
        'usuario': usuario,
        'tipo_choices': Usuario.Tipo.choices,
        'btn_label': 'Salvar alterações',
    })


# ── detalhe ──────────────────────────────────────────────────

@login_required
@admin_required
def usuario_detalhe(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)
    # renderiza detalhe
    return render(request, 'usuarios/detalhe.html', {'usuario': usuario})


# ── deletar usuário ──────────────────────────────────────────

@login_required
@admin_required
def usuario_deletar(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)

    # só executa se for post
    if request.method == 'POST':
        try:
            # usa service para deletar
            UsuarioService.deletar_usuario(usuario, request.user)
            messages.success(request, f'Usuário {usuario.username} removido.')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('apps.usuarios:lista')

    # renderiza confirmação
    return render(request, 'usuarios/confirmar_delete.html', {'usuario': usuario})


# ── ativar / desativar ───────────────────────────────────────

@login_required
@admin_required
def usuario_toggle_ativo(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)

    try:
        # alterna status via service
        UsuarioService.toggle_ativo(usuario, request.user)
        status = 'ativado' if usuario.is_active else 'desativado'
        messages.success(request, f'Usuário {usuario.username} {status}.')
    except Exception as e:
        messages.error(request, str(e))

    # redireciona
    return redirect('apps.usuarios:lista')