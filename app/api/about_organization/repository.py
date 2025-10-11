from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AboutOrganization
from repository.base import BaseRepository


class AboutOrganizationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=AboutOrganization)
