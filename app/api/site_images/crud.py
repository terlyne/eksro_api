from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.site_image import SiteImage


async def create_site_image(
    session: AsyncSession,
    name: str,
    image_url: str,
) -> SiteImage:
    site_image = SiteImage(name=name, image_url=image_url)
    session.add(site_image)

    await session.commit()
    await session.refresh(site_image)

    return site_image


async def get_site_images(
    session: AsyncSession,
) -> list[SiteImage]:
    stmt = select(SiteImage).order_by(desc(SiteImage.created_at))
    result = await session.scalars(stmt)
    return list(result.all())
