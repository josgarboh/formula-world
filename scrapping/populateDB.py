import json
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil


from web.models import Circuito, Equipo, EquiposYPilotos, Piloto, Temporada
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID
from whoosh.qparser import QueryParser

from urllib.parse import urlencode
from urllib.parse import quote

from unidecode import unidecode

#Extraccion de todos los circuitos en los que se ha corrido un gran premio de F1 (1950-2023)
def extraer_circuitos():
    lista=[]
    
    url="https://es.wikipedia.org/wiki/Anexo:Circuitos_de_F%C3%B3rmula_1"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")      
    
    l = s.find("div", id="bodyContent").find("div", class_="mw-parser-output").find("table", class_="sortable")
    circuitos = l.tbody.find_all("tr")
    circuitos.pop(0) #La primera entrada es el índice de tabla: circuito,tipo,ubicacion,GP,temporadas,ediciones,mapa
    
    for c in circuitos:
        columnas = c.find_all("td")
        if len(columnas) == 7: #Las filas que no lo cumplen son lineas que representan un cambio de nombre en el GP pero siendo el mismo circuito, no las necesitamos
            
            #Nombre del Trazado
            nombre = columnas[0].a.string.strip()
            
            #Tipo
            if nombre == "Scandinavian Raceway": #Excepcion: Circuito con tipo "doble" autodromo-aerodromo:
                tipo = "Aeródromo"
            else:
                tipoSinUnificar = columnas[1].string.strip()
                tipo = unidecode(tipoSinUnificar).lower()
            
            #Excepcion: Variación del circuito de Indianapolis indistinguible por el nombre
            if nombre == ("Indianápolis") and tipo == "Autódromo":
                nombre = "Indianápolis (500 millas)"
            
            #País
            ubicacion = columnas[2].find_all("a")
            pais = ubicacion[len(ubicacion)-1].string.strip()    
            
            #Número de Grandes Premios
            edicionesDisputadas = int(columnas[5].string.strip())
            
            #Imagen del trazado
            enlaceImagen = "https://es.wikipedia.org"+ columnas[6].span.a['href']
            pagImagen = urllib.request.urlopen(enlaceImagen)
            sImg = BeautifulSoup(pagImagen,"lxml")
            imagen = sImg.find("div",id="file").a.img['src']
            
            #Distancia del circuito
            enlaceCircuito = "https://es.wikipedia.org" + columnas[0].a['href']
            pagCircuito = urllib.request.urlopen(enlaceCircuito)
            sCir = BeautifulSoup(pagCircuito,"lxml")
            longitud = sCir.find("table",class_="infobox").find("th", string="Longitud").find_next_sibling("td").text.strip().replace(",",".").replace(" km","")
            
            #Excepciones a tratar: Estoril, Indianápolis, Nelson Piquet, Nurburgring, Yeda
            if nombre=="Estoril":
                longitud = longitud.replace(" (4.182)", "")
            elif nombre=="Indianápolis":
                longitud = longitud.replace("4.023 (Oval) / ", "").replace(" (Road)", "")
            elif nombre=="Indianápolis (500 millas)":
                longitud = longitud.replace(" (Oval) / 4.192 (Road)", "")
            elif nombre =="Nelson Piquet":
                longitud = longitud[:4] #Solo contamos el primer valor
            elif nombre=="Nürburgring":
                longitud = longitud.replace("Nordschleife: 20.800GP-Strecke: ","") #El segundo valor es el del circuito tipo Fórmula 1
            elif nombre=="Yeda":
                #longitud = longitud.replace("[1]","")
                longitud = 6.175 # única longitud introducida a mano (da problemas con el casteo a float)
            
            lista.append((nombre,tipo,pais,edicionesDisputadas,float(longitud),imagen))
    print("Extracción de circuitos completada")
    return lista

