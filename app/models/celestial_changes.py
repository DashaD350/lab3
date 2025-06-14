from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app.models import Base, WindDirection

class Celestial_Events(Base):
    __tablename__ = "celestial_changes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey("weather.id", ondelete="CASCADE"))
    last_updated = Column(Date)
    sunrise = Column(Time)
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)

    weather = relationship("Weather", back_populates="celestial_changes")