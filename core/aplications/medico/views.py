from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .models import Especialidad,Horario,Medico
from aplications.authentication.models import CustomUser
from .serializers import EspecialidadSerializer,HorarioSerializer,MedicoSerializer,MedicoListSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def perform_create(self, serializer):
        # Obtenemos los datos de la solicitud
        doctor_id = self.request.data.get('doctor')
        dias_semana = self.request.data.get('dias_semana')
        hora_inicio = self.request.data.get('hora_inicio')
        hora_fin = self.request.data.get('hora_fin')

        # Buscamos si ya existe un horario para el mismo doctor
        horario_existente = Horario.objects.filter(doctor_id=doctor_id, dias_semana=dias_semana, hora_inicio=hora_inicio, hora_fin=hora_fin).first()

        if horario_existente:
            # Si existe, actualizamos el horario existente
            serializer.instance = horario_existente
            serializer.update(horario_existente, self.request.data)
        else:
            # Si no existe, creamos un nuevo horario
            serializer.save()

class Get_Horarios(ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = HorarioSerializer
    
    def get_queryset(self):
        # Obtener el parámetro de consulta 'id_medico' de la solicitud
        id_medico = self.request.query_params.get('id_medico')

        # Verificar si se proporcionó el parámetro 'id_medico'
        if id_medico is not None:
            # Filtrar los horarios por el id del médico proporcionado
            horarios = Horario.objects.filter(doctor=id_medico)
            return horarios
        else:
            # Si no se proporcionó 'id_medico', devolver una lista vacía
            return Horario.objects.none()

    def list(self, request, *args, **kwargs):
        # Obtener la consulta filtrada
        queryset = self.get_queryset()
        
        # Serializar los datos y devolver la respuesta
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)