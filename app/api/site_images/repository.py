from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SiteImage
from repository.base import BaseRepository


class SiteImageRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SiteImage)
