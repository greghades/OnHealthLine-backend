from django.db import models
from aplications.paciente.models import Paciente
# Create your models here.

class Suscripcion(models.Model):
    cedula_paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50,verbose_name="Tipo Suscripcion")
    precio = models.FloatField(max_length=25,verbose_name="Precio")
    fecha_inicio = models.DateField()
    fecha_vecimiento = models.DateField()
    status = models.BooleanField()

