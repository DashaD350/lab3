from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Weather, Celestial_Events, SessionLocal
import pandas as pd

COLUMNS = [
    'country',
    'wind_degree',
    'wind_kph',
    'wind_direction',
    'last_updated',
    'sunrise',
    'sunset',
    'moonrise',
    'moonset'
]

def read_weather_csv(file_path: str) -> pd.DataFrame:
    """Зчитування CSV з вибраними колонками."""
    return pd.read_csv(file_path)[COLUMNS]

def fetch_weather_by_country(session: Session, country: str) -> Weather | None:
    """Отримати Weather за країною або None."""
    try:
        return session.query(Weather).filter_by(country=country).one()
    except NoResultFound:
        return None

def fetch_celestial_events(session: Session, weather_id: int, date: str) -> list[Celestial_Events]:
    """Отримати події за датою."""
    return session.query(Celestial_Events).filter_by(weather_id=weather_id, last_updated=date).all()

def format_event(event: Celestial_Events) -> str:
    return (
        f"Ступінь вітру: {event.wind_degree}, "
        f"Швидкість вітру (км/год): {event.wind_kph}, "
        f"Напрямок вітру: {event.wind_direction}, "
        f"Схід сонця: {event.sunrise}, "
        f"Захід сонця: {event.sunset}, "
        f"Схід місяця: {event.moonrise}, "
        f"Захід місяця: {event.moonset}, "
        f"Чи слід виходити на вулицю: {'Так' if event.go_outside else 'Ні'}"
    )

def get_weather(country: str, date: str) -> str:
    session: Session = SessionLocal()
    try:
        weather = fetch_weather_by_country(session, country)
        if not weather:
            return f"Не знайдено інформації про країну: '{country}'."

        events = fetch_celestial_events(session, weather.id, date)
        if not events:
            return f"Дані для країни '{country}' на дату '{date}' відсутні."

        return "\n".join(format_event(e) for e in events)

    except Exception as e:
        return f"Виникла помилка: {e}"
    finally:
        session.close()