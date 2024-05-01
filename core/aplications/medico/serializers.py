from rest_framework import serializers
from .models import Medico
class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = "__all__"
   
    def create(self, validated_data):
        # Crear un nuevo usuario
        user = Medico.objects.create(
            user=validated_data['user'],
            id_especialidad = validated_data['id_especialidad'],
            descripcion = validated_data['descripcion'],
        
        )
        
        user.save()

        return user