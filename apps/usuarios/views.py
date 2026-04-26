# 1. padrão Python
from functools import wraps

# 2. Django / terceiros
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.utils import timezone

# 3. locais
from .models import Usuario
from .forms import LoginForm, RegistroForm, PerfilForm, UsuarioAdminForm
from .services.usuario_service import UsuarioService


def home(request):
    return render(request, "pages/home.html")


# ── autenticação ──────────────────────────────────────────────


# view de login
def login_view(request):
    # se já estiver logado, redireciona
    if request.user.is_authenticated:
        return redirect("home")

    # se for envio de formulário
    if request.method == "POST":
        # cria o form com os dados enviados
        form = LoginForm(request.POST)

        # valida o formulário
        if form.is_valid():
            # autentica o usuário
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            # se autenticou corretamente
            if user:
                # faz login
                login(request, user)
                # redireciona para próxima página ou mapa
                return redirect(request.GET.get("next", "home"))

            # mensagem de erro
            messages.error(request, "Usuário ou senha incorretos.")
    else:
        # cria form vazio
        form = LoginForm()

    # renderiza tela de login
    return render(request, "pages/login.html", {"form": form})


# view de logout
def logout_view(request):
    # encerra a sessão
    logout(request)
    # redireciona para login
    return redirect("apps.usuarios:login")


# view de registro
def registrar(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistroForm(request.POST, request.FILES)

        if form.is_valid():
            # Pegamos os dados validados do formulário
            dados_usuario = form.cleaned_data

            # Chamamos o Service (Ele cria o usuário inativo e envia o e-mail)
            user = UsuarioService.criar_usuario(dados_usuario)

            messages.success(request, f"Código enviado para {user.email}!")

            # Guardamos o ID do usuário na sessão para saber quem está verificando o código
            request.session['usuario_verificando_id'] = user.id

            return redirect("apps.usuarios:verificar_codigo")
        else:
            # Se cair aqui, o formulário volta com os erros (ex: email duplicado)
            messages.error(request, "Erro no cadastro. Verifique os dados.")
    else:
        form = RegistroForm()

    return render(request, "pages/cadastro.html", {"form": form})


def verificar_codigo(request):
    # Pega o ID do usuário que acabou de se cadastrar
    usuario_id = request.session.get('usuario_verificando_id')

    if not usuario_id:
        return redirect("apps.usuarios:registrar")

    if request.method == "POST":
        codigo_digitado = request.POST.get("codigo")
        usuario = get_object_or_404(Usuario, id=usuario_id)

        # Validação do código e do tempo
        agora = timezone.now()

        if (usuario.codigo_verificacao == codigo_digitado and usuario.codigo_expira_em > agora):

            usuario.is_active = True
            usuario.codigo_verificacao = None  # Limpa o código
            usuario.save(update_fields=['is_active', 'codigo_verificacao'])

            messages.success(request, "Conta ativada com sucesso! Faça login.")
            return redirect("apps.usuarios:login")
        else:
            messages.error(request, "Código inválido ou expirado.")

    return render(request, "pages/verificador.html")

def reenviar_codigo(request):
    usuario_id = request.session.get('usuario_verificando_id')

    if not usuario_id:
        return redirect("apps.usuarios:registro")

    usuario = get_object_or_404(Usuario, id=usuario_id)

    try:
        UsuarioService.reenviar_codigo(usuario)
        messages.success(request, f"Novo código enviado para {usuario.email}!")
    except Exception as e:
        print(f'Erro ao reenviar: {e}')
        messages.error(request, f"Erro: {e}")

    return redirect("apps.usuarios:verificar_codigo")

# ── perfil ───────────────────────────────────────────────────


# exige login
@login_required
def perfil(request):
    # se envio de formulário
    if request.method == "POST":
        # cria form com dados do usuário logado
        form = PerfilForm(request.POST, request.FILES, instance=request.user)

        # valida form
        if form.is_valid():
            # atualiza usando service
            UsuarioService.atualizar_perfil(request.user, form.cleaned_data)
            # mensagem de sucesso
            messages.success(request, "Perfil atualizado com sucesso.")
            # redireciona
            return redirect("apps.usuarios:perfil")
    else:
        # form preenchido com dados atuais
        form = PerfilForm(instance=request.user)

    # renderiza página de perfil
    return render(request, "pages/perfil.html", {"form": form})


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
    tipo = request.GET.get("tipo", "")
    busca = request.GET.get("q", "")
    ativo = request.GET.get("ativo", "")

    # aplica filtros via service
    qs = UsuarioService.filtrar_usuarios(qs, tipo, busca, ativo)

    # pagina resultados
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get("page"))

    # renderiza lista
    return render(
        request,
        "pages/lista.html",
        {
            "page_obj": page,
            "tipo_choices": Usuario.Tipo.choices,
            "filtro_tipo": tipo,
            "filtro_busca": busca,
            "filtro_ativo": ativo,
            "total": qs.count(),
        },
    )


