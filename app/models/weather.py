from sqlalchemy import Column, Integer, String, Float, Enum
import enum
from sqlalchemy.orm import relationship
from app.models import Base

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

    celestial_changes = relationship("Celestial_Changes", back_populates="weather", cascade="all, delete")