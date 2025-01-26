### Описание

Приложение **meteo** позволяет каждому пользователю получать актуальные данные о погоде, а после регистрации пользователи могут отслеживать прогноз погоды на текущий день. Прогноз погоды для каждого города обновляется каждые 15 минут.


### Стек основных технологий

- Python 3.10
- FastAPI 0.115.6
- Uvicorn 0.34


### Запуск проекта

Клонируйте репозиторий:
```
git clone https://github.com/Randy-Colt/meteo.git
cd meteo
```
Установите зависимости
```
pip install -r requerements.txt
```
Зайдите в директорию приложения и запустите его
```
cd src/
python script.py
```


### Примеры запросов и ответов

1. Получить прогноз погоды на текущий час по координатам.
request GET:
```
http://127.0.0.1:8000/api/weather?latitude=55.7522&longitude=37.6156
```
response:
```
{
    "location": {
        "latitude": 55.75,
        "longitude": 37.625
    },
    "timezone": "Europe/Moscow",
    "current_units": {
        "temperature_2m": "°C",
        "surface_pressure": "hPa",
        "wind_speed_10m": "m/s"
    },
    "current": {
        "time": "2025-01-26T21:30",
        "temperature_2m": 2.5,
        "surface_pressure": 1000.9,
        "wind_speed_10m": 1.62
    }
}
```

2. Получить id пользователя по юзернейму. Если пользователь уже зарегестрировал юзернейм, то получит тот же id, что и после первой регистрации.
request POST:
```
http://127.0.0.1:8000/api/registration
```
request body:
```
{
    "username": "User"
}
```
response:
```
"e0aa5fa4-060c-4912-b836-738bb5e33eb1"
```

3. Добавить в список пользователя город, прогноз погоды для которого будет отслеживаться.
request POST:
```
http://127.0.0.1:8000/api/{user_id}/add-city
```
request body:
```
{
    "name": "Ryazan",
    "latitude":  54.6269,
    "longitude": 39.6916
}
```
response:
```
{
    "message": "Город Ryazan успешно добавлен!"
}
```

4. Получить пользовательский список городов, для которых доступен прогноз погоды.
request GET:
```
http://127.0.0.1:8000/api/{user_id}/cities
```
response:
```
{
    "Ryazan"
}
```

5. Получить погоду для указанного города на текущий день в указанный час. Есть возможность указать параметры погоды.
Запрос без параметров:
request GET:
```
http://127.0.0.1:8000/api/e0aa5fa4-060c-4912-b836-738bb5e33eb1/city-weather?city_name=Ryazan&hour=12
```
response:
```
{
    "city_name": "Ryazan",
    "timezone": "Europe/Moscow",
    "time": "12:00",
    "weather": {
        "precipitation": 0.0,
        "temperature": 1.8,
        "wind_speed": 3.36,
        "relative_humidity": 92.0
    },
    "measurement_units": {
        "temperature": "°C",
        "relative_humidity": "%",
        "precipitation": "mm",
        "wind_speed": "m/s"
    }
}
```
Запрос с параметрами:
request GET:
```
http://127.0.0.1:8000/api/e0aa5fa4-060c-4912-b836-738bb5e33eb1/city-weather?params=temperature,relative_humidity&city_name=Ryazan&hour=14
```
response:
```
{
    "city_name": "Ryazan",
    "timezone": "Europe/Moscow",
    "time": "14:00",
    "weather": {
        "temperature": 2.6,
        "relative_humidity": 90.0
    },
    "measurement_units": {
        "temperature": "°C",
        "relative_humidity": "%",
        "precipitation": "mm",
        "wind_speed": "m/s"
    }
}
```