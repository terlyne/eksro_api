from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.news_type import NewsType


class OrganizationSupportDocument(Base, IdMixin):
    """
    Модель для хранения документов сопровождения управляющих советов в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_support_documents"

    # Заголовок/название документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class OrganizationSupportEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий сопровождения управляющих советов в разделе "Образовательным организациям"
    """

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

    __tablename__ = "organization_contacts"

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))

    # Контактная эл. почта
    email: Mapped[str] = mapped_column(String(320))

    # Ссылка на ТГ-канал
    tg_channel: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Ссылка на сообщество ВК
    vk_group: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OrganizationEducationalProgramDocument(Base, IdMixin):
    """
    Модель для хранения документов образовательных программ в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_educational_program_documents"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class OrganizationEducationalProgramContact(Base, IdMixin):
    """
    Модель для хранения контактов образовательных программ в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_educational_program_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Дисциплина ответственного лица
    discipline: Mapped[str] = mapped_column(Text())

    # Контактный Email
    email: Mapped[str] = mapped_column(String(320))

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))


class OrganizationThematicMeetingParticipant(Base, IdMixin):
    """
    Модель для хранения участников тематических встреч в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_thematic_meeting_participants"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OrganizationThematicMeetingEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий тематических встреч в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_thematic_meeting_events"

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


class OrganizationThematicMeetingContact(Base, IdMixin):
    """
    Модель для хранения контактов тематических встреч в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_thematic_meeting_contacts"

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


class OrganizationEtiquetteInEducationDocument(Base, IdMixin):
    """
    Модель для хранения документов проекта "Этикет в образовании" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_etiquette_in_education_documents"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class OrganizationEtiquetteInEducationEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий проекта "Этикет в образовании" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_etiquette_in_education_events"

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


class OrganizationEtiquetteInEducationContact(Base, IdMixin):
    """
    Модель для хранения контактов проекта "Этикет в образовании" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_etiquette_in_education_contacts"

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


class OrganizationProfessionalLearningTrajectoryDocument(Base, IdMixin):
    """
    Модель для хранения документов проекта "Профессиональная траектория обучения ребенка" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_professional_learning_trajectory_documents"

    # Название/заголовок документа
    title: Mapped[str] = mapped_column(Text())

    # Сам файл документа
    file_url: Mapped[str] = mapped_column(Text())


class OrganizationProfessionalLearningTrajectoryParticipant(Base, IdMixin):
    """
    Модель для хранения участников проекта "Профессиональная траектория обучения ребенка" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_professional_learning_trajectory_participants"

    # Имя
    first_name: Mapped[str] = mapped_column(Text())

    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())

    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)


class OrganizationProfessionalLearningTrajectoryEvent(Base, IdMixin):
    """
    Модель для хранения мероприятий проекта "Профессиональная траектория обучения ребенка" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_professional_learning_trajectory_events"

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


class OrganizationProfessionalLearningTrajectoryContact(Base, IdMixin):
    """
    Модель для хранения контактов проекта "Профессиональная траектория обучения ребенка" в разделе "Образовательным организациям"
    """

    __tablename__ = "organization_professional_learning_trajectory_contacts"

    # ФИО
    full_name: Mapped[str] = mapped_column(Text())

    # Должность
    position: Mapped[str] = mapped_column(Text())

    # Контактный Email (опционально)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)

    # Контактный номер телефона
    phone: Mapped[str] = mapped_column(String(40))
