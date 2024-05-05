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

def crear_enlace_google_meet():
    # Autorizar credenciales
    credentials = authorize_credentials()

    # Crear cliente de API de Google Calendar
    service = discovery.build('calendar', 'v3', credentials=credentials)

    # Definir parámetros del evento (reunión)
    fecha_inicio = datetime.now() + timedelta(hours=1)
    fecha_fin = fecha_inicio + timedelta(hours=2)

    evento = {
        'summary': 'Reunión de Google Meet',
        'start': {
            'dateTime': fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Los_Angeles',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'randomstring',  # Debe ser una cadena aleatoria
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }
    }

    # Crea el evento (reunión) en Google Calendar
    evento_creado = service.events().insert(calendarId='primary', body=evento, conferenceDataVersion=1).execute()

    # Obtener enlace de la reunión de Google Meet
    enlace_reunion = evento_creado.get('hangoutLink')

    return enlace_reunion

# # Ejemplo de uso
# enlace_reunion = crear_enlace_google_meet()
# print("Enlace de la reunión de Google Meet:", enlace_reunion)