#Extracción del mundial de pilotos de todas las temporadas de F1 desde 1950 hasta 2022
def extraer_temporadas():
    anyoComienzo = 1950
    anyoFinal = 2022
    ls = []

    for anyo in range(anyoComienzo, anyoFinal+1): #[)

        #Extra: Imagen histórica de cada temporada (campeón, coche dominante, etcétera)
        urlParaImagen="https://es.wikipedia.org/wiki/Temporada_" + str(anyo) + "_de_F%C3%B3rmula_1"
        f0 = urllib.request.urlopen(urlParaImagen)
        s0 = BeautifulSoup(f0,"lxml")
        imagen = s0.find("a", class_="mw-file-description").img['src']

        
        url="https://pitwall.app/seasons/"+ str(anyo) + "-formula-1-world-championship"
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        
        listaAnyo = []      
        tablaPilotos = s.find("div",id="driver-standings").table.tbody.find_all("tr")
        for fila in tablaPilotos:
            columnas = fila.find_all("td")

            posicion = columnas[0].text.strip()
            nombrePiloto = columnas[1].a.text.strip().lower()
            nombreEquipo = columnas[2].text.strip().lower()
            puntos = (columnas[5].text.strip())
            
            enCadena = posicion + "|" + nombrePiloto + "|" + nombreEquipo + "|" + puntos #se hace así para el esquema Whoosh
            listaAnyo.append(enCadena)
            
        parseoLista = ",".join(listaAnyo)        
        ls.append((anyo, parseoLista, imagen))
    
    print("Extracción de temporadas completada")   
    return ls

def extraer_pilotos():
    anyoComienzo=1950
    anyoFinal=2023
    lista=[]
    listaUrls=[] #La usaremos para no entrar en pilotos ya consultados    
    for anyo in range(anyoComienzo, anyoFinal+1): #range llega hasta 2023-1, por eso ponemos el +1
    
        url="https://pitwall.app/drivers/archive/"+str(anyo)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
       
        pilotos = s.find("table",class_="data-table").tbody.find_all("tr")
        for pil in pilotos:
            urlpiloto = "https://pitwall.app" + pil.td.a['href']
            if urlpiloto not in listaUrls:            
                listaUrls.append(urlpiloto) #url ya visitada
                fpiloto = urllib.request.urlopen(urlpiloto)
                spiloto = BeautifulSoup(fpiloto, "lxml")
                
                nombre = spiloto.find("div", id="breadcrumbs").find_all("span")[4].a.text.strip().lower()
                print(nombre) #mas o menos para llevar un conteo

                #ESCUDO (algunas vienen sin él)
                lugarImagen = spiloto.find("div", class_="image")
                if lugarImagen.img:
                    imagen = lugarImagen.img['src']
                else:
                    imagen = "/static/media/perfil-de-usuario.webp" #imagen predeterminada
    
                nacionalidad = spiloto.find("div", class_="overview-blocks").find_all("div",class_="value")[2].text.strip()
                pais = traduce_nacionalidades(nacionalidad)
    
                #campeonatosMundiales y temporadas
                temporadas=[]
                campeonatosMundiales = []
                filasTemporadas = spiloto.find("table", class_="data-table").tbody.find_all("tr")
                for temporada in filasTemporadas:
                    columnas = temporada.find_all("td")
                    temporadas.append(columnas[0].a.text) #lista con los años presente en F1
                    if columnas[1].text.strip() == "1st":
                        campeonatosMundiales.append(columnas[0].a.text)
    
                temporadasTexto = ",".join(temporadas)       
                campeonatosMundialesTexto = ",".join(campeonatosMundiales)
    
                #Seccion de victorias,podios,puntos
                seccionDatos = spiloto.find("div", id="show-driver").find_all("div", class_="section")[1].div.find_all("div", class_="stats-block")
                for dato in seccionDatos:
                    if dato.div.text.strip() == "Wins":
                        victoriasHistorico = int(dato.find_all("div")[1].text.strip())
                    elif dato.div.text.strip() == "Podiums":
                        podiosHistorico = int(dato.find_all("div")[1].text.strip())
                    elif dato.div.text.strip() == "Points":
                        puntosHistorico  = float(dato.find_all("div")[1].text.strip())
                
                lista.append((nombre,pais,imagen,victoriasHistorico,podiosHistorico,puntosHistorico,
                              temporadasTexto,campeonatosMundialesTexto))
    
    print("Se ha completado la extracción de Pilotos")
    print("Numero de pilotos: " + str(len(lista)))
    return lista

