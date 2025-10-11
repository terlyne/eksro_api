from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Project
from repository.base import BaseRepository


class ProjectRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Project)
