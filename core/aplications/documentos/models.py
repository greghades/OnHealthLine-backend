from django.db import models
from aplications.paciente.models import Paciente
from aplications.medico.models import Medico

TYPE_DOCUMENT_OPTIONS = (
        ('1', 'Analisis'),
        ('2', 'Radiografias'),
        ('3','Ecografías'),
        ('4', 'Tomografías computarizadas'),
        ('5','Resonancias magnéticas'),
    )


# Create your models here.
class Documento_Medico(models.Model):
    cedula_paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50,verbose_name="Tipo Dumento",choices=TYPE_DOCUMENT_OPTIONS)
    fecha_emicion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    url = models.URLField()


class Resultado_Medico(models.Model):
    cedula_paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    cadula_doctor = models.ForeignKey(Medico,on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50,verbose_name="Tipo Dumento",choices=TYPE_DOCUMENT_OPTIONS)
    fecha_emicion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    url = models.URLField()
