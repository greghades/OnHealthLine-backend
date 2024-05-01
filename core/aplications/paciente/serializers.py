from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = "__all__"

    def create(self, validated_data):
        # Crear un nuevo usuario
        user = Paciente.objects.create(
            user=validated_data['user'],
            birthdate = validated_data['birthdate'],
            address= validated_data['address']
        
        )
        
        user.save()

        return user