# ── criar usuário ────────────────────────────────────────────


@login_required
@admin_required
def usuario_criar(request):
    # se envio de formulário
    if request.method == "POST":
        form = RegistroForm(request.POST, request.FILES)

        # valida form
        if form.is_valid():
            # pega dados limpos
            data = form.cleaned_data

            # adiciona tipo manualmente
            data["tipo"] = request.POST.get("tipo", Usuario.Tipo.CIDADAO)

            # cria usuário via service
            user = UsuarioService.criar_usuario(data)

            # mensagem de sucesso
            messages.success(request, f"Usuário {user.username} criado com sucesso.")
            return redirect("apps.usuarios:lista")
    else:
        # form vazio
        form = RegistroForm()

    # renderiza form
    return render(
        request,
        "pages/form.html",
        {
            "form": form,
            "titulo": "Novo usuário",
            "tipo_choices": Usuario.Tipo.choices,
            "btn_label": "Criar usuário",
        },
    )


# ── editar usuário ───────────────────────────────────────────


@login_required
@admin_required
def usuario_editar(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)

    # se envio
    if request.method == "POST":
        form = UsuarioAdminForm(request.POST, request.FILES, instance=usuario)

        # valida form
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado.")
            return redirect("apps.usuarios:lista")
    else:
        form = UsuarioAdminForm(instance=usuario)

    # renderiza form
    return render(
        request,
        "pages/form.html",
        {
            "form": form,
            "titulo": f"Editar — {usuario.username}",
            "usuario": usuario,
            "tipo_choices": Usuario.Tipo.choices,
            "btn_label": "Salvar alterações",
        },
    )


# ── detalhe ──────────────────────────────────────────────────


@login_required
@admin_required
def usuario_detalhe(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)
    # renderiza detalhe
    return render(request, "pages/detalhe.html", {"usuario": usuario})


# ── deletar usuário ──────────────────────────────────────────


@login_required
@admin_required
def usuario_deletar(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)

    # só executa se for post
    if request.method == "POST":
        try:
            # usa service para deletar
            UsuarioService.deletar_usuario(usuario, request.user)
            messages.success(request, f"Usuário {usuario.username} removido.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect("apps.usuarios:lista")

    # renderiza confirmação
    return render(request, "pages/confirmar_delete.html", {"usuario": usuario})


# ── ativar / desativar ───────────────────────────────────────


@login_required
@admin_required
def usuario_toggle_ativo(request, pk):
    # busca usuário
    usuario = get_object_or_404(Usuario, pk=pk)

    try:
        # alterna status via service
        UsuarioService.toggle_ativo(usuario, request.user)
        status = "ativado" if usuario.is_active else "desativado"
        messages.success(request, f"Usuário {usuario.username} {status}.")
    except Exception as e:
        messages.error(request, str(e))

    # redireciona
    return redirect("apps.usuarios:lista")
