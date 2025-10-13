from datetime import date

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Contact(Base, IdMixin):

    # Контактный email
    email: Mapped[str] = mapped_column(String(320), nullable=True)
    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))
    # Адрес организации
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    # ВК группа ссылка
    vk_group: Mapped[str] = mapped_column(Text(), nullable=True)  # Ссылка на группу ВК
    # ТГ канал ссылка
    tg_channel: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # Ссылка на канал в телеграмме
    # Дисциплина ответственного лица
    discipline: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # Название дисциплины ответственного лица
    # Фотография ответственного лица
    image_url: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # URL изображения ответсвенного лица
    # Режим и график работы
    work_hours: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # Часы работы
    # Дата создания организации
    date_of_created: Mapped[date] = mapped_column(
        nullable=True
    )  # Дата создания организации
    # Полное наименование образовательной организации
    full_name: Mapped[str] = mapped_column(
        Text(), nullable=True
    )  # Полное название организации
    # Сокращенное наименование организации
    short_name: Mapped[str] = mapped_column(
        Text(), nullable=True
    )  # Сокращенное название организации
    # Учредитель образовательной организации
    organization_founder: Mapped[str] = mapped_column(
        Text(), nullable=True
    )  # Учредитель-компания организации
