from math import sqrt
from statistics import mean
from web.models import Equipo, EquiposYPilotos, Voto, User, Circuito, Piloto
from django.contrib.contenttypes.models import ContentType

def prueba():
    print(Piloto.objects.get(id=240).numeroMundiales)


# SISTEMA DE RECOMENDACIÓN BASADO EN CONTENIDO #

# Objetivo: {Usuario: [id1,id2...]}
# Habrá un diccionario por modelo (vistas separadas)

def organiza_votos(modelo):
    diccionario = {}
    for usuario in User.objects.all():
        votosUsuario = []
        votosModelo = Voto.objects.filter(usuario=usuario, content_type=ContentType.objects.get_for_model(modelo))
        for voto in votosModelo:
            votosUsuario.append(voto.object_id) #añadimos el id objeto (del modelo concreto) votado
        diccionario[usuario] = votosUsuario
    
    return diccionario # devolvemos todos los votos del modelo pasado organizado por usuario

def organiza_votos_2(modelo, usuario):
    votosUsuario = []
    votosModelo = Voto.objects.filter(usuario=usuario, content_type=ContentType.objects.get_for_model(modelo))
    for voto in votosModelo:
        votosUsuario.append(voto.object_id)
    
    return votosUsuario

##### Función para circuitos ####
# Puntuamos tipo, longitud y ediciones disputadas

#circuitos gustados es la lista de circuitos a los que request.user ha dado me gusta
def recomienda_circuitos(circuitos_votados, ponderacion_tipo=4, ponderacion_longitud=4, ponderacion_ediciones=2): #le doy valores predeterminados

    #Transformamos las id en el objeto
    circuitos_gustados = []
    for id in circuitos_votados:
        circuitos_gustados.append(Circuito.objects.get(id=id))

    tipos_votados = []
    longitudes_votadas = []
    ediciones_votadas = []
    for cir_g in circuitos_gustados:
        tipos_votados.append(cir_g.tipo) #los tipos que le gustan
        longitudes_votadas.append(cir_g.longitud)
        ediciones_votadas.append(cir_g.edicionesDisputadas)

    media_longitud = mean(longitudes_votadas)
    media_ediciones = mean(ediciones_votadas)

    valoraciones_no_votados = {}
    for circuito in Circuito.objects.all():
        puntuacionCircuito = 0
        if circuito not in circuitos_gustados: #Para no recomendar los que ya le gustan
            
            #tipo
            if circuito.tipo in tipos_votados:
                puntuacionCircuito+=ponderacion_tipo #lo que más suma

            #longitud
            longitud = circuito.longitud
            ponderacionMaximaLongitud = ponderacion_longitud
            proporcion_cercania = 1 - abs(longitud - media_longitud) / (2 * media_longitud)
            puntuacionCircuito += ponderacionMaximaLongitud * proporcion_cercania

            #edicionesDisputadas
            ediciones = circuito.edicionesDisputadas
            ponderacionMaximaEdiciones = ponderacion_ediciones
            proporcion_cercania_2 = 1 - abs(ediciones - media_ediciones) / (2 * media_ediciones)
            puntuacionCircuito += ponderacionMaximaEdiciones * proporcion_cercania_2

            valoraciones_no_votados[circuito] = puntuacionCircuito

    recomendaciones_ordenadas = dict(sorted(valoraciones_no_votados.items(), key=lambda item: item[1], reverse=True))
    
    return list(recomendaciones_ordenadas.keys())[:9] #Devolvemos los 9 con más nota

##### Función para pilotos ####
# Puntuamos
# coincidencia de nacionalidad (20pts)
# cercanía en longevidad de carrera (numero temporadas 20pts max)
# cercanía a media de mundiales, victorias y podios

# EXTRA: Coincidencia de equipos en los que ha estado (si le gusta el equipo)

