from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Event
from repository.base import BaseRepository


class EventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Event)
