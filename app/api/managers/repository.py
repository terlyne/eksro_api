from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Manager
from repository.base import BaseRepository


class ManagerRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Manager)
