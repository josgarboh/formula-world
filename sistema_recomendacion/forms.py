from django import forms

class PonderacionesCircuitoForm(forms.Form):
    ponderacion_tipo = forms.FloatField(
        label='...el tipo del circuito? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=5,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_longitud = forms.FloatField(
        label='...la longitud del circuito? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=4,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_ediciones = forms.FloatField(
        label='...el número de ediciones disputadas en el circuito? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=2,
        widget=forms.NumberInput(attrs={'step': '1'})
    )

class PonderacionesPilotoForm(forms.Form):
    ponderacion_equipos = forms.FloatField(
        label='...que el piloto haya estado en alguno de tus equipos favoritos? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=3,        
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_pais = forms.FloatField(
        label='...que el país del piloto coincida con el país de tus pilotos favoritos? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=4,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_longevidad = forms.FloatField(
        label='...la longevidad de la carrera del piloto? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=2,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_mundiales = forms.FloatField(
        label='...el número de campeonatos ganados? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=3,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_victorias = forms.FloatField(
        label='...el número de victorias? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=2,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_podios = forms.FloatField(
        label='...el número de podios? Dale un valor de 0 a 5',
        min_value=0, max_value=5, initial=1,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
