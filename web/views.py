import json
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q



from web.models import Circuito, Piloto,Temporada, Equipo, Voto


def landing(request):
    return render(request, 'landing.html')

def index(request):
    return render(request, 'home.html')

def terminos(request):
    return render(request, 'terms.html')

def gdpr(request):
    return render(request, 'gdpr.html')


############## CIRCUITOS

def list_circuitos(request):

    #Sprint 4: BUSCADOR
    query = request.GET.get('query')

    if query:
        query.lower() #Ignoramos así mayus/minus
        # Realiza la búsqueda en función de los campos que se introduzcan
        circuitos = Circuito.objects.filter(
            Q(nombre__icontains=query) |
            Q(pais__icontains=query) |    
            Q(tipo__icontains=query) |     
            Q(edicionesDisputadas__icontains=query) | 
            Q(longitud__icontains=query)  
        ).order_by('-edicionesDisputadas')
    else:
        # Si no hay consulta, muestra todos los circuitos
        circuitos = Circuito.objects.all().order_by('-edicionesDisputadas')

    return render(request, 'listCircuitos.html', {'circuitos':circuitos})


def detallesCircuito(request, idEntrada):
    circuito = Circuito.objects.get(id = idEntrada)
    siHaVotado = estadoVoto_AUX(request, Circuito, idEntrada)

    return render(request, 'detallesCircuito.html', {'cir':circuito, 'siHaVotado': siHaVotado})

############ TEMPORADAS #############

def list_temporadas(request):
    #temporadas = Temporada.objects.all().order_by('-anyo')

    #Sprint 4: BUSCADOR
    query = request.GET.get('query')
    if query:
        query.lower()
        temporadas = Temporada.objects.filter(
            Q(anyo__icontains=query)
        ).order_by('-anyo')
    else:
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
        objetoPiloto = Piloto.objects.get(nombre=nombre.lower()) #para poder redireccionar con urls

        equipo = datos['equipo'].title()
        objetoEquipo = Equipo.objects.get(nombre=equipo.lower())
        
        
        puntos = datos['puntosPiloto']
        if str(puntos).__contains__('.0'):  #Si es un número entero, quitaremos la coma
            puntos = int(puntos)

        mundialPilotos.append({'posicion': posicion,
                                'nombre': nombre, 'objetoPiloto':objetoPiloto, 
                                'equipo': equipo, 'objetoEquipo':objetoEquipo,
                                'puntos': puntos})

    return render(request, 'detallesTemporada.html', {'temporada':temporada, 'mundialPilotos':mundialPilotos})


################# PILOTOS ##########

def list_pilotos(request):
    
    #Sprint 4: BUSCADOR
    query = request.GET.get('query')

    if query:
        query.lower()
        pilotos = Piloto.objects.filter(
            Q(nombre__icontains=query) |
            Q(pais__icontains=query)
        ).order_by('-victoriasHistorico','-podiosHistorico','-puntosHistorico')

        #No paginamos en caso de búsqueda
        return render(request, 'listPilotos.html', {'entity':pilotos})
    else:
        pilotos = Piloto.objects.all().order_by('-victoriasHistorico','-podiosHistorico','-puntosHistorico')  
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
    siHaVotado = estadoVoto_AUX(request, Piloto, idEntrada)

    equiposDelPiloto = piloto.equipos_asociados()
    listaMundiales = piloto.listaCampeonatosMundiales()

    if listaMundiales[0] == "": #Significa que no hay ninguno (aunque len sea = 1)
        numeroMundiales = 0
        listaMundiales = ""
    else:
        numeroMundiales = len(listaMundiales)

    datos = {
        'piloto':piloto,
        'equiposDelPiloto':equiposDelPiloto,
        'listaMundiales':listaMundiales,
        'numeroMundiales':numeroMundiales,
        'siHaVotado': siHaVotado,
        }  

    return render(request, 'detallesPiloto.html', datos)

####################### EQUIPOS ##############

def list_equipos(request):
    #Sprint 4: BUSCADOR
    query = request.GET.get('query')

    if query:
        query.lower()
        equipos = Equipo.objects.filter(
            Q(nombre__icontains=query) |
            Q(pais__icontains=query)
        ).order_by('-victoriasHistorico','-podiosHistorico','-puntosHistorico')
        return render(request, 'listEquipos.html', {'entity':equipos})
    else:
        equipos = Equipo.objects.all().order_by('-victoriasHistorico','-podiosHistorico','-puntosHistorico')    
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
    siHaVotado = estadoVoto_AUX(request, Equipo, idEntrada)

    listaMundiales = equipo.listaCampeonatosMundiales()

    #Hay un pequeño bug con la lista vacía, da como mínimo un mundial a cada uno
    if listaMundiales[0] == "":
        numeroMundiales = 0
        listaMundiales = ""
    else:
        numeroMundiales = len(listaMundiales)
    datos = {
        'equipo':equipo,
        'listaMundiales':listaMundiales,
        'numeroMundiales':numeroMundiales,
        'siHaVotado':siHaVotado
        }      

    return render(request, 'detallesEquipo.html', datos)


############################## VOTACIÓN ########################

#Función que se usará en cada detalles"Modelo" para saber si el usuario ha votado ese modelo o no
def estadoVoto_AUX(request, modelo, idEntrada):
    if request.user.is_authenticated:
        usuario_logueado = request.user
        try:
            existeVoto = Voto.objects.get(usuario=usuario_logueado,
                                            content_type= ContentType.objects.get_for_model(modelo),
                                            object_id = idEntrada)
            siHaVotado = True
        except ObjectDoesNotExist:
            siHaVotado = False
    else:
        siHaVotado = False #No es un false como tal, es que el usuario está sin identificar        

    return siHaVotado

@login_required(login_url="/login")
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

    if tipoModelo != None:
        objeto = get_object_or_404(tipoModelo, id = objeto_id)
        usario_logueado = request.user
        accion = request.POST.get("accion")

        if accion == "vota_si":
            content_type = ContentType.objects.get_for_model(objeto)
            voto, created = Voto.objects.get_or_create(usuario = usario_logueado,
                                                        content_type = content_type,
                                                          object_id = objeto_id)
            voto.me_gusta = True
            voto.save()

        elif accion == "vota_no":
            content_type = ContentType.objects.get_for_model(objeto)
            #No sería voto, _ como arriba (esto devuelve unicamente el voto)
            votoNegativo = Voto.objects.get(usuario = usario_logueado, content_type = content_type,
                                                    object_id = objeto_id)
            votoNegativo.delete()          
    
    return redirect("detalles" +modelo.capitalize(), idEntrada=objeto_id)

    