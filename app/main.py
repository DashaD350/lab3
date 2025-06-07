import csv
from datetime import datetime, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.weather import Weather, WindDirection

engine = create_engine("sqlite:///app.db")
SessionLocal = sessionmaker(bind=engine)

def parse_time(time_str: str) -> time:
    try:
        return datetime.strptime(time_str.strip(), "%I:%M %p").time()
    except ValueError:
        return None

def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None

def load_weather_from_csv(file_path: str):
    session = SessionLocal()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                weather = Weather(
                    country=row.get("country", ""),
                    wind_degree=int(row["wind_degree"]) if row["wind_degree"] else None,
                    wind_kph=float(row["wind_kph"]) if row["wind_kph"] else None,
                    wind_direction=WindDirection[row["wind_direction"]] if row["wind_direction"] in WindDirection.__members__ else None,
                    last_updated=parse_date(row.get("last_updated", "")),
                    sunrise=parse_time(row.get("sunrise", "")),
                    sunset=parse_time(row.get("sunset", "")),
                    moonrise=parse_time(row.get("moonrise", "")),
                    moonset=parse_time(row.get("moonset", ""))
                )
                session.add(weather)
            except Exception as e:
                print(f"Виникла помилка при обробці рядка: {e}\nРядок: {row}")
        session.commit()
    session.close()

if __name__ == "__main__":
    csv_path = "data/weather_data.csv"
    load_weather_from_csv(csv_path)