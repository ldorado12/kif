import subprocess
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import datetime


SERVICE_ACCOUNT_FILE = 'C:/Users/Santi/OneDrive/Escritorio/TPSanti/credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send'
]


try:
    response = subprocess.run(['ping', 'oauth2.googleapis.com'], capture_output=True, text=True, check=True)
    print(response.stdout)
except subprocess.CalledProcessError as e:
    print(f'Error al hacer ping: {e}')
    exit(1)


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


calendar_service = build('calendar', 'v3', credentials=credentials)
gmail_service = build('gmail', 'v1', credentials=credentials)


calendar_id = 'santi.1234.azcurra@gmail.com'


def agendar_evento():
    """Función para agendar un evento en el calendario."""
    try:
        summary = input("Introduce el resumen del evento: ")
        location = input("Introduce la ubicación del evento: ")
        description = input("Introduce la descripción del evento: ")
        start_time = input("Introduce la fecha y hora de inicio (formato: YYYY-MM-DDTHH:MM:SS-03:00): ")
        end_time = input("Introduce la fecha y hora de fin (formato: YYYY-MM-DDTHH:MM:SS-03:00): ")

      
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
        }
       
        event = calendar_service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f'Evento creado: {event.get("htmlLink")}')
    except HttpError as error:
        print(f'Error al crear el evento: {error}')


def leer_eventos():
    """Función para leer eventos del calendario."""
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        future = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

        print(f"Leyendo eventos desde {now} hasta {future}...")

        events_result = calendar_service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=future,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            print('No hay eventos próximos.')
        else:
            print("Eventos encontrados:")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"- {event['summary']} (Inicio: {start})")
    except HttpError as error:
        print(f'Error al leer los eventos: {error}')




def main():
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Agendar un evento")
        print("2. Leer eventos")
        print("3. Salir")
        choice = input("Introduce el número de tu elección: ").strip()

        if choice == '1':
            agendar_evento()
        elif choice == '2':
            leer_eventos()
        elif choice == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige nuevamente.")



if __name__ == "__main__":
    main()
