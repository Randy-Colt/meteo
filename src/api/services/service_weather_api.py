from typing import Any

from fastapi import HTTPException
from httpx import AsyncClient, AsyncHTTPTransport

from core.constants import WEATHER_API_URL
from .service_process_json import clean_json_from_api

TRANSPORT = AsyncHTTPTransport(retries=3)


async def get_weather_from_api(
    latitude: float,
    longitude: float,
    mode: str
) -> dict[str, Any]:
    '''
    Обратиться к внешнему API за данными о погоде.

    :param laitude, longitude: координаты
    :param mode: режим, в котором нужно получить данные; <hourly> - почасовой
    прогноз на текущий день; <current> - получить прогноз на текущий момент.
    '''
    if mode == 'hourly':
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'timezone': 'Europe/Moscow',
            'forecast_days': 1,
            'wind_speed_unit': 'ms',
            'hourly': [
                'temperature_2m',
                'relative_humidity_2m',
                'wind_speed_10m',
                'precipitation'
            ]
        }
    elif mode == 'current':
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'timezone': 'Europe/Moscow',
            'wind_speed_unit': 'ms',
            'current': [
                'temperature_2m',
                'surface_pressure',
                'wind_speed_10m'
            ]
        }
    else:
        raise ValueError(f'Невалидный режим: {mode}')
    async with AsyncClient(transport=TRANSPORT) as client:
        response = await client.get(WEATHER_API_URL, params=params)
        response_json = response.json()
        if response_json.get('error', False):
            raise HTTPException(response.status_code, response_json)
        return clean_json_from_api(response_json, mode)
