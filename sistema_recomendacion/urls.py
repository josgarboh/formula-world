from django.urls import include, path
from sistema_recomendacion import views


urlpatterns = [
    path("prueba/", views.probando),
    path("recomendacionCircuitos/", views.recomendacion_circuitos, name="recomendacionCircuitos"),
    path("recomendacionPilotos/", views.recomendacion_pilotos, name="recomendacionPilotos"),
    path("recomendacionEquipos/", views.recomendacion_equipos, name="recomendacionEquipos")

]