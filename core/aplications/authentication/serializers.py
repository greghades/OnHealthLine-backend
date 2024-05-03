from rest_framework import serializers
from .models import CustomUser,CodesVerification
from aplications.paciente.models import Paciente


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = fields = ('id', 'email', 'password', 'first_name', 'last_name','second_last_name','sex','phone', 'user_type')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','password')
    

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name','second_last_name','sex','phone', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True}, 
        }
    def create(self, validated_data):

        # Crear un nuevo usuario
        user = CustomUser.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['name'],
            last_name=validated_data['last_name'],
            second_last_name=validated_data['name'],
            sex=validated_data['last_name'],
            phone=validated_data['name'],
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
