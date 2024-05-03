from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Especialidad
from .serializers import EspecialidadSerializer
# Create your views here.


class Get_Especialidades(ListAPIView):
    serializer_class = EspecialidadSerializer
    queryset = Especialidad.objects.all()


