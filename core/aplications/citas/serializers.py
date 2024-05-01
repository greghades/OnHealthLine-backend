from rest_framework.fields import CharField,ListField
from rest_framework.serializers import ModelSerializer
from .models import Cita_Medica

class CitaSerializer(ModelSerializer[Cita_Medica]):
    attendee = ListField(child=CharField(required=False), required=False)

    class Meta:
        model = Cita_Medica
        fields = ('id', 'title', 'description', 'start_at', 'end_at', 'location', 'attendee',)
        extra_kwargs = {'attendee': {'required': False, "allow_null": True}}