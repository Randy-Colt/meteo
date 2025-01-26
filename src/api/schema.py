from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from core.constants import (
    MAX_LATITUDE,
    MAX_LONGITUDE,
    MAX_USERNAME,
    MIN_LATITUDE,
    MIN_LONGITUDE,
    MIN_USERNAME
)

LatitudeConstrainted = Annotated[
    float, Query(ge=MIN_LATITUDE, le=MAX_LATITUDE)
]
LongitudeConstrainted = Annotated[
    float, Query(ge=MIN_LONGITUDE, le=MAX_LONGITUDE)
]


class CitySchema(BaseModel):
    '''Схема для добавления города в список отслеживаемых.'''

    name: str
    latitude: LatitudeConstrainted
    longitude: LongitudeConstrainted


class UserRegistrationSchema(BaseModel):
    '''Схема для получения id по юзернейму.'''

    username: Annotated[
        str,
        Query(min_length=MIN_USERNAME, max_length=MAX_USERNAME)
    ]
