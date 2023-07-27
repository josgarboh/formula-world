from django.shortcuts import render
from web.models import Circuito #,Temporada

# Create your views here.

def index(request):
    return render(request, 'home.html')
