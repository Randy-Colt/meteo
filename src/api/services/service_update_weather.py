import asyncio

from api.crud import (
    get_all_cities,
    update_all_cities_weathers
)
from core.constants import FIFTEEN_MINUTES
from core.db_settings import db_helper
from .service_weather_api import get_weather_from_api


async def update_weathers():
    '''Обновляет все записи о погоде каждые 15 минут.'''
    async_session = db_helper.session_factory
    while True:
        async with async_session() as session:
            cities = await get_all_cities(session)
            if cities:
                results = []
                for city in cities:
                    latitude = city.latitude
                    longitude = city.longitude
                    result_weather = await get_weather_from_api(
                        latitude,
                        longitude,
                        'hourly'
                    )
                    result_weather['id'] = city.weather_id
                    results.append(result_weather)
                await update_all_cities_weathers(session, results)
        await asyncio.sleep(FIFTEEN_MINUTES)
