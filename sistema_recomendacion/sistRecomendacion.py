from math import sqrt
from statistics import mean
from web.models import Voto, User, Circuito
from django.contrib.contenttypes.models import ContentType

# def prueba():
#     print(Voto.objects.all())
#     print("Esto es un mensaje")
#     print(User.objects.all())


# SISTEMA DE RECOMENDACIÓN BASADO EN CONTENIDO #

# Objetivo: {Usuario: [id1,id2...]}
# Habrá un diccionario por modelo (vistas separadas)

def organiza_votos(modelo):
    diccionario = {}
    for usuario in User.objects.all():
        votosUsuario = []
        votosModelo = Voto.objects.filter(usuario=usuario, content_type=ContentType.objects.get_for_model(modelo))
        for voto in votosModelo:
            votosUsuario.append(voto.object_id) #añadimos el id del objeto (del modelo concreto) votado
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
def recomienda_circuitos(circuitos_votados):
    recomendaciones = []

    #Transformamos las id en los objetos concretos:
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
                puntuacionCircuito+=4 #lo que más suma

            #longitud
            longitud = circuito.longitud
            ponderacionMaximaLongitud = 4
            proporcion_cercania = 1 - abs(longitud - media_longitud) / (2 * media_longitud)
            puntuacionCircuito += ponderacionMaximaLongitud * proporcion_cercania

            #edicionesDisputadas
            ediciones = circuito.edicionesDisputadas
            ponderacionMaximaEdiciones = 2
            proporcion_cercania_2 = 1 - abs(ediciones - media_ediciones) / (2 * media_ediciones)
            puntuacionCircuito += ponderacionMaximaEdiciones * proporcion_cercania_2

            valoraciones_no_votados[circuito] = puntuacionCircuito

    recomendaciones_ordenadas = dict(sorted(valoraciones_no_votados.items(), key=lambda item: item[1], reverse=True))
    
    return list(recomendaciones_ordenadas.keys())[:15] #Devolvemos los 15 con más nota

            
            



    



