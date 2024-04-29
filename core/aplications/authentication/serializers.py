from rest_framework import serializers
from .models import CustomUser,CodesVerification



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username', 'email','first_name', 'last_name')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','password')
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'name', 'last_name', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True},  # La contraseña solo se debe escribir, no se muestra en las respuestas
        }

    def create(self, validated_data):
        # Crear un nuevo usuario
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type']
        )

        # Establecer la contraseña y realizar el hash
        user.set_password(validated_data['password'])
        user.save()

        return user

class ValidateCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodesVerification
        exclude = ('id',)
