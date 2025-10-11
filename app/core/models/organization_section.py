from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.news_type import NewsType


class OrganizationSupportDocument(Base, IdMixin):
    """
    Модель для хранения документов сопровождения управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_support_documents"

    # Заголовок/название документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class OrganizationSupportEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий сопровождения управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_support_events"

    # Заголовок/название мероприятия
    title: Mapped[str] = mapped_column(Text())

    # Описание мероприятия
    description: Mapped[str] = mapped_column(Text())

    # Изображение мероприятия
    image_url: Mapped[str] = mapped_column(Text())

    # Активно ли мероприятие
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    # Дата в формате dd.mm.YYYY hh:mm
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Локация
    location: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OrganizationSupportApplication(Base, IdMixin):
    """
    Модель для хранения заявок сопровождения управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_support_applications"

    # Тип заявки ("Консультация", "Вступление в УС", "Другое")
    application_type: Mapped[str] = mapped_column(String(50))

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Сам текст заявки
    text: Mapped[str] = mapped_column(Text())


class OrganizationLeader(Base, IdMixin):
    """
    Модель для хранения лидеров управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_leaders"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография члена Управляющего совета (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OrganizationNews(Base, IdMixin):
    """
    Модель для хранения новостей управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_news"

    # Заголовок
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок
    subtitle: Mapped[str] = mapped_column(Text())

    # Сам текст новости (описание)
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class OrganizationQuestion(Base, IdMixin):
    """
    Модель для хранения вопросов управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_questions"

    # Имя
    name: Mapped[str] = mapped_column(Text())

    # Номер телефона (опционально)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Текст сообщения/вопроса
    message: Mapped[str] = mapped_column(Text())

    # Флаг, отвечающий на вопрос: отвечено ли
    is_answered: Mapped[bool] = mapped_column(default=False)

    # Ответ на вопрос
    response: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OrganizationContact(Base, IdMixin):
    """
    Модель для хранения контактов управляющих советов в разделе "Образовательным организациям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ORGANIZATIONS
    )

    __tablename__ = "organization_contacts"

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Контактная эл. почта
    email: Mapped[str] = mapped_column(String(320))

    # Ссылка на ТГ-канал
    tg_channel: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Ссылка на сообщество ВК
    vk_group: Mapped[str | None] = mapped_column(Text(), nullable=True)
