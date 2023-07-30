from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import URLValidator

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
    

class User(AbstractUser):
    id = models.AutoField(primary_key=True)