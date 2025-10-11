from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Feedback
from repository.base import BaseRepository


class FeedbackRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Feedback)
