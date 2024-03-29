"""
URL configuration for FormulaWorld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from web import views
from scrapping import views as scrappingviews

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', views.landing, name="landing"),
    path('', views.landing, name="landing"),
    path('cargaBD/', scrappingviews.carga, name="cargaBD"),
   #path('cargaWhoosh/', scrappingviews.cargaWhoosh, name="cargaWhoosh"),
    path('terminos/', views.terminos, name="terminos"),
    path('gdpr/', views.gdpr, name="gdpr"),

    path('circuitos/', views.list_circuitos, name = "listaCircuitos"),
    path('circuito/<int:idEntrada>', views.detallesCircuito, name = "detallesCircuito"),

    path('temporadas/', views.list_temporadas, name= "listaTemporadas"),
    path('temporada/<int:anyoEntrada>', views.detallesTemporada, name = "detallesTemporada"),

    path('pilotos/', views.list_pilotos, name= "listaPilotos"),
    path('piloto/<int:idEntrada>', views.detallesPiloto, name = "detallesPiloto"),

    path('equipos/', views.list_equipos, name= "listaEquipos"),
    path('equipo/<int:idEntrada>', views.detallesEquipo, name = "detallesEquipo"),

    #Voto
    path('votar/<str:modelo>/<int:objeto_id>/', views.votar_objeto, name='votar_objeto'),

    path('', include("authentication.urls")),
    path('', include('sistema_recomendacion.urls')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)