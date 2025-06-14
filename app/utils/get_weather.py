from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Weather, Celestial_Events, SessionLocal
import pandas as pd

def read_weather_csv(file_path):
    df = pd.read_csv(file_path)

    df = df[[
        'country',
        'wind_degree',
        'wind_kph',
        'wind_direction',
        'last_updated',
        'sunrise',
        'sunset',
        'moonrise',
        'moonset'
    ]]

    return df

def get_weather(country: str, date: str) -> str:
    session: Session = SessionLocal()
    try:
        try:
            weather = session.query(Weather).filter_by(country=country).one()
        except NoResultFound:
            return f"Помилка: Не знайдено інформації за країною: '{country}'."

        celestial_events = session.query(Celestial_Events).filter_by(weather_id=weather.id, last_updated=date).all()
        if not celestial_events:
            return f"Помилка: Не знайдено інформації за країною: '{country}' за датою: '{date}'."

        formatted_measurements = []
        for measurement in celestial_events:
            formatted_measurements.append(
                f"Ступінь вітру: {measurement.wind_degree}, "
                f"Швидкість вітру (км/год): {measurement.wind_kph}, "
                f"Напрямок вітру: {measurement.wind_direction}, "
                f"Схід сонця: {measurement.sunrise}, "
                f"Захід сонця: {measurement.sunset}, "
                f"Схід місяця: {measurement.moonrise}, "
                f"Захід місяця: {measurement.moonset}, "
                f"Чи слід виходити на вулицю: {'Так' if measurement.go_outside else 'Ні'}"
            )
        return "\n".join(formatted_measurements)
    except Exception as e:
        return f"Виникла помилка: {e}"
    finally:
        session.close()