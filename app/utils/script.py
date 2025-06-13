import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Weather, SessionLocal, WindDirection

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

def should_go_outside(wind_kph: float) -> bool:
    return wind_kph < 24

def fill_weather(df: pd.DataFrame):
    session: Session = SessionLocal()

    try:
        for _, row in df.iterrows():
            try:
                weather = session.query(Weather).filter_by(country=row['country']).one()
            except NoResultFound:
                weather = Weather(country=row['country'])
                session.add(weather)
                session.commit()

            weather_measurement = Weather(
                weather_id=weather.id,
                wind_degree=int(row['wind_degree']) if not pd.isna(row['wind_degree']) else None,
                wind_kph=float(row['wind_kph']) if not pd.isna(row['wind_kph']) else None,
                wind_direction=WindDirection[row['wind_direction']] if row['wind_direction'] in WindDirection.__members__ else None,
                last_updated=pd.to_datetime(row['last_updated']).date() if not pd.isna(row['last_updated']) else None,
                sunrise=pd.to_datetime(row['sunrise']).time() if not pd.isna(row['sunrise']) else None,
                sunset=pd.to_datetime(row['sunset']).time() if not pd.isna(row['sunset']) else None,
                moonrise=pd.to_datetime(row['moonrise']).time() if not pd.isna(row['moonrise']) else None,
                moonset=pd.to_datetime(row['moonset']).time() if not pd.isna(row['moonset']) else None,
                go_outside=should_go_outside(float(row['wind_kph'])) if not pd.isna(row['wind_kph']) else None
            )
            session.add(weather_measurement)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Помилка при записі до бази: {e}")
    finally:
        session.close()
