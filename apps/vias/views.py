# Importa a função render, usada para retornar templates HTML
from django.shortcuts import render

# Importa HttpResponse (não está sendo usado aqui)


# View da página inicial (home)
def home(request):

    # Renderiza o template localizado em:
    # templates/home/home.html
    # e retorna ele como resposta para o navegador
    return render(request, "home/home.html")
