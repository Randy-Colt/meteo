from core.constants import (
    DEFAULT_WEATHER_PARAMS,
    DEFAULT_SPLITED_WEATHER_PARAMS
)


def split_and_check_params(params: str) -> list[str] | None:
    '''
    Разделяет параметры на список строк и проверяет на соответствие допустимым.
    '''
    if params is DEFAULT_WEATHER_PARAMS:
        return params.split(',')
    splited_params = params.split(',')
    for param in splited_params:
        if param not in DEFAULT_SPLITED_WEATHER_PARAMS:
            return None
    return splited_params
