
from django.shortcuts import redirect, render
from scrapping import populateDB


def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:
            num_circuitos,num_temporadas = populateDB.populateDB()
            
            mensaje ="Se han almacenado: " + str(num_circuitos) +" circuitos y " +str(num_temporadas) + " temporadas."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("")
           
    return render(request, 'confirmacion.html')

  
def cargaWhoosh(request):

    if request.method=='POST':
        if 'Aceptar' in request.POST:
            numCircuitos = populateDB.populateWhooshCircuitos()
            numTemporadas = populateDB.populateWhooshTemporadas()

            mensaje="Se ha cargado el esquema Whoosh correctamente con " + str(numCircuitos) +" circuitos y" +str(numTemporadas) + " temporadas."
            return render(request, 'cargaWhoosh.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')