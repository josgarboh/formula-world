from django.shortcuts import render
from web.models import Circuito #,Temporada

def landing(request):
    return render(request, 'landing.html')

def index(request):
    return render(request, 'home.html')

def list_circuitos(request):
    circuitos = Circuito.objects.all().order_by('nombre')
    return render(request, 'circuitos.html', {'circuitos':circuitos})

def detallesCircuito(request, idEntrada):
    circuito = Circuito.objects.get(id = idEntrada)
    return render(request, 'detallesCircuito.html', {'cir':circuito})
