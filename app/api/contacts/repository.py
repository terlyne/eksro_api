from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Contact
from repository.base import BaseRepository


class ContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Contact)
