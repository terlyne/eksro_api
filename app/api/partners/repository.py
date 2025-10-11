from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Partner
from repository.base import BaseRepository


class PartnerRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Partner)
