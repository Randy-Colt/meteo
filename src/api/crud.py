from typing import Any, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.schema import CitySchema, UserRegistrationSchema
from core.models import City, CityWeather, User, UsersCities


async def get_cities_names(session: AsyncSession, user: User) -> Sequence[str]:
    '''Получить список имён городов, для которых отслеживается погода.'''
    result = await session.execute(
        select(City.name).filter(City.users.contains(user))
    )
    return result.scalars().all()


async def get_city_weather_by_name(
    session: AsyncSession,
    city_name: str,
    user: User
) -> City:
    '''Получить объект погоды в городе по его названию.'''
    result = await session.execute(
        select(City).where(City.name == city_name)
        .filter(City.users.contains(user))
        .options(joinedload(City.weather))
    )
    city = result.scalar_one_or_none()
    return getattr(city, 'weather', None)


async def get_city_by_name(
    session: AsyncSession,
    city_name: str,
    user: User
) -> City:
    '''Получить объект города по его названию.'''
    return await session.scalar(
        select(City).where(City.name == city_name)
        .filter(City.users.contains(user))
    )


async def create_city_and_weather(
        session: AsyncSession,
        city_data: CitySchema,
        weather_data: dict[str, Any],
        user: User
) -> None:
    '''Добавить город в список отслеживаемых и добавить данные о погоде в этом городе.'''
    checked_city = await session.scalar(
        select(City).where(City.name == city_data.name)
        .where(City.latitude == city_data.latitude)
        .where(City.longitude == city_data.longitude)
    )
    if checked_city is not None:
        session.add(UsersCities(city_id=checked_city.id, user_id=user.id))
        await session.commit()
        return None
    weather = CityWeather(**weather_data)
    session.add(weather)
    await session.flush()
    city = City(weather_id=weather.id, **city_data.model_dump())
    session.add(city)
    city.users.append(user)
    await session.commit()


async def create_user(
    session: AsyncSession,
    user: UserRegistrationSchema
) -> User:
    '''Создать юзера.'''
    created_user = User(**user.model_dump())
    session.add(created_user)
    await session.commit()
    return created_user


async def get_or_create_user_id(
    session: AsyncSession,
    user: UserRegistrationSchema
) -> str:
    '''Получить или создать id юзера по юзернейму.'''
    user_id = await session.scalar(
        select(User.id).where(User.username == user.username)
    )
    if user_id is None:
        created_user = await create_user(session, user)
        return created_user.id
    return user_id


async def get_user(session: AsyncSession, user_id: str) -> User:
    '''Получить объект юзера по id.'''
    return await session.get(User, user_id)


async def update_all_cities_weathers(
    session: AsyncSession,
    params: Sequence[dict[str, str]]
) -> None:
    '''Обновить данные о погоде для всех записей о погоде в городах.'''
    await session.execute(update(CityWeather), params)
    await session.commit()


async def get_all_cities(session: AsyncSession) -> Sequence[City]:
    '''Получить список объектов всех городов.'''
    result = await session.execute(select(City))
    return result.scalars().all()
