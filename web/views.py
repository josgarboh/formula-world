import json
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from web.models import Circuito, Piloto,Temporada, Equipo, Voto




def landing(request):
    return render(request, 'landing.html')

def index(request):
    return render(request, 'home.html')


############## CIRCUITOS

def list_circuitos(request):
    circuitos = Circuito.objects.all().order_by('-edicionesDisputadas')
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

    return render(request, 'detallesTemporada.html', {'temporada':temporada, 'mundialPilotos':mundialPilotos})


################# PILOTOS ##########

def list_pilotos(request):
    pilotos = Piloto.objects.all().order_by('-victoriasHistorico')
    page  = request.GET.get('page', 1) #Devuelve variable page o la pagina 1 en caso contrario

    try:
        paginator = Paginator(pilotos, 50)  # 50 pilotos en cada página
        pilotos = paginator.page(page)
    except: #si la página no existe
        raise Http404

    # Se pasa pilotos como 'entity' para reutilizar paginator.html
    return render(request, 'listPilotos.html', {'entity':pilotos, 'paginator':paginator})

def detallesPiloto(request, idEntrada):
    piloto = Piloto.objects.get(id=idEntrada)
    equiposDelPiloto = piloto.equipos_asociados()
    listaMundiales = piloto.listaCampeonatosMundiales()

    if listaMundiales[0] == "":
        numeroMundiales = 0
        listaMundiales = ""
        datos = {
        'piloto':piloto,
        'equiposDelPiloto':equiposDelPiloto,
        'listaMundiales':listaMundiales,
        'numeroMundiales':numeroMundiales
        }  
    else:
        numeroMundiales = len(listaMundiales)
        datos = {
        'piloto':piloto,
        'equiposDelPiloto':equiposDelPiloto,
        'listaMundiales':listaMundiales,
        'numeroMundiales':numeroMundiales
        }  

    return render(request, 'detallesPiloto.html', datos)

####################### EQUIPOS ##############

def list_equipos(request):
    equipos = Equipo.objects.all().order_by('-victoriasHistorico')
    page  = request.GET.get('page', 1) #Devuelve variable page o la pagina 1 en caso contrario

    try:
        paginator = Paginator(equipos, 50)  # 50 equipos en cada página
        equipos = paginator.page(page)
    except: #si la página no existe
        raise Http404

    # Se pasa equipos como 'entity' para reutilizar paginator.html
    return render(request, 'listEquipos.html', {'entity':equipos, 'paginator':paginator})

def detallesEquipo(request, idEntrada):
    equipo = Equipo.objects.get(id=idEntrada)
    listaMundiales = equipo.listaCampeonatosMundiales()

    #Hay un pequeño bug con la lista vacía, da como mínimo un mundial a cada uno
    if listaMundiales[0] == "":
        numeroMundiales = 0
        listaMundiales = ""
        datos = {
        'equipo':equipo,
        'listaMundiales':listaMundiales,
        'numeroMundiales':numeroMundiales
        }  
    else:
        numeroMundiales = len(listaMundiales)
        datos = {
        'equipo':equipo,
        'listaMundiales':listaMundiales,
        'numeroMundiales':numeroMundiales
        }  

    return render(request, 'detallesEquipo.html', datos)


############################## VOTACIÓN ########################

@login_required
def votar_objeto(request, modelo, objeto_id):
    tipoModelo = None

    if modelo == "circuito":
        tipoModelo = Circuito
    elif modelo == "temporada":
        tipoModelo = Temporada
    elif modelo == "piloto":
        tipoModelo = Piloto
    elif modelo == "equipo":
        tipoModelo = Equipo

    print(modelo)
    print(tipoModelo)

    if tipoModelo != None:
        objeto = get_object_or_404(tipoModelo, id = objeto_id)
        print(objeto)
        usario_logueado = request.user
        accion = request.POST.get("accion")
        print(accion)

        if accion == "vota_si":
            content_type = ContentType.objects.get_for_model(objeto)
            print(content_type)
            voto, created = Voto.objects.get_or_create(usuario = usario_logueado,
                                                        content_type = content_type,
                                                          object_id = objeto_id)
            voto.me_gusta = True
            voto.save()
    
    return redirect("detalles" +modelo.capitalize(), idEntrada=objeto_id)

    