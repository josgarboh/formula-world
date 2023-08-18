from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator


class Temporada(models.Model):
    id = models.IntegerField(primary_key=True)
    anyo = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1950), MaxValueValidator(2023)])
    tablaPilotos = models.JSONField(blank=False, null=False)

    def __str__(self):
        return self.anyo
    

class Circuito(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    tipo = models.CharField(max_length=25, blank=False, null=False)
    pais = models.CharField(max_length=50, blank=False, null=False)
    edicionesDisputadas = models.IntegerField(blank=False, null=False)
    longitud = models.FloatField(blank=False, null=False)
    imagen = models.URLField(validators=[URLValidator()])
    
    def __str__(self):
        return self.nombre 

class Equipo(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    pais = models.CharField(max_length=50, blank=False, null=False)
    victoriasHistorico = models.IntegerField(blank=False, null=False)
    podiosHistorico = models.IntegerField(blank=False, null=False)
    puntosHistorico = models.FloatField(blank=False, null=False)
    campeonatosMundiales = models.CharField(max_length=200, blank=True, null=True)
    temporadas = models.CharField(max_length=200, blank=False, null=False)
    imagen = models.URLField(null=True, validators=[URLValidator()])
    
    #pilotos = models.ManyToManyField(Piloto, blank=False)

    def __str__(self):
        return self.nombre
    
    def listaCampeonatosMundiales(self):
        return self.campeonatosMundiales.split(",")
    
    def listaTemporadas(self):
        return self.temporadas.split(",")
    
    # def listaPilotos(self):
    #     return self.pilotos.split(",")
    
class Piloto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    pais = models.CharField(max_length=50, blank=False, null=False)
    victoriasHistorico = models.IntegerField(blank=False, null=False)
    podiosHistorico = models.IntegerField(blank=False, null=False)
    puntosHistorico = models.FloatField(blank=False, null=False)
    campeonatosMundiales = models.CharField(max_length=200, blank=True, null=True)
    imagen = models.URLField(null=True, validators=[URLValidator()])
    temporadas = models.CharField(max_length=200, blank=True, null=True)

    #equipos = models.ManyToManyField(Equipo, blank=False, through='EquiposYPilotos')

    def __str__(self):
        return self.nombre
    
    def listaCampeonatosMundiales(self):
        return self.campeonatosMundiales.split(",")

class EquiposYPilotos(models.Model):
    piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    #temporadas = models.CharField(max_length=200)

    def __str__(self):
        return self.piloto.__str__ + " - " + self.equipo.__str__


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.username