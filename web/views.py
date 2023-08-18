import json
from django.shortcuts import render
from web.models import Circuito,Temporada

def landing(request):
    return render(request, 'landing.html')

def index(request):
    return render(request, 'home.html')

def list_circuitos(request):
    circuitos = Circuito.objects.all().order_by('id')
    return render(request, 'listCircuitos.html', {'circuitos':circuitos})

def detallesCircuito(request, idEntrada):
    circuito = Circuito.objects.get(id = idEntrada)
    return render(request, 'detallesCircuito.html', {'cir':circuito})

def list_temporadas(request):
    temporadas = Temporada.objects.all().order_by('-anyo')

    ganadores = []
    for temporada in temporadas:
        dataFile = json.loads(temporada.tablaPilotos)
        ganadores.append(dataFile.get("1").get("nombre"))

    temporadas_ganadores = zip(temporadas, ganadores)

    return render(request, 'listTemporadas.html', {'temporadas_ganadores':temporadas_ganadores})