def extraer_escuderias():
    anyoComienzo=1950
    anyoFinal=2023
    lista=[]
    listaUrls=[] #La usaremos para no entrar en escuderías ya consultadas
    for anyo in range(anyoComienzo, anyoFinal+1): #range llega hasta 2023-1, por eso ponemos el +1
    
        url="https://pitwall.app/teams/archive/"+str(anyo)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
       
        escuderias = s.find("table",class_="data-table").tbody.find_all("tr")
        for esc in escuderias:
            urlEscuderia = "https://pitwall.app" + esc.td.a['href']
            if urlEscuderia not in listaUrls:            
                listaUrls.append(urlEscuderia) #url ya visitada
                fEscuderia = urllib.request.urlopen(urlEscuderia)
                sEscuderia = BeautifulSoup(fEscuderia, "lxml")
                               
                nombre = sEscuderia.find("div", class_="title").h1.text.strip().lower()
                print(nombre)
                
                #ESCUDO (algunas vienen sin él)
                lugarImagen = sEscuderia.find("div", class_="image")
                if lugarImagen.img:
                    imagen = lugarImagen.img['src']
                else:
                    imagen = "/static/media/Imagen_no_disponible.png"
                
                nacionalidad = sEscuderia.find("div", class_="stats-block").find_all("div")[1].text.strip()
                pais = traduce_nacionalidades(nacionalidad)
                
                #campeonatosMundiales y temporadas
                temporadas=[]
                campeonatosMundiales = []
                filasTemporadas = sEscuderia.find("table", class_="data-table").tbody.find_all("tr")
                for temporada in filasTemporadas:
                    columnas = temporada.find_all("td")
                    temporadas.append(columnas[0].a.text) #lista con los años presente en F1
                    if columnas[1].text.strip() == "1st":
                        campeonatosMundiales.append(columnas[0].a.text)
                        
                temporadasTexto = ",".join(temporadas)       
                campeonatosMundialesTexto = ",".join(campeonatosMundiales)
                
                secciones = sEscuderia.find("div", id="show-constructor").find_all("div", class_="section")
                
                #Seccion de victorias,podios,puntos
                seccionDatos = secciones[1].div.find_all("div", class_="stats-block")
                victoriasHistorico = int(seccionDatos[3].find("div",class_="value").text)
                podiosHistorico    = int(seccionDatos[5].find("div",class_="value").text)
                puntosHistorico  = float(seccionDatos[6].find("div",class_="value").text)
                
                #Pilotos: debemos hacer distinción entre escuderías activas (una sección más) y retiradas
                pilotos=[] #No se repetirán porque unicamente entramos una vez en cada escudería
                if len(secciones) == 3: #Escudería "vieja"
                    filasPilotos = secciones[2].table.tbody.find_all("tr")
                    for fila in filasPilotos:
                        pilotos.append(fila.find_all("td")[0].a.text.lower())
                        
                else: #escudería activa
                    filasPilotos1 = secciones[2].table.tbody.find_all("tr")
                    filasPilotos2 = secciones[3].table.tbody.find_all("tr")
                    for fila in filasPilotos1:
                        pilotos.append(fila.find_all("td")[0].a.text.strip().lower())
                    for fila in filasPilotos2:
                        pilotos.append(fila.find_all("td")[0].a.text.strip().lower())
                
                pilotosTexto = ",".join(pilotos)
                
                lista.append((nombre,pais,imagen,victoriasHistorico,podiosHistorico,puntosHistorico,
                              temporadasTexto,campeonatosMundialesTexto,pilotosTexto))
                
    print("Se ha completado la extracción de Escuderías")
    return lista

