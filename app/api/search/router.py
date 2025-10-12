import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.search.repository import SearchRepository
from api.search.schemas import SearchResult


router = APIRouter()


@router.get("/", response_model=list[SearchResult])
async def search_entities(
    query: Annotated[str, Query(min_length=1)],
    entity_type: Annotated[
        str | None, Query()
    ] = None,  # Тип сущности для поиска (опционально)
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Поиск по всем сущностям или по определенному типу сущности

    :param query: Поисковый запрос
    :param entity_type: Тип сущности для поиска (опционально)
    :param skip: Смещение для пагинации
    :param limit: Лимит результатов для пагинации
    :param session: Сессия базы данных
    :param user: Текущий активный пользователь
    :return: Список результатов поиска
    """
    search_repo = SearchRepository(session)

    # Если указан тип сущности, ищем только по этому типу
    if entity_type:
        results = await search_repo.search_by_entity_type(
            query=query,
            entity_type=entity_type,
            skip=skip,
            limit=limit,
        )
    else:
        # Иначе ищем по всем сущностям
        results = await search_repo.search_all(
            query=query,
            skip=skip,
            limit=limit,
        )

    return results


@router.get("/suggestions/", response_model=list[str])
async def get_search_suggestions(
    query: Annotated[str, Query(min_length=1)],
    entity_type: Annotated[
        str | None, Query()
    ] = None,  # Тип сущности для получения подсказок (опционально)
    limit: Annotated[int, Query(ge=1, le=10)] = 5,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Получение подсказок для поиска по всем сущностям или по определенному типу сущности

    :param query: Поисковый запрос
    :param entity_type: Тип сущности для получения подсказок (опционально)
    :param limit: Лимит подсказок
    :param session: Сессия базы данных
    :param user: Текущий активный пользователь
    :return: Список подсказок для поиска
    """
    search_repo = SearchRepository(session)

    # Если указан тип сущности, получаем подсказки только по этому типу
    if entity_type:
        suggestions = await search_repo.get_suggestions_by_entity_type(
            query=query,
            entity_type=entity_type,
            limit=limit,
        )
    else:
        # Иначе получаем подсказки по всем сущностям
        suggestions = await search_repo.get_all_suggestions(
            query=query,
            limit=limit,
        )

    return suggestions
