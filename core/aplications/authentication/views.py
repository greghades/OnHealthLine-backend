from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from core.settings.base import EMAIL_HOST_USER
from aplications.paciente.serializers import PacienteSerializer
from aplications.medico.serializers import MedicoSerializer
from rest_framework.views import APIView

from .models import CustomUser,CodesVerification
from .serializers import UserSerializer, RegisterSerializer,UserTokenSerializer,LoginSerializer, ValidateCodeSerializer
from .messages.responses_ok import CODE_VALIDATED, DELETED_USER, EMAIL_SEND, LOGIN_OK, PASSWORD_CHANGED, SIGNUP_OK,LOGOUT_OK, UPDATE_OK
from .messages.responses_error import USER_ALREADY_EXISTS_ERROR,INACTIVE_USER_ERROR,CHANGED_PASSWORD_ERROR, CODER_VERIFICATION_ERROR, LOGIN_CREDENTIALS_REQUIRED_ERROR, LOGIN_CREDENTIALS_ERROR,LOGOUT_ERROR, NOT_FOUND_USER
from .helpers.content_emails import PASSWORD_RESET
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .helpers.randCodes import generatedCode

# Create your views here.


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        # Verificar si email o password son None
        if email is None or password is None:
            return Response(LOGIN_CREDENTIALS_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            
            # Verificar si el usuario es None o si la contraseña no coincide
            if user is None or user.password != password:
                return Response(LOGIN_CREDENTIALS_ERROR, status=status.HTTP_401_UNAUTHORIZED)
            
            # Verificar si el usuario está activo
            if not user.is_active:
                return Response(INACTIVE_USER_ERROR, status=status.HTTP_401_UNAUTHORIZED)
            
            # Obtener o crear el token
            token, created = Token.objects.get_or_create(user=user)
            
            # Si el token ya existe, eliminarlo y crear uno nuevo
            if not created:
                token.delete()
                token = Token.objects.create(user=user)

            # Devolver la respuesta con el token actualizado
            rspn = {
                "Token": token.key,
                "user": UserTokenSerializer(user, context=self.get_serializer_context()).data,
            }
            return Response(rspn, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response(LOGIN_CREDENTIALS_ERROR, status=status.HTTP_401_UNAUTHORIZED)

            


class RegistroView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        # Serializar los datos del usuario
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            # Crear el usuario
            user = user_serializer.save()

            # Obtener el tipo de usuario
            user_type = request.data.get('user_type')
            
            # Verificar el tipo de usuario y guardar los detalles adicionales si es necesario
            if user_type == 'PACIENTE':
                paciente_data = {
                    'user': user.id,
                    'birthdate': request.data.get('birthdate'),
                    'address': request.data.get('address')
                }
                paciente_serializer = PacienteSerializer(data=paciente_data)
                
                if paciente_serializer.is_valid():
                    paciente_serializer.save()
                    return Response({'message': 'Paciente registrado exitosamente'}, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    return Response(paciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            elif user_type == 'MEDICO':
                medico_data = {
                    'user': user.id,
                    'id_especialidad': request.data.get('id_especialidad'),
                    'descripcion': request.data.get('descripcion')
                }
                medico_serializer = MedicoSerializer(data=medico_data)
                
                if medico_serializer.is_valid():
                    medico_serializer.save()
                    return Response({'message': 'Médico registrado exitosamente'}, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    return Response(medico_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.delete()
                return Response({'message': 'Tipo de usuario no válido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(USER_ALREADY_EXISTS_ERROR, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    
    def post(self, request):
        token_request = request.data.get("Token", None)
        token = Token.objects.get(key=token_request)
        if token:
            user = CustomUser.objects.get(auth_token=token)
            user.auth_token.delete()
            logout(request)
            
            return Response(LOGOUT_OK,status=status.HTTP_200_OK)
        return Response(LOGOUT_ERROR, status=status.HTTP_400_BAD_REQUEST)      

class UpdateUser(generics.RetrieveUpdateAPIView):
    
    serializer_class = UserTokenSerializer
    queryset = CustomUser.objects.all()

    def put(self, request, *args, **kwargs):

        return Response({
            'data':request.data,
            'message':UPDATE_OK
        },status=status.HTTP_202_ACCEPTED)


class ListUsers(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.order_by('id')

class DeleteView(generics.GenericAPIView):
    
    def delete(self, request, pk):
        user= CustomUser.objects.get(id=pk)
        if user:
            user.delete()
            return Response(DELETED_USER, status=status.HTTP_200_OK)
        else:
            return Response(NOT_FOUND_USER, status=status.HTTP_404_NOT_FOUND)

class SendCodeResetPassword(generics.GenericAPIView):

    def post(self,request):
        email = request.data.get('email',None)
        try:
            user = CustomUser.objects.get(email=email)
            if user:
                mailReset = EmailMultiAlternatives(
                    'Reset password',
                    'Abroad',
                    EMAIL_HOST_USER,
                    [email]

                )
                
                code = CodesVerification(
                    changePasswordCode=generatedCode(),
                    user = user
                )
                code.save()

                mailReset.attach_alternative(f'<h1>Your verification Code: {code.changePasswordCode}</h1>','text/html')
                mailReset.send()

                return Response(EMAIL_SEND,status=status.HTTP_200_OK)
        except:
            return Response(LOGIN_CREDENTIALS_ERROR, status=status.HTTP_401_UNAUTHORIZED)

class ValidationCodeView(generics.GenericAPIView):
    def post(self,request):
        code_request = request.data.get('code',None)
        try:
            code_database = CodesVerification.objects.get(changePasswordCode=code_request)
            serializerValidate = ValidateCodeSerializer(code_database)
            if code_database is not None:
                return Response({
                    'Validated':CODE_VALIDATED,
                    'Entity':serializerValidate.data,
                    },status=status.HTTP_202_ACCEPTED)
        except:
            return Response(CODER_VERIFICATION_ERROR, status=status.HTTP_401_UNAUTHORIZED)

class ResetPasswordView(generics.GenericAPIView):
    def post(self,request):
        userId = request.data.get('user',None)
        new_password = request.data.get('password',None)
        if new_password is not None and userId is not None:
            user = CustomUser.objects.get(id=userId)
            user.set_password(new_password)
            user.save()
            return Response(PASSWORD_CHANGED,status=status.HTTP_200_OK)
        else:
            return Response(CHANGED_PASSWORD_ERROR,status=status.HTTP_400_BAD_REQUEST)