#Traducción de gentilicios en inglés a paises en español
def traduce_nacionalidades(nacionalidad):
    mapeo = {
        "Spanish": "España",
        "British": "Gran Bretaña",
        "Irish": "Irlanda",
        "French": "Francia",
        "German": "Alemania",
        "East German": "Alemania",
        "Italian": "Italia",
        "American": "Estados Unidos",
        "American-Italian":"Estados Unidos e Italia",
        "Australian": "Australia",
        "Canadian": "Canadá",
        "Japanese": "Japón",
        "Brazilian": "Brasil",
        "Mexican": "México",
        "Argentinian": "Argentina",
        "Argentine":"Argentina",
        "Argentine-Italian":"Argentina e Italia",
        "Dutch": "Países Bajos",
        "Belgian": "Bélgica",
        "Belgium":"Bélgica",
        "Swiss": "Suiza",
        "Austrian": "Austria",
        "Russian": "Rusia",
        "Rhodesian":"República de Rodesia",
        "Chinese": "China",
        "Indian": "India",
        "Swedish": "Suecia",
        "Danish": "Dinamarca",
        "Finnish": "Finlandia",
        "Norwegian": "Noruega",
        "Portuguese": "Portugal",
        "South African": "Sudáfrica",
        "Korean": "Corea del Sur",
        "Monegasque": "Mónaco",
        "New Zealander": "Nueva Zelanda",
        "Venezuelan": "Venezuela",
        "Colombian": "Colombia",
        "Chilean": "Chile",
        "Polish": "Polonia",
        "Hungarian": "Hungría",
        "Romanian": "Rumania",
        "Czech": "República Checa",
        "Singaporean": "Singapur",
        "Malaysian": "Malasia",
        "Indonesian": "Indonesia",
        "Thai": "Tailandia",
        "Turkish": "Turquía",
        "Greek": "Grecia",
        "Israeli": "Israel",
        "Iranian": "Irán",
        "Egyptian": "Egipto",
        "Uruguayan": "Uruguay",
        "Liechtensteiner":"Liechtenstein",
        "New Zealand": "Nueva Zelanda",
        "Hong Kong": "Hong Kong",
    }

    if nacionalidad in mapeo.keys():
        return(mapeo.get(nacionalidad))
    else:
        return("Sin traducción: " + str(nacionalidad))

#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDB():
    #variables para contar el número de registros que vamos a almacenar
    num_circuitos = 0
    num_temporadas = 0
    num_equipos = 0
    num_pilotos = 0   
    
    #borramos todas las tablas de la BD
    Circuito.objects.all().delete()
    Temporada.objects.all().delete()
    Equipo.objects.all().delete()
    Piloto.objects.all().delete()
    EquiposYPilotos.objects.all().delete()

    listaCircuitos= extraer_circuitos()
    num_circuitos = 1
    for circuito in listaCircuitos:
        if not Circuito.objects.filter(nombre=circuito[0]).exists():

            c = Circuito.objects.create(id=num_circuitos, nombre= circuito[0], tipo = circuito[1], pais = circuito[2],
                                     edicionesDisputadas = circuito[3], longitud = circuito[4],
                                       imagen=circuito[5])
            
            c.save()
            num_circuitos = num_circuitos + 1
    
    print("Se ha completado el poblado de Circuitos")

    listaTemporadas=extraer_temporadas()
    num_temporadas=1 #para las ID
    for temporada in listaTemporadas:
        if not Temporada.objects.filter(anyo=temporada[0]).exists():

            dicccionarioTemporada = dict()            
            for infoPiloto in temporada[1].split(","): #Cadena del tipo: Piloto|Equipo|puntosPiloto,Piloto|...
                posicion, nombre, equipo, puntosPiloto = infoPiloto.split("|")
                dicccionarioTemporada[posicion]= {"nombre": nombre, "equipo": equipo, "puntosPiloto": float(puntosPiloto)}

            datos_json = json.dumps(dicccionarioTemporada)#, indent=4)

            t = Temporada.objects.create(id=num_temporadas, anyo=temporada[0], tablaPilotos=datos_json,
                                         imagenHistorica=temporada[2])
            t.save()
            num_temporadas = num_temporadas + 1

    print("Se ha completado el poblado de Temporadas")

    listaEquipos= extraer_escuderias()
    num_equipos = 1
    for equipo in listaEquipos:
        if not Equipo.objects.filter(nombre=equipo[0]).exists():
            e = Equipo.objects.create(id=num_equipos, nombre= equipo[0], pais = equipo[1], imagen = equipo[2],
                                     victoriasHistorico = equipo[3], podiosHistorico = equipo[4],
                                     puntosHistorico = equipo[5], temporadas = equipo[6],
                                     campeonatosMundiales = equipo[7]) #pilotos = equipo[8]
            
            e.save()
            num_equipos = num_equipos + 1
    
    print("Se ha completado el poblado de Equipos")

    listaPilotos= extraer_pilotos()
    num_pilotos = 1
    for piloto in listaPilotos:
        if not Piloto.objects.filter(nombre=piloto[0]).exists():
            p = Piloto.objects.create(id=num_pilotos, nombre= piloto[0], pais = piloto[1], imagen = piloto[2],
                                     victoriasHistorico = piloto[3], podiosHistorico = piloto[4],
                                     puntosHistorico = piloto[5], temporadas = piloto[6],
                                     campeonatosMundiales = piloto[7])
            
            p.save()
            num_pilotos = num_pilotos + 1
    print("Se ha completado el poblado de Pilotos")

    ###############MANY TO MANY EQUIPOSYPILOTOS ##################

    for datos in listaEquipos:
        equipo = Equipo.objects.get(nombre=datos[0])
        pilotosStr = datos[8].split(",")
        for nombrePiloto in pilotosStr:
            print(nombrePiloto)
            piloto = Piloto.objects.get(nombre=nombrePiloto)
            EquiposYPilotos.objects.create(piloto=piloto, equipo=equipo)
    
    print("Relación entre equipos y pilotos poblada")

    print("Poblado de la base de datos completado")
    return (num_circuitos-1, num_temporadas-1, num_equipos-1, num_pilotos-1)


