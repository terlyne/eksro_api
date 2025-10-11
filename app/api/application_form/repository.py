from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ApplicationForm
from repository.base import BaseRepository


class ApplicationFormRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ApplicationForm)
