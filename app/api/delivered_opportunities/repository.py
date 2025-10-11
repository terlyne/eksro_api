from sqlalchemy.ext.asyncio import AsyncSession

from core.models import DeliveredOpportunity
from repository.base import BaseRepository


class DeliveredOpportunityRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=DeliveredOpportunity)
