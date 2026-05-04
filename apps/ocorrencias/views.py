# Importa a função render, usada para retornar templates HTML
from django.shortcuts import render
from django.db.models import Q
from .models import Ocorrencia, Alerta
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OcorrenciaForm
from django.contrib.auth.decorators import login_required

# Importa HttpResponse, usado para retornar respostas simples (texto puro, por exemplo)
# View responsável por exibir a lista de ocorrências
def lista(request):
#busca todas as ocorrencias do banco de dados
    ocorrencias = Ocorrencia.objects.select_related('via', 'usuario').all()
    
    tipo_filtro   = request.GET.get('tipo', '')
    status_filtro = request.GET.get('status', '')
    busca         = request.GET.get('busca', '')
   
    if tipo_filtro:
        ocorrencias = ocorrencias.filter(tipo=tipo_filtro)

    if status_filtro:
        ocorrencias = ocorrencias.filter(status=status_filtro)

    if busca:
        ocorrencias = ocorrencias.filter(
            Q(descricao__icontains=busca) |
            Q(via__nome__icontains=busca)
        )

#dicionario python que envia dados ao HTML
    contexto = {
        'ocorrencias': ocorrencias, #lista de ocorrecias filtradas
        'tipos': Ocorrencia.Tipo.choices,
        'status.opcoes': Ocorrencia.Status.choices, 
        'tipo_filtro': status_filtro, #filtro atual
        'status_filtro': tipo_filtro, 
        'busca': busca,
    }
# Renderiza (carrega) o template HTML localizado em:
# templates/ocorrencia/ocorrencias.html
# e retorna como resposta para o navegador
    return render(request, "pages/ocorrencias.html")

@login_required
def nova(request):
#Se o usuário enviou o formulário
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST, request.FILES)
        #valida todos os campos
        #retorna True se tudo estiver ok, False se houver erro
        if form.is_valid():
            #cria o objeto Ocorrencia, mas precisa adiionar o campo 'usuario' antes de salvar no bd
            #commit=False: prepara a ocorrência, mas não registra ainda
            oc = form.save(commit=False)
            #request.user: o usuario está logado agora
            #registra quem fez a ocorrência
            oc.usuario = request.user
            #salva no banco de dados
            oc.save()
#gera o alerta automático
        if oc.tipo in ('ACIDENTE', 'SEMAFORO'):
            nivel = 'CRITICO' if oc.tipo == 'ACIDENTE' else 'AVISO'

            mensagem = f'{oc.get_tipo_display()} em {oc.via}'
#Cria e salva o alerta no banco
            Alerta.objects.create(
                ocorrencia=oc, #liga o alerta à ocorrência
                nivel=nivel,
                mensagem=mensagem,
            )
#Manda o navegador ir para a lista
        return redirect('ocorrencias:lista')
#exibe um formulário em branco pro usuáio preencher
    else:
        form = OcorrenciaForm() #formulario vazio

    return render(request, 'pages/ocorrencias.html', {'ocorrencias': form})

def detalhe(request, pk):
#Tenta buscar Ocorrencia WHERE id = pk
#Se encontrar: retorna o objeto
#se não: retorna a página 404 automaticamente
#select_related: traz os dados de via e usuario juntos
    ocorrencia = get_object_or_404(
        Ocorrencia.objects.select_related('via', 'usuario'),
        pk=pk
    )

#busca todos os alertas vinculados a essa ocorrencia
    alertas = ocorrencia.alertas.all()

    contexto = {
        'ocorrencia': ocorrencia,
        'alertas': alertas,
    #status para o template montar as atualizações de status pro agente
        'status_opcoes': Ocorrencia.Status.choices,
    }
    return render(request, 'ocorrencias/detalhe.html', contexto)


