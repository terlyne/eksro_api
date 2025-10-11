from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    OrganizationSupportDocument,
    OrganizationSupportEvent,
    OrganizationSupportApplication,
    OrganizationLeader,
    OrganizationNews,
    OrganizationQuestion,
    OrganizationContact,
)
from repository.base import BaseRepository


class OrganizationSupportDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationSupportDocument,
        )


class OrganizationSupportEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationSupportEvent,
        )


class OrganizationSupportApplicationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationSupportApplication,
        )


class OrganizationLeaderRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationLeader,
        )


class OrganizationNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationNews,
        )


class OrganizationQuestionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationQuestion,
        )


class OrganizationContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationContact,
        )
