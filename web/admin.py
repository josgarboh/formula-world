from django.contrib import admin
from .models import Circuito, User, Temporada, Piloto, Equipo, EquiposYPilotos, Voto

# Register your models here.

admin.site.register(User)
admin.site.register(Circuito)
admin.site.register(Temporada)
admin.site.register(Piloto)
admin.site.register(Equipo)
admin.site.register(EquiposYPilotos)
admin.site.register(Voto)