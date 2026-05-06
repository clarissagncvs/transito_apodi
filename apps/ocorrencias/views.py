# Importa a função render, usada para retornar templates HTML
from django.db.models import Q
from .models import Ocorrencia
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OcorrenciaForm
from django.contrib.auth.decorators import login_required

# View responsável por exibir a lista de ocorrências


def lista(request):
    ocorrencias = Ocorrencia.objects.select_related('via', 'usuario').all()

    tipo_filtro = request.GET.get('tipo', '')
    status_filtro = request.GET.get('status', '')
    busca = request.GET.get('busca', '')

    if tipo_filtro:
        ocorrencias = ocorrencias.filter(tipo=tipo_filtro)
    if status_filtro:
        ocorrencias = ocorrencias.filter(status=status_filtro)
    if busca:
        ocorrencias = ocorrencias.filter(
            Q(descricao__icontains=busca) | Q(via__nome__icontains=busca)
        )

    contexto = {
        'ocorrencias': ocorrencias,
        'tipos': Ocorrencia.Tipo.choices,
        'status_opcoes': Ocorrencia.Status.choices,
        'tipo_filtro': tipo_filtro,
        'status_filtro': status_filtro,
        'busca': busca,
    }

    return render(request, "pages/ocorrencias.html", contexto)


@login_required
def nova(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST, request.FILES)
        if form.is_valid():
            oc = form.save(commit=False)
            oc.usuario = request.user
            oc.save()
            return redirect('ocorrencias:lista')
    else:
        form = OcorrenciaForm()

    return render(request, 'pages/ocorrencia.html', {'form': form})


def detalhe(request, pk):
    # select_related: traz os dados de via e usuario juntos
    ocorrencia = get_object_or_404(
        Ocorrencia.objects.select_related('via', 'usuario'),
        pk=pk
    )

    contexto = {
        'ocorrencia': ocorrencia,
        'status_opcoes': Ocorrencia.Status.choices,
    }
    return render(request, 'ocorrencias/detalhe.html', contexto)


@login_required
def atualizar_status(request, pk):
    if not (request.user.is_agente or request.user.is_admin_transito):
        return redirect('ocorrencias:lista')

    oc = get_object_or_404(Ocorrencia, pk=pk)

    if request.method == 'POST':
        novo_status = request.POST.get('status')

        if novo_status in Ocorrencia.Status.values:
            oc.status = novo_status
            oc.save(update_fields=['status', 'atualizado_em'])

    return redirect('ocorrencias:detalhe', pk=pk)


@login_required
def status(request):
    return render(request, "pages/status.html")
