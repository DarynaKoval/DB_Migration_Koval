"""Domain/ORM-шар: описана лише частина колонок CSV."""
import enum
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): pass

class WindDirection(enum.Enum):
    N="N"; NNE="NNE"; NE="NE"; ENE="ENE"; E="E"; ESE="ESE"; SE="SE"; SSE="SSE"
    S="S"; SSW="SSW"; SW="SW"; WSW="WSW"; W="W"; WNW="WNW"; NW="NW"; NNW="NNW"

class Weather(Base):
    __tablename__ = "weather"
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    location_name: Mapped[str] = mapped_column(String(150))
    last_updated = mapped_column(DateTime)
    sunrise = mapped_column(Time, nullable=True)
    wind: Mapped["Wind"] = relationship(back_populates="weather", uselist=False)

class Wind(Base):
    __tablename__ = "wind"
    id: Mapped[int] = mapped_column(primary_key=True)
    weather_id: Mapped[int] = mapped_column(ForeignKey("weather.id"), unique=True)
    wind_mph = mapped_column(Float, nullable=True)
    wind_kph = mapped_column(Float, nullable=True)
    wind_degree = mapped_column(Integer, nullable=True)
    wind_direction = mapped_column(Enum(WindDirection, name="wind_direction", values_callable=lambda e: [x.value for x in e]), nullable=True)
    gust_mph = mapped_column(Float, nullable=True)
    gust_kph = mapped_column(Float, nullable=True)
    go_outside: Mapped[bool] = mapped_column(Boolean)
    weather: Mapped[Weather] = relationship(back_populates="wind")
