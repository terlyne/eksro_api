from sqlalchemy import select, or_, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import News
from repository.base import BaseRepository


class SearchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_entity_type(
        self, query: str, entity_type: str, skip: int, limit: int
    ):
        # Для упрощения возвращаем пустой список, т.к. в проекте нет других сущностей
        return []

    async def search_all(self, query: str, skip: int, limit: int):
        # Используем существующую функцию для поиска новостей
        return await search_news(self.session, query, limit, skip)

    async def get_suggestions_by_entity_type(
        self, query: str, entity_type: str, limit: int
    ):
        # Для упрощения возвращаем пустой список
        return []

    async def get_all_suggestions(self, query: str, limit: int):
        # Используем существующую функцию для получения подсказок
        return await get_suggestions(self.session, query, limit)


async def get_suggestions(
    session: AsyncSession,
    query: str,
    limit: int = 5,
) -> list[str]:
    stmt = (
        select(News)
        .where(
            or_(
                News.title.ilike(f"%{query}%"),
                News.keywords.any(query),
            )
        )
        .limit(limit * 3)
        .order_by(desc(News.news_date))
    )

    result = await session.scalars(stmt)
    news_items = result.all()
    suggestions = set()

    for news in news_items:
        # Добавляем заголовок если совпадает
        if query.lower() in news.title.lower():
            suggestions.add(news.title)

        # Добавляем подходящие keywords
        for keyword in news.keywords:
            if query.lower() in keyword.lower():
                suggestions.add(keyword)

        # Ограничиваем количество
        if len(suggestions) >= limit:
            break

    return list(suggestions)[:limit]


async def search_news(
    session: AsyncSession,
    query: str,
    limit: int = 10,
    skip: int = 0,
) -> list[News]:
    stmt = (
        select(News)
        .options(joinedload(News.type))
        .where(
            or_(
                News.title.ilike(f"%{query}%"),
                News.keywords.any(query),
                News.min_text.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .offset(skip)
        .order_by(desc(News.news_date))
    )

    result = await session.scalars(stmt)
    return list(result.all())
