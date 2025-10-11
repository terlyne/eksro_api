from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection, SovietSubpage
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.news_type import NewsType


class SovietSupportDocument(Base, IdMixin):
    """
    Модель для хранения документов сопровождения управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_support_documents"

    # Заголовок/название документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class SovietSupportEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий сопровождения управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_support_events"

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


class SovietSupportApplication(Base, IdMixin):
    """
    Модель для хранения заявок сопровождения управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_support_applications"

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


class SovietLeader(Base, IdMixin):
    """
    Модель для хранения лидеров управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_leaders"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография члена Управляющего совета (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class SovietNews(Base, IdMixin):
    """
    Модель для хранения новостей управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_news"

    # Заголовок
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок
    subtitle: Mapped[str] = mapped_column(Text())

    # Сам текст новости (описание)
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class SovietQuestion(Base, IdMixin):
    """
    Модель для хранения вопросов управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_questions"

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


class SovietContact(Base, IdMixin):
    """
    Модель для хранения контактов управляющих советов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.SUPPORT_SOVIETS,
        nullable=True,
    )

    __tablename__ = "soviet_contacts"

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Контактная эл. почта
    email: Mapped[str] = mapped_column(String(320))

    # Ссылка на ТГ-канал
    tg_channel: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Ссылка на сообщество ВК
    vk_group: Mapped[str | None] = mapped_column(Text(), nullable=True)


class LearningDocument(Base, IdMixin):
    """
    Модель для хранения документов в разделе "Обучение"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.LEARNING,
        nullable=True,
    )

    __tablename__ = "learning_documents"

    # Название/Заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class LearningEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий в разделе "Обучение"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.LEARNING,
        nullable=True,
    )

    __tablename__ = "learning_events"

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


class LearningApplication(Base, IdMixin):
    """
    Модель для хранения заявок в разделе "Обучение"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.LEARNING,
        nullable=True,
    )

    __tablename__ = "learning_applications"

    # Тип заявки ("Платное", "Бесплатное" или "Другое")
    application_type: Mapped[str] = mapped_column(String(50))

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Номер телефона (опциональное поле)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Сам текст заявки
    text: Mapped[str] = mapped_column(Text())


class LearningNews(Base, IdMixin):
    """
    Модель для хранения новостей в разделе "Обучение"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.LEARNING,
        nullable=True,
    )

    __tablename__ = "learning_news"

    # Заголовок новости
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок
    subtitle: Mapped[str] = mapped_column(Text())

    # Текст новости
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class LearningQuestion(Base, IdMixin):
    """
    Модель для хранения вопросов в разделе "Обучение"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.LEARNING,
        nullable=True,
    )

    __tablename__ = "learning_questions"

    # Имя
    name: Mapped[str] = mapped_column(Text())

    # Номер телефона (опционально)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Текст вопроса
    message: Mapped[str] = mapped_column(Text())

    # Флаг, отвечающий на вопрос: отвечено ли
    is_answered: Mapped[bool] = mapped_column(default=False)

    # Ответ на вопрос
    response: Mapped[str | None] = mapped_column(Text(), nullable=True)


class LearningContact(Base, IdMixin):
    """
    Модель для хранения контактов в разделе "Обучение"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.LEARNING,
        nullable=True,
    )

    __tablename__ = "learning_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Фотография ответственного лица
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Описание
    description: Mapped[str] = mapped_column(Text())

    # Контактная эл. почта
    email: Mapped[str] = mapped_column(String(320))

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))


class OnlineConferenceRegulation(Base, IdMixin):
    """
    Модель для хранения регламентов онлайн селекторных совещаний в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.ONLINE_CONFERENCE_CALLS,
        nullable=True,
    )

    __tablename__ = "online_conference_regulations"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл регламента
    file_url: Mapped[str] = mapped_column(Text())


