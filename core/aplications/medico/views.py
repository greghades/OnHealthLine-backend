from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .models import Especialidad,Horario,Medico
from aplications.authentication.models import CustomUser
from .serializers import EspecialidadSerializer,HorarioSerializer,MedicoSerializer,MedicoListSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class ListAllDoctors(ListAPIView):
    serializer_class = MedicoListSerializer
    queryset = Medico.objects.all()
    

class Get_Especialidades(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EspecialidadSerializer
    queryset = Especialidad.objects.all()


class Create_Horario(CreateAPIView):
    serializer_class = HorarioSerializer
    model = Horario

class Get_Horarios(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = HorarioSerializer
    
    def get_queryset(self):

        horarios = Horario.objects.filter(doctor=self.request.user.id)

        return horarios