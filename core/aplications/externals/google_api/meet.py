import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
from datetime import datetime, timedelta

CLIENT_SECRET = 'C:/Users/58412/Downloads/token.json'
SCOPE = 'https://www.googleapis.com/auth/calendar'
STORAGE = Storage('credentials.storage')

def authorize_credentials():
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials don't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

def crear_enlace_google_meet(titulo, descripcion, invitados,start_at,end_at):
    # Autorizar credenciales
    credentials = authorize_credentials()

    # Crear cliente de API de Google Calendar
    service = discovery.build('calendar', 'v3', credentials=credentials)

    # Definir parámetros del evento (reunión)
    fecha_inicio = datetime.now() + timedelta(hours=1)
    fecha_fin = fecha_inicio + timedelta(hours=2)

    # Crear el evento en Google Calendar
    evento = {
            'summary': titulo,
            'description': descripcion,
            'start': {
                'dateTime': start_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [{'email': correo} for correo in invitados],
            'conferenceData': {
                'createRequest': {
                    'requestId': 'randomstring',  # Debe ser una cadena aleatoria
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                    'conferenceSolution': {
                        'type': 'hangoutsMeet'
                    },
                    'entryPoints': [
                        {
                            'entryPointType': 'video',
                            'uri': 'https://meet.google.com/link',
                            'label': 'Enlace de Google Meet'
                        }
                    ]
                }
            },
            "sendNotifications": True
        }
        
    evento_creado = service.events().insert(calendarId='primary', body=evento, conferenceDataVersion=1).execute()
    
    return evento_creado

# # Ejemplo de uso
# titulo_evento = 'Reunión de equipo'
# descripcion_evento = 'Reunión semanal para discutir el progreso del proyecto.'
# fecha_inicio_evento = datetime(2024, 5, 5, 10, 0)  # 5 de mayo de 2024 a las 10:00 AM
# fecha_fin_evento = fecha_inicio_evento + timedelta(hours=1)  # Duración de una hora
# invitados_evento = ['correo1@example.com', 'correo2@example.com', 'correo3@example.com']

# # Llama a la función para crear el evento en Google Calendar
# enlace_reunion = crear_enlace_google_meet(titulo_evento, descripcion_evento, fecha_inicio_evento, fecha_fin_evento, invitados_evento)

# print("Enlace de la reunión de Google Meet:", enlace_reunion)
