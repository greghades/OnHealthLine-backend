from rest_framework.fields import CharField,ListField
from rest_framework.serializers import ModelSerializer
from .models import Cita_Medica

from rest_framework import serializers
class CitaSerializer(ModelSerializer[Cita_Medica]):
    attendee = ListField(child=CharField(required=False), required=False)

    class Meta:
        model = Cita_Medica
        fields = ('id', 'title', 'description', 'start_at', 'end_at', 'location', 'attendee',)
        extra_kwargs = {'attendee': {'required': False, "allow_null": True}}

class CitasListSerializer(ModelSerializer[Cita_Medica]):
    
    nombre = serializers.SerializerMethodField()
    especialidad = serializers.SerializerMethodField()

    def get_nombre(self, obj):
        # Verificar el tipo de usuario que está realizando la consulta
        type_user = self.context['request'].user.user_type
        
        if type_user == "PACIENTE":
            # Si el usuario es un paciente, devolver el nombre del doctor
            return f"{obj.doctor.first_name} {obj.doctor.last_name} {obj.doctor.second_last_name}"
        else:
            # Si el usuario es un doctor, devolver el nombre del paciente
            return f"{obj.created_by.first_name} {obj.created_by.last_name} {obj.created_by.second_last_name}"

    def get_especialidad(self, obj):
        # Verificar el tipo de usuario que está realizando la consulta
        type_user = self.context['request'].user.user_type
        
        if type_user == "PACIENTE":
            # Si el usuario es un paciente, devolver la especialidad del doctor
            return obj.doctor.medico.id_especialidad.name
        else:
            # Si el usuario es un doctor, devolver None para ocultar la especialidad
            return None


    class Meta:
        model = Cita_Medica
        fields = ('nombre', 'especialidad','start_at', 'end_at', 'attendee',)
        extra_kwargs = {'attendee': {'required': False, "allow_null": True}}