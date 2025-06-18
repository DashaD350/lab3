import pandas as pd
from contextlib import contextmanager
from app.models import Weather, SessionLocal, WindDirection, Celestial_Events


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Помилка при записі до бази: {e}")
    finally:
        session.close()

def read_weather_csv(file_path):
    return pd.read_csv(file_path)[[
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


def parse_enum(value, enum_class):
    return enum_class.__members__.get(value, None)


def parse_datetime(value, mode='date'):
    if pd.isna(value):
        return None
    dt = pd.to_datetime(value)
    return dt.date() if mode == 'date' else dt.time()


def safe_float(value):
    return float(value) if not pd.isna(value) else None


def write_weather(df: pd.DataFrame):
    with get_session() as session:
        for _, row in df.iterrows():
            weather = session.query(Weather).filter_by(country=row['country']).one_or_none()
            if not weather:
                weather = Weather(country=row['country'])
                session.add(weather)
                session.commit()

            event = Celestial_Events(
                weather_id=weather.id,
                wind_degree=int(row['wind_degree']) if not pd.isna(row['wind_degree']) else None,
                wind_kph=safe_float(row['wind_kph']),
                wind_direction=parse_enum(row['wind_direction'], WindDirection),
                last_updated=parse_datetime(row['last_updated'], 'date'),
                sunrise=parse_datetime(row['sunrise'], 'time'),
                sunset=parse_datetime(row['sunset'], 'time'),
                moonrise=parse_datetime(row['moonrise'], 'time'),
                moonset=parse_datetime(row['moonset'], 'time'),
                go_outside=safe_float(row['wind_kph']) < 24 if not pd.isna(row['wind_kph']) else None
            )

            session.add(event)
