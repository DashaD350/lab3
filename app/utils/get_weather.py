from sqlalchemy.orm import Session
from app.models import Weather, SessionLocal

def get_weather(country: str, date: str) -> str:
    session: Session = SessionLocal()
    try:
        weather_measurements = session.query(Weather).filter_by(weather_id=Weather.id, last_updated=date).all()
        if not weather_measurements:
            return f"Error: No weather measurements found for the country '{country}' on the date '{date}'."

        formatted_measurements = []
        for measurement in weather_measurements:
            formatted_measurements.append(
                f"Wind Degree: {measurement.wind_degree}, "
                f"Wind Speed (kph): {measurement.wind_kph}, "
                f"Wind Direction: {measurement.wind_direction}, "
                f"Sunrise: {measurement.sunrise}, "
                f"Go Outside: {'Yes' if measurement.go_outside else 'No'}"
            )
        return "\n".join(formatted_measurements)
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    finally:
        session.close()