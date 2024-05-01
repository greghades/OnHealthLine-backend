from django.shortcuts import render

# Create your views here.
from uuid import UUID
#from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.exceptions import ValidationError
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from django.db import transaction
from .serializers import CitaSerializer
from .models import Cita_Medica
from aplications.medico.models import Medico,Horario
from aplications.externals.nocodeapi.google_calendar import (
    nocodeapi_google_calendar_create_event,
    nocodeapi_google_calendar_edit_event,
    nocodeapi_google_calendar_delete_event
)
from aplications.authentication.models import CustomUser
from .utils import get_event_info


class CreateEventView(CreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = CitaSerializer

    @transaction.atomic
    def post(self, request: Request) -> Response:
        """Create event view."""
        if not request.user.is_authenticated:
            return Response(
                {"message": "User not authenticated"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Need email confirmed
        if not request.user.email_confirmed:
            return Response(
                {"message": "email not confirmed, please check your mail for the confirmation mail"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)


        # Obtener el doctor y el usuario de la solicitud
        doctor_id = request.data.get('doctor_id')
        usuario_id = request.data.get('usuario_id')
        
        medico = CustomUser.objects.get(id=doctor_id,user_type='MEDICO')
        


        # Obtener la fecha y hora de inicio y fin de la cita
        start_at = serializer.validated_data['start_at']
        end_at = serializer.validated_data['end_at']
        
        # Validar si el doctor tiene disponible el horario
        if not self.doctor_tiene_horario_disponible(doctor_id, start_at, end_at):
            raise ValidationError("El doctor no tiene disponible este horario")
        

        response = serializer.save(doctor_id=doctor_id, usuario_id=usuario_id,attendee=[request.user.id], created_by=request.user)
        google_calendar_response = nocodeapi_google_calendar_create_event(serializer.data, request.user.email,medico.email)
        response.google_calendar_event_id = google_calendar_response
        response.invitation_sent = True
        response.save()
        return Response({"message": "Event successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def doctor_tiene_horario_disponible(self, doctor_id, start_at, end_at):
        # Buscar si hay algún horario para el doctor en el rango de fechas y horas especificado
        horarios = Horario.objects.filter(doctor_id=doctor_id, dia=start_at.date(), hora_inicio__lte=start_at.time(), hora_fin__gte=end_at.time())
        
        # Si encontramos al menos un horario, significa que el doctor tiene disponible ese horario
        return horarios.exists()

class EditEventView(UpdateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = CitaSerializer

    @transaction.atomic
    def patch(self, request: Request, cita_id: UUID) -> Response:
        """Edit an event."""
        if not request.user.is_authenticated:
            return Response({"message": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)
        try:
            cita = Cita_Medica.objects.get(id=cita_id)
        except Cita_Medica.DoesNotExist:
            return Response({"message": f"Event with id {cita_id} does not exist"},
                            status=status.HTTP_201_CREATED)

        if cita.created_by != request.user.id:
            return Response({"message": "You don't have permission to edit this event"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(instance=cita, data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save(updated_by=request.user)
        google_calendar_response = nocodeapi_google_calendar_edit_event(cita.__dict__, request.user.email)
        response.google_calendar_event_id = google_calendar_response
        response.save()
        return Response({"message": "Event successfully edited"}, status=status.HTTP_200_OK)


class RetrieveEventView(RetrieveAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs) -> Response:
        try:
            cita = Cita_Medica.objects.all()
        except Cita_Medica.DoesNotExist:
            return Response(
                {"message": f"Events does not exist"},
                status=status.HTTP_200_OK
            )
        data = get_event_info(cita)
        return Response(data, status=status.HTTP_200_OK)


class JoinEventView(UpdateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = CitaSerializer

    @transaction.atomic
    def patch(self, request: Request, cita_id: UUID, user_id: UUID) -> Response:
        """Edit an event."""
        if not request.user.is_authenticated:
            return Response({"message": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)
        try:
            cita = Cita_Medica.objects.get(id=cita_id)
        except Cita_Medica.DoesNotExist:
            return Response({"message": f"Event with id {cita_id} does not exist"},
                            status=status.HTTP_201_CREATED)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"message": f"User with id {user_id} does not exist"},
                            status=status.HTTP_201_CREATED)
        if str(user_id) not in cita.attendee:
            cita.attendee += [str(user_id)]
            cita.save()
            nocodeapi_google_calendar_edit_event(cita.__dict__, user.email)
            return Response({"message": "Successfully registered for this event"}, status=status.HTTP_200_OK)
        else:
            cita.attendee.remove(str(user_id))
            nocodeapi_google_calendar_delete_event(cita.__dict__)
            cita.save()
            return Response({"message": "You have successfully removed this event"}, status=status.HTTP_200_OK)