def populateWhooshCircuitos():
    
    #define el esquema de la información
    schem = Schema(idCircuito=NUMERIC(stored=True), nombre=TEXT(stored=True,phrase=False), tipo=KEYWORD(stored=True,lowercase=True), pais=KEYWORD(stored=True), edicionesDisputadas=NUMERIC(stored=True,numtype=int), longitud=NUMERIC(stored=True,numtype=float), imagen=TEXT(stored=True,phrase=True))

    #eliminamos el directorio del índice, si existe
    if os.path.exists("IndexCircuitos"):
        shutil.rmtree("IndexCircuitos")
    os.mkdir("IndexCircuitos")

    #creamos el índice
    ix = create_in("IndexCircuitos", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    numCircuitos=1
    lista=extraer_circuitos()
    for circuito in lista:
        #añade cada circuito de la lista al índice
        writer.update_document(idCircuito = numCircuitos, nombre=str(circuito[0]), tipo=str(circuito[1]), pais=str(circuito[2]), edicionesDisputadas=int(str(circuito[3])), longitud=float(str(circuito[4])), imagen=str(circuito[5]))    
        numCircuitos +=1
    writer.commit()
    print("Carga de Whoosh de circuitos completada con éxito")

    return numCircuitos-1

def populateWhooshTemporadas():
    #define el esquema de la información
    schem = Schema(idTemporada=NUMERIC(stored=True), anyo=NUMERIC(stored=True,numtype=int), datos=KEYWORD(stored=True,commas=True,lowercase=True), imagen=TEXT(stored=True,phrase=True))

    #eliminamos el directorio del índice, si existe
    if os.path.exists("IndexTemporadas"):
        shutil.rmtree("IndexTemporadas")
    os.mkdir("IndexTemporadas")

    #creamos el índice
    ix = create_in("IndexTemporadas", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    numTemporadas=1
    lista=extraer_temporadas()
    for t in lista:
        #añade cada temporada de la lista al índice
        writer.update_document(idTemporada=numTemporadas, anyo=int(str(t[0])), datos=str(t[1]), imagen=str(t[2]))    
        numTemporadas+=1
    writer.commit()
    print("Carga de Whoosh de temporadas completada con éxito")

    return numTemporadas-1

## TODO: POPULATEWHOOSH PILOTOS Y EQUIPOS