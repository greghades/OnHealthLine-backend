from django.db import models
from aplications.authentication.models import CustomUser
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



