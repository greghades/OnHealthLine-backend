from rest_framework import serializers
from .models import Medico,Especialidad,Horario
from aplications.authentication.models import CustomUser
class MedicoSerializer(serializers.ModelSerializer):

    # especialidad = serializers.CharField(source='id_especialidad.name')
    # nombre = serializers.SerializerMethodField()

    class Meta:
        
        model = Medico
        fields = ['user', 'id_especialidad', 'descripcion']
   
    def create(self, validated_data):
        # Crear un nuevo usuario
        user = Medico.objects.create(
            user=validated_data['user'],
            id_especialidad = validated_data['id_especialidad'],
            descripcion = validated_data['descripcion'],
        
        )
        
        user.save()

        return user
    def get_nombre(self, obj):
        return f'Dr. {obj.user.get_full_name()}' if obj.user.sex == 'M' else f'Dra. {obj.user.get_full_name()}'


class MedicoListSerializer(serializers.ModelSerializer):
   
    especialidad = serializers.CharField(source='id_especialidad.name')
    cedula = serializers.CharField(source='user.id')
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = Medico
        fields = ['cedula', 'nombre', 'especialidad', 'descripcion']

    def get_nombre(self, obj):
        # Aquí puedes proporcionar la lógica para obtener el nombre del médico
        return f'Dr. {obj.user.get_full_name()}'  # Suponiendo que el nombre del médico está en el campo user

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = "__all__"

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = "__all__"
