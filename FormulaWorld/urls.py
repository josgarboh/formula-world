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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', views.landing, name="landing"),
    path('', views.landing, name="landing"),
    path('cargaBD/', scrappingviews.carga, name="cargaBD"),
   #path('cargaWhoosh/', scrappingviews.cargaWhoosh, name="cargaWhoosh"),

    path('circuitos/', views.list_circuitos, name = "listaCircuitos"),
    path('circuito/<int:idEntrada>', views.detallesCircuito),

    path('temporadas/', views.list_temporadas, name= "listaTemporadas"),
    path('temporada/<int:anyoEntrada>', views.detallesTemporada),

    path('', include("authentication.urls")),
]
