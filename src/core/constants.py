# URL-адрес апи
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast/'

# Время в секундах
FIFTEEN_MINUTES = 60 * 15

# Минимальный и максимальный возможный час
MIN_HOUR = 0
MAX_HOUR = 23

# Минимальные и максимальные значения широты и долготы
MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180

# Максимальное количество символов для названия города
MAX_CITY_NAME = 50

# Максимальное и минимальное количество символов для юзернейма
MAX_USERNAME = 10
MIN_USERNAME = 3

# Параметры по умолчанию для получения прогноза погоды на выбраный час
DEFAULT_WEATHER_PARAMS = (
    'temperature,relative_humidity,'
    'wind_speed,precipitation'
)
# Те же параметры по умолчанию в виде кортежа
DEFAULT_SPLITED_WEATHER_PARAMS = (
    'temperature', 'relative_humidity',
    'wind_speed', 'precipitation'
)
