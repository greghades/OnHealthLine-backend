from aplications.citas.models import Cita_Medica
from aplications.citas.utils import request_wrapper, ThirdPartyAPIConnectionError


NOCODEAPI_GOOGLE_CALENDAR_BASE_URL = "https://v1.nocodeapi.com/greg251325/calendar/SvOedyqlpEwxfWMh"


def nocodeapi_google_calendar_create_event(cita: Cita_Medica, user_email: str,doctor_email: str):
    """Create an event on google calendar using nocodeapi."""
    response_data = None
    # payload to be sent to nocodeapi to create an event
    request_data = {
        "summary": cita['title'],
        "location": cita['location'],
        "description": cita['description'],
        "start": {"dateTime": cita['start_at']},
        "end": {"dateTime": cita['end_at']},
        "locked": True,
        "sendNotifications": True,
        "attendees": [{"email": user_email},{"email": doctor_email}],
        "guestsCanInviteOthers": False,
        "guestsCanModify": False,
        "guestsCanSeeOtherGuests": False,
    }

    try:
        response = request_wrapper(
            method='post',
            params={'sendUpdates': 'all'},
            post_data=request_data,
            url=f'{NOCODEAPI_GOOGLE_CALENDAR_BASE_URL}/event',
            headers={'Content-Type': 'application/json'},
        )
        # check if the response is not None, and the status_code is 200'
        if response is not None and response.status_code == 200:
            return response.response_data['id']

    except ThirdPartyAPIConnectionError as error:
        pass
        # you can log to an error handler like sentry
    return response_data


def nocodeapi_google_calendar_edit_event(cita: Cita_Medica, user_email: str):
    """Edit an event."""
    response_data = None
    # payload to be sent to nocodeapi google_calendar to edit an event.
    request_data = {
        "summary": cita['title'],
        "location": cita['location'],
        "description": cita['description'],
        "start": {"dateTime": str(cita['start_at'].isoformat())},
        "end": {
            "dateTime": str(cita['end_at'].isoformat()),
        },
        "sendNotifications": True,
        "guestsCanInviteOthers": False,
        "guestsCanModify": False,
        "guestsCanSeeOtherGuests": False,
        "locked": True,
        "attendees": [{"email": user_email}],

    }
    try:
        response = request_wrapper(
            method='put',
            params={"eventId": cita['google_calendar_event_id'], "sendUpdates": "all"},
            post_data=request_data,
            url=f'{NOCODEAPI_GOOGLE_CALENDAR_BASE_URL}/event',
            headers={'Content-Type': 'application/json'},
        )
        # check if the response is not None, and the status_code is 200
        if response is not None and response.status_code == 200:
            response_data = {'nocodeapi_google_calendar_api': response.response_data}
            return response.response_data['id']
    except ThirdPartyAPIConnectionError as error:
        pass
        # you can log to an error handler like sentry
    return response_data


def nocodeapi_google_calendar_delete_event(cita: str):
    """Delete an event on nocodeapi google calendar."""
    try:
        request_wrapper(
            method='delete',
            params={"eventId": cita['google_calendar_event_id'], "sendUpdates": "all"},
            url=f'{NOCODEAPI_GOOGLE_CALENDAR_BASE_URL}/event',
            headers={'Content-Type': 'application/json'},
        )
    except ThirdPartyAPIConnectionError as error:
        pass
        # you can log to an error handler like sentry
    return True
