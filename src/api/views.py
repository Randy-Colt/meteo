from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import (
    create_city_and_weather,
    get_cities_names,
    get_city_weather_by_name,
    get_or_create_user_id
)
from api.depends import check_city, get_user_by_id
from api.schema import (
    CitySchema,
    LatitudeConstrainted,
    LongitudeConstrainted,
    UserRegistrationSchema
)
from api.services import create_json_weather, get_weather_from_api
from api.utils import split_and_check_params
from core.constants import DEFAULT_WEATHER_PARAMS, MAX_HOUR, MIN_HOUR
from core.db_settings import db_helper
from core.models import User

router = APIRouter()


@router.get(
    '/weather',
    summary='Получить прогноз погоды на текущий час для выбранной локации.'
)
async def get_current_weather(
    latitude: LatitudeConstrainted,
    longitude: LongitudeConstrainted
):
    return await get_weather_from_api(latitude, longitude, 'current')


@router.post(
    '/{user_id}/add-city',
    status_code=status.HTTP_201_CREATED,
    summary=(
        'Добавить город в базу данных для отслеживания прогноза погоды'
        'на текущий день.'
    )
)
async def add_city(
    user_id: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(get_user_by_id),
    city_data: CitySchema = Depends(check_city)
):
    weather_json = await get_weather_from_api(
        city_data.latitude,
        city_data.longitude,
        'hourly'
    )
    await create_city_and_weather(
        session,
        city_data,
        weather_json,
        user
    )
    return {'message': f'Город {city_data.name} успешно добавлен!'}


@router.get(
    '/{user_id}/cities',
    summary=(
        'Получить список городов, для которых отслеживается прогноз погоды.'
    )
)
async def get_cities_list(
    user_id: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(get_user_by_id)
):
    return await get_cities_names(session, user)


@router.get(
    '/{user_id}/city-weather',
    summary='Получить прогноз погоды для города на выбранный час.'
)
async def get_weather_in_city(
    user_id: str,
    city_name: str,
    hour: Annotated[int, Query(ge=MIN_HOUR, le=MAX_HOUR)],
    params: str = DEFAULT_WEATHER_PARAMS,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(get_user_by_id)
):
    splitted_params = split_and_check_params(params)
    if splitted_params is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Переданы невалидные параметры в params.'
        )
    city_weather = await get_city_weather_by_name(session, city_name, user)
    if city_weather is None:
        raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'Город {city_name} не найден.'
            )
    weather_json = create_json_weather(
        city_weather.__dict__,
        hour,
        splitted_params
    )
    return {
        'city_name': city_name,
        'timezone': 'Europe/Moscow',
        'time': f'{hour:02}:00',
        'weather': weather_json,
        'measurement_units': {
            'temperature': '°C',
            'relative_humidity': '%',
            'precipitation': 'mm',
            'wind_speed': 'm/s'
        }
    }


@router.post(
    '/registration',
    summary='Получить id по юзернейму.'
)
async def get_user_id(
    user: UserRegistrationSchema,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await get_or_create_user_id(session, user)
