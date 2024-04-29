from django.db import models
from aplications.authentication.models import CustomUser
# Create your models here.
class Paciente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True,null=True)    
    address = models.CharField(max_length=150,null=True)