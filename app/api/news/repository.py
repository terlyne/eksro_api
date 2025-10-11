from sqlalchemy.ext.asyncio import AsyncSession

from core.models import News, NewsType
from repository.base import BaseRepository


class NewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=News)


class NewsTypeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=NewsType)
