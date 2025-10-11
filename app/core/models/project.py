from sqlalchemy import Text, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Project(Base, IdMixin):
    __tablename__ = "projects"

    title: Mapped[str] = mapped_column(Text, nullable=False)
    project_url: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    min_text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    theme: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
