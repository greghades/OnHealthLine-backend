from django.db import models
from aplications.medico.models import Medico
from aplications.paciente.models import Paciente
# Create your models here.
class Cita_Medica(models.Model):
    cedula_paciente = models.ForeignKey(Paciente,verbose_name="Cedula Paciente",on_delete=models.CASCADE)
    cedula_doctor = models.ForeignKey(Medico,verbose_name="Cedula Doctor",on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    status = models.BooleanField()
    