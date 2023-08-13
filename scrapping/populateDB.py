import json
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil

from django.shortcuts import redirect, render
from web.models import Circuito, Temporada
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
        url="https://pitwall.app/seasons/"+ str(anyo) + "-formula-1-world-championship"
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        
        listaAnyo = []      
        tablaPilotos = s.find("div",id="driver-standings").table.tbody.find_all("tr")
        for fila in tablaPilotos:
            columnas = fila.find_all("td")

            nombrePiloto = columnas[1].a.text.strip().lower()
            nombreEquipo = columnas[2].text.strip().lower()
            puntos = (columnas[5].text.strip())
            
            enCadena = nombrePiloto + "|" + nombreEquipo + "|" + puntos #se hace así para el esquema Whoosh
            listaAnyo.append(enCadena)
            
        parseoLista = ",".join(listaAnyo)        
        ls.append((anyo, parseoLista))
    
    print("Extracción de temporadas completada")   
    return ls



#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDB():
    #variables para contar el número de registros que vamos a almacenar
    num_circuitos = 0
    num_temporadas = 0
    
    #borramos todas las tablas de la BD
    Circuito.objects.all().delete()
    Temporada.objects.all().delete()

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
                nombre, equipo, puntosPiloto = infoPiloto.split("|")
                dicccionarioTemporada[nombre]= {"equipo": equipo, "puntosPiloto": float(puntosPiloto)}

            datos_json = json.dumps(dicccionarioTemporada)#, indent=4)

            t = Temporada.objects.create(id=num_temporadas, anyo=temporada[0], tablaPilotos=datos_json)
            t.save()
            num_temporadas = num_temporadas + 1

    print("Se ha completado el poblado de Temporadas")

    print("Poblado de la base de datos completado")
    return (num_circuitos-1, num_temporadas-1)


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
    schem = Schema(idTemporada=NUMERIC(stored=True), anyo=NUMERIC(stored=True,numtype=int), datos=KEYWORD(stored=True,commas=True,lowercase=True))

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
        writer.update_document(idTemporada=numTemporadas, anyo=int(str(t[0])), datos=str(t[1]))    
        numTemporadas+=1
    writer.commit()
    print("Carga de Whoosh de temporadas completada con éxito")

    return numTemporadas-1