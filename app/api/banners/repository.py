from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Banner
from repository.base import BaseRepository


class BannerRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Banner)
