from sqlalchemy import Column, Integer, Float, String, Enum, Date, Time
import enum
from app.models.base import Base

class WindDirection(enum.Enum):
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    country = Column(String)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirection))
    last_updated = Column(Date)
    sunrise = Column(Time)
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)