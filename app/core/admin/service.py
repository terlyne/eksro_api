import string
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.user import User, ADMIN_ROLE


class AdminService:

    @classmethod
    async def create_admin(cls, session: AsyncSession) -> bool:
        # Проверяем, не существует ли уже админ
        exisiting_admin = await session.scalar(
            select(User).where(User.role == ADMIN_ROLE)
        )

        if exisiting_admin:
            return False

        admin = User(
            email=settings.admin.email,
            username=settings.admin.username,
            password="adminadmin",
            role=ADMIN_ROLE,
            is_active=True,
        )

        session.add(admin)
        await session.commit()
