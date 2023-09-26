from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from sistema_recomendacion import sistRecomendacion
from sistema_recomendacion.forms import PonderacionesCircuitoForm, PonderacionesEquipoForm, PonderacionesPilotoForm
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
                form = PonderacionesCircuitoForm(request.POST)
                if form.is_valid():
                    ponderacion_tipo = form.cleaned_data['ponderacion_tipo']
                    ponderacion_longitud = form.cleaned_data['ponderacion_longitud']
                    ponderacion_ediciones = form.cleaned_data['ponderacion_ediciones']

                    # Llama a la función con las ponderaciones proporcionadas por el usuario
                    recomendaciones = sistRecomendacion.recomienda_circuitos(circuitos_votados, ponderacion_tipo, ponderacion_longitud, ponderacion_ediciones)
                else:
                    # Si el formulario no es válido no permite enviarlo
                    form = PonderacionesCircuitoForm()
        else:
            form = PonderacionesCircuitoForm()  # Crea un formulario en blanco si es una solicitud GET
   
        return render(request, 'recomendacionCircuitos.html', {'recomendaciones':recomendaciones,
                                                               'form': form})


@login_required
def recomendacion_pilotos(request):
    pilotos_votados = sistRecomendacion.organiza_votos_2(Piloto, request.user)
    equipos_votados = sistRecomendacion.organiza_votos_2(Equipo, request.user) #EXTRA: si el piloto ha estado en alguno de sus equipos favs sumará

    if not pilotos_votados:
        return render(request, 'recomendacionPilotos.html')
    else:
        recomendaciones = sistRecomendacion.recomienda_pilotos(pilotos_votados, equipos_votados)

        #Procesamos las ponderaciones
        if request.method == 'POST':
                form = PonderacionesPilotoForm(request.POST)
                if form.is_valid():
                    ponderacion_equipos = form.cleaned_data['ponderacion_equipos']
                    ponderacion_pais = form.cleaned_data['ponderacion_pais']
                    ponderacion_longevidad = form.cleaned_data['ponderacion_longevidad']
                    ponderacion_mundiales = form.cleaned_data['ponderacion_mundiales']
                    ponderacion_victorias = form.cleaned_data['ponderacion_victorias']
                    ponderacion_podios = form.cleaned_data['ponderacion_podios']

                    # Llama a la función con las ponderaciones proporcionadas por el usuario
                    recomendaciones = sistRecomendacion.recomienda_pilotos(pilotos_votados, equipos_votados,ponderacion_equipos,
                       ponderacion_pais,ponderacion_longevidad,ponderacion_mundiales,
                       ponderacion_victorias,ponderacion_podios)
                    
                else:
                    # Si el formulario no es válido no permite enviarlo
                    form = PonderacionesPilotoForm()
        else:
            form = PonderacionesPilotoForm()  # Crea un formulario en blanco si es una solicitud GET

        return render(request, 'recomendacionPilotos.html', {'recomendaciones':recomendaciones,
                                                             'form': form})


@login_required
def recomendacion_equipos(request):
    equipos_votados = sistRecomendacion.organiza_votos_2(Equipo, request.user)
    pilotos_votados = sistRecomendacion.organiza_votos_2(Piloto, request.user)

    if not equipos_votados:
        return render(request, 'recomendacionEquipos.html')
    else:
        recomendaciones = sistRecomendacion.recomienda_equipos(equipos_votados, pilotos_votados)

        #Procesamos las ponderaciones
        if request.method == 'POST':
                form = PonderacionesEquipoForm(request.POST)
                if form.is_valid():
                    ponderacion_pilotos = form.cleaned_data['ponderacion_pilotos']
                    ponderacion_pais = form.cleaned_data['ponderacion_pais']
                    ponderacion_longevidad = form.cleaned_data['ponderacion_longevidad']
                    ponderacion_mundiales = form.cleaned_data['ponderacion_mundiales']
                    ponderacion_victorias = form.cleaned_data['ponderacion_victorias']
                    ponderacion_podios = form.cleaned_data['ponderacion_podios']

                    # Llama a la función con las ponderaciones proporcionadas por el usuario
                    recomendaciones = sistRecomendacion.recomienda_equipos(equipos_votados, pilotos_votados,ponderacion_pilotos,
                       ponderacion_pais,ponderacion_longevidad,ponderacion_mundiales,
                       ponderacion_victorias,ponderacion_podios)
                    
                else:
                    # Si el formulario no es válido no permite enviarlo
                    form = PonderacionesEquipoForm()
        else:
            form = PonderacionesEquipoForm()  # Crea un formulario en blanco si es una solicitud GET


        return render(request, 'recomendacionEquipos.html', {'recomendaciones':recomendaciones,
                                                             'form':form})
    


