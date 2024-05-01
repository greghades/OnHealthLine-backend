from django.db import models
from django.contrib.postgres.fields import ArrayField
from aplications.medico.models import Medico
import uuid
from aplications.paciente.models import Paciente
from aplications.authentication.models import CustomUser
# Create your models here.
class Cita_Medica(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    attendee = ArrayField(models.CharField(max_length=120, null=True, blank=True), null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='event_updated_by')
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=120, null=True, blank=True)
    invitation_sent = models.BooleanField(default=False)
    doctor = models.ForeignKey(Medico, on_delete=models.CASCADE)
    google_calendar_event_id = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.title