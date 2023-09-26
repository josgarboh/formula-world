from django import forms

class PonderacionesForm(forms.Form):
    ponderacion_tipo = forms.FloatField(
        label='...el tipo del circuito? Dale un valor de 0 a 5',
        min_value=0, max_value=5,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_longitud = forms.FloatField(
        label='...la longitud del circuito? Dale un valor de 0 a 5',
        min_value=0, max_value=5,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    ponderacion_ediciones = forms.FloatField(
        label='...el número de ediciones disputadas en el circuito? Dale un valor de 0 a 5',
        min_value=0, max_value=5,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
