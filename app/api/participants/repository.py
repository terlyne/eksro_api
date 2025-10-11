from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Participant
from repository.base import BaseRepository


class ParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Participant)
