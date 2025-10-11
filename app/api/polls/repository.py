from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Poll, PollAnswer
from repository.base import BaseRepository


class PollRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Poll)


class PollAnswerRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=PollAnswer)
