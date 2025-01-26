from typing import Any
from re import sub


def clean_hourly_json(raw_json: dict[str, Any]) -> dict[str, str] | None:
    '''Преобразовать json, если он был получен в режиме <hourly>.'''
    weather_data = raw_json['hourly']
    if not weather_data or not isinstance(weather_data, dict):
        return None
    weather_data.pop('time')
    clean_json = {
        sub(r'_\d+\D', '', key): ','.join([str(item) for item in value])
        for key, value in weather_data.items()
    }
    return clean_json


def clean_current_time_json(raw_json: dict[str, Any]) -> dict[str, Any]:
    '''Преобразовать json, если он был получен в режиме <current>.'''
    clean_json = {}
    clean_json['location'] = {
        'latitude': raw_json.get('latitude'),
        'longitude': raw_json.get('longitude')
    }
    clean_json['timezone'] = raw_json.get('timezone')
    clean_json['current_units'] = raw_json.get('current_units')
    clean_json['current_units'].pop('interval')
    clean_json['current_units'].pop('time')
    clean_json['current'] = raw_json.get('current')
    clean_json['current'].pop('interval')
    return clean_json


def clean_json_from_api(raw_json: dict[str, Any], mode: str) -> dict[str, Any]:
    '''
    Преобразовать полученный от внешнего API json в зависимости от переданного
    режима: hourly - почасовой прогноз на текущий день, current - прогноз на
    текущий момент.
    '''
    if mode == 'hourly':
        return clean_hourly_json(raw_json)
    elif mode == 'current':
        return clean_current_time_json(raw_json)
    raise ValueError(f'Невалидный режим: {mode}')


def create_json_weather(
    raw_data: dict[str, Any],
    hour: int,
    attrs: list[str]
) -> dict[str, float]:
    weather_data = {}
    for key, value in raw_data.items():
        if key in attrs:
            weather_data[key] = float(value.split(',')[hour])
    return weather_data
