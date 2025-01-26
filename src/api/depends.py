from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import get_city_by_name, get_user
from api.schema import CitySchema
from core.db_settings import db_helper
from core.models import User


async def get_user_by_id(
    user_id: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> User:
    '''Получить пользователя по id или error 404 в случае его отсутствия.'''
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Пользователь не найден.'
        )
    return user


async def check_city(
    city_schema: CitySchema,
    user_id: str,
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> None:
    '''Проверить, есть ли город в списке пользователя.'''
    city = await get_city_by_name(session, city_schema.name, user)
    if city is not None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f'Город {city_schema.name} уже отслеживается.'
        )
    return city_schema
