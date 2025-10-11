from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, ARRAY, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection, ParentSubpage
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.news_type import NewsType


class ParentDocument(Base, IdMixin):
    """
    Модель для хранения документов в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        nullable=True,
    )

    __tablename__ = "parent_documents"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class ParentContact(Base, IdMixin):
    """
    Модель для хранения контактов в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        nullable=True,
    )

    __tablename__ = "parent_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Дисциплина ответственного лица
    discipline: Mapped[str] = mapped_column(Text())

    # Контактный Email
    email: Mapped[str] = mapped_column(String(320))

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))


class ThematicMeetingParticipant(Base, IdMixin):
    """
    Модель для хранения участников тематических встреч в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.THEMATIC_MEETINGS,
        nullable=True,
    )

    __tablename__ = "thematic_meeting_participants"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class ThematicMeetingEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий тематических встреч в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.THEMATIC_MEETINGS,
        nullable=True,
    )

    __tablename__ = "thematic_meeting_events"

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


class ThematicMeetingContact(Base, IdMixin):
    """
    Модель для хранения контактов тематических встреч в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.THEMATIC_MEETINGS,
        nullable=True,
    )

    __tablename__ = "thematic_meeting_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Должность
    position: Mapped[str] = mapped_column(Text())

    # Контактный Email
    email: Mapped[str] = mapped_column(String(320))

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Фотография ответственного лица
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class EtiquetteInEducationDocument(Base, IdMixin):
    """
    Модель для хранения документов проекта "Этикет в образовании" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.ETIQUETTE_IN_EDUCATION,
        nullable=True,
    )

    __tablename__ = "etiquette_in_education_documents"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class EtiquetteInEducationEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий проекта "Этикет в образовании" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.ETIQUETTE_IN_EDUCATION,
        nullable=True,
    )

    __tablename__ = "etiquette_in_education_events"

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


class EtiquetteInEducationContact(Base, IdMixin):
    """
    Модель для хранения контактов проекта "Этикет в образовании" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.ETIQUETTE_IN_EDUCATION,
        nullable=True,
    )

    __tablename__ = "etiquette_in_education_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Должность
    position: Mapped[str] = mapped_column(Text())

    # Контактный Email
    email: Mapped[str] = mapped_column(String(320))

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Фотография ответственного лица
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class ProfessionalLearningTrajectoryDocument(Base, IdMixin):
    """
    Модель для хранения документов проекта "Профессиональная траектория обучения ребенка" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.PROFESSIONAL_LEARNING_TRAJECTORY_CHILD,
        nullable=True,
    )

    __tablename__ = "professional_learning_trajectory_documents"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class ProfessionalLearningTrajectoryParticipant(Base, IdMixin):
    """
    Модель для хранения участников проекта "Профессиональная траектория обучения ребенка" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.PROFESSIONAL_LEARNING_TRAJECTORY_CHILD,
        nullable=True,
    )

    __tablename__ = "professional_learning_trajectory_participants"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class ProfessionalLearningTrajectoryEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий проекта "Профессиональная траектория обучения ребенка" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.PROFESSIONAL_LEARNING_TRAJECTORY_CHILD,
        nullable=True,
    )

    __tablename__ = "professional_learning_trajectory_events"

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


class ProfessionalLearningTrajectoryContact(Base, IdMixin):
    """
    Модель для хранения контактов проекта "Профессиональная траектория обучения ребенка" в разделе "Родителям"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.PARENTS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[ParentSubpage] = mapped_column(
        SQLEnum(ParentSubpage, name="parentsubpage_enum"),
        default=ParentSubpage.PROFESSIONAL_LEARNING_TRAJECTORY_CHILD,
        nullable=True,
    )

    __tablename__ = "professional_learning_trajectory_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Должность
    position: Mapped[str] = mapped_column(Text())

    # Контактный Email (опционально)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))
