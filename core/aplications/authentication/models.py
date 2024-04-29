from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
SEX_OPTIONS = (
        ('1', 'Masculino'),
        ('2', 'Femenimo'),
    )

class CustomUser(AbstractUser):
    id = models.CharField(max_length=100,primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=150,null=False)
    name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    sex = models.CharField(max_length=50, null=True,choices=SEX_OPTIONS)
    age =  models.CharField(max_length=2,null=True)
    phone = models.CharField(max_length=150,null=True)
    email = models.EmailField(max_length=200, unique=True)
    user_type = models.CharField(max_length=10, choices=(('PACIENTE', 'Paciente'), ('MEDICO', 'Médico')), null=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.get_full_name()}"

class CodesVerification(models.Model):
    changePasswordCode = models.CharField(max_length=10,unique=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL) 
    def __str__(self):
        return f"{self.user}"