from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Document
from repository.base import BaseRepository


class DocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Document)
