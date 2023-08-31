from django.urls import include, path
from sistema_recomendacion import views


urlpatterns = [
    path("prueba/", views.probando),
    path("recomendacionCircuitos/", views.recomendacion_circuitos, name="recomendacionCircuitos"),

]