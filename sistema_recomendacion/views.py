from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from sistema_recomendacion import sistRecomendacion
from web.models import Circuito

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
    