def recomienda_pilotos(pilotos_votados,equipos_votados,ponderacion_equipos=5,
                       ponderacion_pais=5,ponderacion_longevidad=3,ponderacion_mundiales=5,
                       ponderacion_victorias=3,ponderacion_podios=2): #valores por defecto

    #Transformamos las id en el objeto
    pilotos_gustados = []

    for id in pilotos_votados:
        pilotos_gustados.append(Piloto.objects.get(id=id))
            

    paises_votados = []
    temporadas_pilotosFavs = []
    mundiales_votados = []
    victorias_votados = []
    podios_votados = []
    for p in pilotos_gustados:
        paises_votados.append(p.pais)
        temporadas_pilotosFavs.append(len(p.temporadas.split(",")))
        mundiales_votados.append(0 if p.campeonatosMundiales.split(",")[0] == "" else len(p.campeonatosMundiales.split(",")))
        victorias_votados.append(p.victoriasHistorico)
        podios_votados.append(p.podiosHistorico)

    media_temporadas = mean(temporadas_pilotosFavs)
    media_mundiales = mean(mundiales_votados)
    media_victorias = mean(victorias_votados)
    media_podios = mean(podios_votados)

    valoraciones_no_votados = {}

    for piloto in Piloto.objects.all():
        puntuacionPiloto = 0
        if piloto not in pilotos_gustados: #Para no recomendar los que ya le gustan
            
            #Extra
            for equipoId in equipos_votados:
                #comprobación
                if EquiposYPilotos.objects.filter(piloto=piloto, equipo=Equipo.objects.get(id=equipoId)).exists():
                    #print(EquiposYPilotos.objects.get(piloto=piloto, equipo=Equipo.objects.get(id=equipoId)))
                    puntuacionPiloto+= ponderacion_equipos


            #pais
            if piloto.pais in paises_votados:
                puntuacionPiloto+=ponderacion_pais

            #longevidad
            longevidad = len(piloto.temporadas.split(","))
            #No añadimos el condicional porque media_temporadas como mínimo será siempre 1

            ponderacionMaximaTemporadas = ponderacion_longevidad
            proporcion_cercania = 1 - abs(longevidad - media_temporadas) / (2 * media_temporadas)
            puntuacionPiloto += ponderacionMaximaTemporadas * proporcion_cercania
            
            #mundiales
            mundiales = 0 if piloto.campeonatosMundiales.split(",")[0] == "" else len(piloto.campeonatosMundiales.split(","))
            if media_mundiales != 0: #Evitamos la division por 0
                ponderacionMaximaMundiales = ponderacion_mundiales
                proporcion_cercania_2 = 1 - abs(mundiales - media_mundiales) / (2 * media_mundiales)
                puntuacionPiloto += ponderacionMaximaMundiales * proporcion_cercania_2

            #victorias
            victorias = piloto.victoriasHistorico
            if media_victorias != 0:
                ponderacionMaximaVictorias = ponderacion_victorias
                proporcion_cercania_3 = 1 - abs(victorias - media_victorias) / (2 * media_victorias)
                puntuacionPiloto += ponderacionMaximaVictorias * proporcion_cercania_3

            #podios
            podios = piloto.podiosHistorico
            if media_podios != 0:
                ponderacionMaximaPodios = ponderacion_podios
                proporcion_cercania_4 = 1 - abs(podios - media_podios) / (2 * media_podios)
                puntuacionPiloto += ponderacionMaximaPodios * proporcion_cercania_4

            valoraciones_no_votados[piloto] = puntuacionPiloto

    recomendaciones_ordenadas = dict(sorted(valoraciones_no_votados.items(), key=lambda item: item[1], reverse=True))
    
    return list(recomendaciones_ordenadas.keys())[:12] #Devolvemos los 12 con más nota

### Función para equipos: similar para pilotos aún ###
# 
           
            
def recomienda_equipos(equipos_votados):

    #Transformamos las id en el objeto
    equipos_gustados = []
    for id in equipos_votados:
        equipos_gustados.append(Equipo.objects.get(id=id))

    paises_votados = []
    temporadas_equiposFavs = []
    mundiales_votados = []
    victorias_votados = []
    podios_votados = []
    for e in equipos_gustados:
        paises_votados.append(e.pais)
        temporadas_equiposFavs.append(len(e.temporadas.split(",")))
        mundiales_votados.append(0 if e.campeonatosMundiales.split(",")[0] == "" else len(e.campeonatosMundiales.split(",")))
        victorias_votados.append(e.victoriasHistorico)
        podios_votados.append(e.podiosHistorico)

    media_temporadas = mean(temporadas_equiposFavs)
    media_mundiales = mean(mundiales_votados)
    media_victorias = mean(victorias_votados)
    media_podios = mean(podios_votados)

    valoraciones_no_votados = {}

    for equipo in Equipo.objects.all():
        puntuacionEquipo = 0
        if equipo not in equipos_gustados: #Para no recomendar los que ya le gustan
            
            #pais
            if equipo.pais in paises_votados:
                puntuacionEquipo+=20

            #longevidad
            longevidad = len(equipo.temporadas.split(","))
            ponderacionMaximaTemporadas = 20
            proporcion_cercania = 1 - abs(longevidad - media_temporadas) / (2 * media_temporadas)
            puntuacionEquipo += ponderacionMaximaTemporadas * proporcion_cercania
            
            #mundiales
            mundiales = 0 if equipo.campeonatosMundiales.split(",")[0] == "" else len(equipo.campeonatosMundiales.split(","))
            ponderacionMaximaMundiales = 25
            proporcion_cercania_2 = 1 - abs(mundiales - media_mundiales) / (2 * media_mundiales)
            puntuacionEquipo += ponderacionMaximaMundiales * proporcion_cercania_2

            #victorias
            victorias = equipo.victoriasHistorico
            ponderacionMaximaVictorias = 20
            proporcion_cercania_3 = 1 - abs(victorias - media_victorias) / (2 * media_victorias)
            puntuacionEquipo += ponderacionMaximaVictorias * proporcion_cercania_3

            #podios
            podios = equipo.podiosHistorico
            ponderacionMaximaPodios = 15
            proporcion_cercania_4 = 1 - abs(podios - media_podios) / (2 * media_podios)
            puntuacionEquipo += ponderacionMaximaPodios * proporcion_cercania_4

            valoraciones_no_votados[equipo] = puntuacionEquipo

    recomendaciones_ordenadas = dict(sorted(valoraciones_no_votados.items(), key=lambda item: item[1], reverse=True))
    
    return list(recomendaciones_ordenadas.keys())[:9] #Devolvemos los 9 con más nota


    



