
from django.shortcuts import redirect, render
from scrapping import populateDB


def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:
            num_circuitos,num_temporadas,num_equipos,num_pilotos = populateDB.populateDB()
            
            mensaje ="Se han almacenado: " + str(num_circuitos) +" circuitos, " +str(num_temporadas) + " temporadas, " + str(num_equipos) + " equipos y " + str(num_pilotos) + " pilotos."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("")
           
    return render(request, 'confirmacion.html')


# Posponemos las consultas de Whoosh hasta que no completemos el sistema de puntuación y el de recomendación

# def cargaWhoosh(request):

#     if request.method=='POST':
#         if 'Aceptar' in request.POST:
#             numCircuitos = populateDB.populateWhooshCircuitos()
#             numTemporadas = populateDB.populateWhooshTemporadas()

#             mensaje="Se ha cargado el esquema Whoosh correctamente con " + str(numCircuitos) +" circuitos y" +str(numTemporadas) + " temporadas."
#             return render(request, 'cargaWhoosh.html', {'mensaje':mensaje})
#         else:
#             return redirect("/")
           
#     return render(request, 'confirmacion.html')