from django.db import models
from aplications.authentication.models import CustomUser

from django.contrib.postgres.fields import ArrayField

from aplications.paciente.models import Paciente
# Create your models here.


class Especialidad(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"{self.name}"

class Medico(models.Model):
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    paciente = models.ManyToManyField(Paciente,blank=True)
    descripcion =  models.TextField(max_length=700)



class Horario(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #dia = models.DateField()
    titulo = models.TextField(max_length=200,null=True, blank=True)
    descripcion = models.TextField(max_length=500,null=True, blank=True)
    dias_semana =  ArrayField(models.CharField(max_length=120, null=True, blank=True), null=True, blank=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    # def __str__(self):
    #     return f"{self.doctor} - {self.dias_semana} - {self.hora_inicio} a {self.hora_fin}"