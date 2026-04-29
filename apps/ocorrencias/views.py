# Importa a função render, usada para retornar templates HTML
from django.shortcuts import render
from django.contrib.auth.decorators import login_required   


# Importa HttpResponse, usado para retornar respostas simples (texto puro, por exemplo)
# View responsável por exibir a lista de ocorrências
def lista(request):

    # Renderiza (carrega) o template HTML localizado em:
    # templates/ocorrencia/ocorrencias.html
    # e retorna como resposta para o navegador
    return render(request, "pages/ocorrencias.html")


# Comentário padrão criado pelo Django ao gerar o arquivo views.py
# Pode ser removido se quiser, não tem função prática
# Create your views here.

@login_required
def status(request):
    print(request.user)           # mostra quem está logado
    print(request.user.is_authenticated)  # True ou False
    return render(request, "pages/status.html")
