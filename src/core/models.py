from uuid import uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import MAX_CITY_NAME, MAX_USERNAME
from core.db_settings import Base, BaseID


class City(BaseID):
    '''
    Модель города.

    :param name: название города
    :params latitude, longitude: координаты
    :param weather: погода в городе
    :param users: пользователи, в чьих списках есть этот город
    '''
    __tablename__ = 'cities'

    name: Mapped[str] = mapped_column(String(MAX_CITY_NAME), unique=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    weather: Mapped['CityWeather'] = relationship(
        'CityWeather',
        back_populates='city',
        uselist=False
    )
    weather_id: Mapped[int] = mapped_column(ForeignKey('cityweathers.id'))
    users: Mapped[list['User']] = relationship(
        back_populates='cities',
        secondary='userscities'
    )


class CityWeather(BaseID):
    '''
    Модель погоды в городе.

    :param city: город, к которому относится запись о погоде
    :param temperature: температура, °C
    :param relative_humidity: относительная влажность, %
    :param wind_speed: скорость ветра, m/s
    :param precipitation: осадки, mm
    '''

    city: Mapped['City'] = relationship(
        'City',
        back_populates='weather',
        uselist=False
    )
    temperature: Mapped[str]
    relative_humidity: Mapped[str]
    wind_speed: Mapped[str]
    precipitation: Mapped[str]


def _get_uuid():
    return str(uuid4())


class User(Base):
    '''
    Модель пользователя.

    :param username: уникальный юзернейм
    :param cities: список городов, для которых отслеживается прогноз погоды
    '''

    id: Mapped[str] = mapped_column(
        default=_get_uuid,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(String(MAX_USERNAME), unique=True)
    cities: Mapped[list[City]] = relationship(
        back_populates='users',
        secondary='userscities'
    )


class UsersCities(Base):
    __tablename__ = 'userscities'

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'),
        primary_key=True
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey('cities.id'),
        primary_key=True
    )
