from django.shortcuts import render
from django.http import HttpResponse

def lista(request):
    return render(request, 'ocorrencia/ocorrencias.html')

# Create your views here.
