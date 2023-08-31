from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from sistema_recomendacion import sistRecomendacion
from web.models import Circuito, Piloto, Equipo

def probando(request):
    if request.method=='POST':
        if 'Aceptar' in request.POST:
            sistRecomendacion.prueba()
            return render(request, 'prueba.html')
        else:
            return redirect("")
           
    return render(request, 'confirmacion.html')


@login_required
def recomendacion_circuitos(request):
    circuitos_votados = sistRecomendacion.organiza_votos_2(Circuito, request.user)
    recomendaciones = sistRecomendacion.recomienda_circuitos(circuitos_votados)
    return render(request, 'recomendacionCircuitos.html', {'recomendaciones':recomendaciones})

@login_required
def recomendacion_pilotos(request):
    pilotos_votados = sistRecomendacion.organiza_votos_2(Piloto, request.user)
    recomendaciones = sistRecomendacion.recomienda_pilotos(pilotos_votados)
    return render(request, 'recomendacionPilotos.html', {'recomendaciones':recomendaciones})

@login_required
def recomendacion_equipos(request):
    equipos_votados = sistRecomendacion.organiza_votos_2(Equipo, request.user)
    recomendaciones = sistRecomendacion.recomienda_equipos(equipos_votados)
    return render(request, 'recomendacionEquipos.html', {'recomendaciones':recomendaciones})
    