class OnlineConferenceParticipant(Base, IdMixin):
    """
    Модель для хранения участников онлайн селекторных совещаний в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.ONLINE_CONFERENCE_CALLS,
        nullable=True,
    )

    __tablename__ = "online_conference_participants"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OnlineConferenceNews(Base, IdMixin):
    """
    Модель для хранения новостей онлайн селекторных совещаний в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.ONLINE_CONFERENCE_CALLS,
        nullable=True,
    )

    __tablename__ = "online_conference_news"

    # Заголовок
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок
    subtitle: Mapped[str] = mapped_column(Text())

    # Сам текст новости (описание)
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class OnlineConferenceQuestion(Base, IdMixin):
    """
    Модель для хранения вопросов онлайн селекторных совещаний в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.ONLINE_CONFERENCE_CALLS,
        nullable=True,
    )

    __tablename__ = "online_conference_questions"

    # Имя
    name: Mapped[str] = mapped_column(Text())

    # Номер телефона (опционально)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Текст вопроса
    message: Mapped[str] = mapped_column(Text())

    # Флаг, отвечающий на вопрос: отвечено ли
    is_answered: Mapped[bool] = mapped_column(default=False)

    # Ответ на вопрос
    response: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OnlineConferenceContact(Base, IdMixin):
    """
    Модель для хранения контактов онлайн селекторных совещаний в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.ONLINE_CONFERENCE_CALLS,
        nullable=True,
    )

    __tablename__ = "online_conference_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Описание
    description: Mapped[str] = mapped_column(Text())

    # Изображение ответственного лица
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Контактная эл. почта
    email: Mapped[str] = mapped_column(String(320))


class PodcastApplication(Base, IdMixin):
    """
    Модель для хранения заявок подкастов с командами УС в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.PODCASTS_WITH_SOVIET_TEAMS,
        nullable=True,
    )

    __tablename__ = "podcast_applications"

    # Тип заявки ("Образовательный", "Разговорный" или "Другое")
    application_type: Mapped[str] = mapped_column(String(50))

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Номер телефона (опционально)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Сам текст запроса
    text: Mapped[str] = mapped_column(Text())


class PodcastParticipant(Base, IdMixin):
    """
    Модель для хранения участников подкастов с командами УС в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.PODCASTS_WITH_SOVIET_TEAMS,
        nullable=True,
    )

    __tablename__ = "podcast_participants"

    # Видео
    video_url: Mapped[str] = mapped_column(Text())

    # Гости (несколько ФИО)
    guests: Mapped[list[str]] = mapped_column(Text())  # В виде JSON строки


class PodcastNews(Base, IdMixin):
    """
    Модель для хранения новостей подкастов с командами УС в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.PODCASTS_WITH_SOVIET_TEAMS,
        nullable=True,
    )

    __tablename__ = "podcast_news"

    # Заголовок
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок
    subtitle: Mapped[str] = mapped_column(Text())

    # Сам текст новости (описание)
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class PodcastContact(Base, IdMixin):
    """
    Модель для хранения контактов подкастов с командами УС в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.PODCASTS_WITH_SOVIET_TEAMS,
        nullable=True,
    )

    __tablename__ = "podcast_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Описание
    description: Mapped[str] = mapped_column(Text())

    # Фотография ответственного лица
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Контактный адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))


class ProjectNews(Base, IdMixin):
    """
    Модель для хранения новостей банка проектов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.PROJECTS_BANK,
        nullable=True,
    )

    __tablename__ = "project_news"

    # Заголовок
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок
    subtitle: Mapped[str] = mapped_column(Text())

    # Текст новости
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class ProjectReport(Base, IdMixin):
    """
    Модель для хранения отчетов банка проектов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.PROJECTS_BANK,
        nullable=True,
    )

    __tablename__ = "project_reports"

    # Наименование образовательной организации
    organization_name: Mapped[str] = mapped_column(Text())

    # Видео отчета
    video_url: Mapped[str] = mapped_column(Text())


class CompetitionDocument(Base, IdMixin):
    """
    Модель для хранения документов конкурса в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.COMPETITION,
        nullable=True,
    )

    __tablename__ = "competition_documents"

    # Название документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class CompetitionContact(Base, IdMixin):
    """
    Модель для хранения контактов конкурса в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.SOVIETS
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        default=SovietSubpage.COMPETITION,
        nullable=True,
    )

    __tablename__ = "competition_contacts"

    # Название ответственной организации
    organization_name: Mapped[str] = mapped_column(Text())

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Контактный адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))


class JournalNews(Base, IdMixin):
    """
    Модель для хранения новостей журналов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        nullable=True,
    )

    __tablename__ = "journal_news"

    # Заголовок новости
    title: Mapped[str] = mapped_column(Text())

    # Подзаголовок новости
    subtitle: Mapped[str] = mapped_column(Text())

    # Текст новости
    description: Mapped[str] = mapped_column(Text())

    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())


class JournalContact(Base, IdMixin):
    """
    Модель для хранения контактов журналов в разделе "Управляющим советам"
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[SovietSubpage] = mapped_column(
        SQLEnum(SovietSubpage, name="sovietsubpage_enum"),
        nullable=True,
    )

    __tablename__ = "journal_contacts"

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Контактный адрес эл. почты
    email: Mapped[str] = mapped_column(String(320))

    # Адрес
    address: Mapped[str] = mapped_column(Text())
