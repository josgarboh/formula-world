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

############ TEMPORADAS #############

def list_temporadas(request):
    temporadas = Temporada.objects.all().order_by('-anyo')

    ganadores = []
    for temporada in temporadas:
        dataFile = json.loads(temporada.tablaPilotos)
        ganadores.append(dataFile.get("1").get("nombre"))

    temporadas_ganadores = zip(temporadas, ganadores)

    return render(request, 'listTemporadas.html', {'temporadas_ganadores':temporadas_ganadores})

def detallesTemporada(request, anyoEntrada):
    temporada = Temporada.objects.get(anyo = anyoEntrada)

    dataFile = json.loads(temporada.tablaPilotos)

    #MUNDIAL DE PILOTOS
    mundialPilotos = []
    for posicion, datos in dataFile.items():
        nombre = datos['nombre'].title()
        equipo = datos['equipo'].title()
        puntos = datos['puntosPiloto']
        mundialPilotos.append({'posicion': posicion, 'nombre': nombre, 'equipo': equipo, 'puntos': puntos})


    #Descartamos de momento
    #MUNDIAL DE CONSTRUCTORES: lo haremos sumando los puntos de los pilotos que hayan corrido para la escudería ese año
    
    # mundialConstructores = dict() # {equipo:puntos}
    # for diccionarioPiloto in mundialPilotos:
    #     equipo = diccionarioPiloto['equipo']#.title()
    #     if equipo not in mundialConstructores.keys():
    #         mundialConstructores[equipo] = diccionarioPiloto['puntos']
    #     else:
    #        puntos = mundialConstructores.get(equipo)
    #        puntos +=  diccionarioPiloto['puntos']
    #        mundialConstructores[equipo] = puntos

    # #ordenamos de mayor a menos puntuación
    # mundialConstructores = dict(sorted(mundialConstructores.items(), key= lambda x:x[1], reverse=True))
    # print(mundialConstructores)    

    return render(request, 'detallesTemporada.html', {'temporada':temporada, 'mundialPilotos':mundialPilotos})
