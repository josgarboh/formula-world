from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from sistema_recomendacion import sistRecomendacion
from sistema_recomendacion.forms import PonderacionesForm
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
    if not circuitos_votados: #No ha votado ninguno, no mostraremos nada
        return render(request, 'recomendacionCircuitos.html')

    else:
        recomendaciones = sistRecomendacion.recomienda_circuitos(circuitos_votados) #por defecto

        #Procesamos las ponderaciones
        if request.method == 'POST':
                form = PonderacionesForm(request.POST)
                if form.is_valid():
                    ponderacion_tipo = form.cleaned_data['ponderacion_tipo']
                    ponderacion_longitud = form.cleaned_data['ponderacion_longitud']
                    ponderacion_ediciones = form.cleaned_data['ponderacion_ediciones']

                    # Llama a la función con las ponderaciones proporcionadas por el usuario
                    recomendaciones = sistRecomendacion.recomienda_circuitos(circuitos_votados, ponderacion_tipo, ponderacion_longitud, ponderacion_ediciones)
                else:
                    # El formulario no es válido, maneja el error o muestra un mensaje al usuario
                    print('jajano')
        else:
            form = PonderacionesForm()  # Crea un formulario en blanco si es una solicitud GET
   
        return render(request, 'recomendacionCircuitos.html', {'recomendaciones':recomendaciones,
                                                               'form': form})

@login_required
def recomendacion_pilotos(request):
    pilotos_votados = sistRecomendacion.organiza_votos_2(Piloto, request.user)
    if not pilotos_votados:
        return render(request, 'recomendacionPilotos.html')
    else:
        recomendaciones = sistRecomendacion.recomienda_pilotos(pilotos_votados)
        return render(request, 'recomendacionPilotos.html', {'recomendaciones':recomendaciones})

@login_required
def recomendacion_equipos(request):
    equipos_votados = sistRecomendacion.organiza_votos_2(Equipo, request.user)
    if not equipos_votados:
        return render(request, 'recomendacionEquipos.html')
    else:
        recomendaciones = sistRecomendacion.recomienda_equipos(equipos_votados)
        return render(request, 'recomendacionEquipos.html', {'recomendaciones':recomendaciones})
    


