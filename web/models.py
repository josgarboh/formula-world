from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator



class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.username
    

#Clase generica, para poder votar en Circuitos, temporadas... etcétera
class Voto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    #ContentType nos permitirá elegir si tratamos circuito, temporada...
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    objeto_votado = GenericForeignKey('content_type', 'object_id') #recibe el tipo y su id, así lo identifica

    me_gusta = models.BooleanField(default=False)

    #luego obtenemos usuario y objeto_votado en la vista que lo requiera

    def __str__(self):
        if self.me_gusta == True:
            return  f"{self.usuario.username} - Voto para {self.content_type } - {self.object_id} - {self.objeto_votado}"


class Temporada(models.Model):
    id = models.IntegerField(primary_key=True)
    anyo = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1950), MaxValueValidator(2023)])
    tablaPilotos = models.JSONField(blank=False, null=False)
    imagenHistorica = models.URLField(validators=[URLValidator()])

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

    votos = GenericRelation(Voto)
    
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
    imagen = models.URLField(validators=[URLValidator()])
    
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
    imagen = models.URLField(validators=[URLValidator()])
    temporadas = models.CharField(max_length=200, blank=True, null=True)

    #equipos = models.ManyToManyField(Equipo, blank=False, through='EquiposYPilotos')

    def __str__(self):
        return self.nombre
    
    def listaCampeonatosMundiales(self):
        return self.campeonatosMundiales.split(",")
    
    # Hay que hacer una pequeña correción para que pilotos con 0 mundiales no tengan 1
    def numeroMundiales(self):
        return 0 if self.listaCampeonatosMundiales[0] == "" else len(self.listaCampeonatosMundiales)
    
    def listaTemporadas(self):
        return self.temporadas.split(',')
    
    def equipos_asociados(self):
        return Equipo.objects.filter(equiposypilotos__piloto=self)

class EquiposYPilotos(models.Model):
    piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    #temporadas = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.piloto.nombre} ({self.piloto.id}) - {self.equipo.nombre } ({self.equipo.id})"



