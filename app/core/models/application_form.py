from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class ApplicationForm(Base, IdMixin):
    """
    Модель для хранения различных форм заявок на сайте
    """

    __tablename__ = "application_forms"

    # Тип заявки
    application_type: Mapped[str] = mapped_column(String(100))

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Номер телефона
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Текст заявки
    text: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Флаг, отвечающий на вопрос: обработана ли заявка
    is_processed: Mapped[bool] = mapped_column(default=False)
