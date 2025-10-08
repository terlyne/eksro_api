from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.mixins.id import IdMixin
from core.models.base import Base


class SiteImage(Base, IdMixin):
    __tablename__ = "site_images"

    name: Mapped[str] = mapped_column(Text())
    image_url: Mapped[str] = mapped_column(Text())
