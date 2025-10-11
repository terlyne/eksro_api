from typing import Annotated
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SovietSupportDocumentBase(BaseModel):
    # Заголовок/название документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class SovietSupportDocumentCreate(SovietSupportDocumentBase):
    pass


class SovietSupportDocumentUpdate(SovietSupportDocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class SovietSupportDocumentResponse(SovietSupportDocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class SovietSupportEventBase(BaseModel):
    # Заголовок/название мероприятия
    title: Annotated[str, Field(max_length=200)]
    # Описание мероприятия
    description: Annotated[str, Field(max_length=1000)]
    # Изображение мероприятия
    image_url: Annotated[str, Field(max_length=500)]
    # Активно ли мероприятие
    is_active: bool = True
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: datetime
    # Локация
    location: Annotated[str, Field(max_length=20)] | None = None


class SovietSupportEventCreate(SovietSupportEventBase):
    pass


class SovietSupportEventUpdate(SovietSupportEventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=20, default=None)]


class SovietSupportEventResponse(SovietSupportEventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class SovietSupportApplicationBase(BaseModel):
    # Тип заявки ("Консультация", "Вступление в УС", "Другое")
    application_type: Annotated[str, Field(max_length=50)]
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Сам текст заявки
    text: Annotated[str, Field(max_length=1000)]


class SovietSupportApplicationCreate(SovietSupportApplicationBase):
    pass


class SovietSupportApplicationUpdate(SovietSupportApplicationBase):
    application_type: Annotated[str | None, Field(max_length=50, default=None)]
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    text: Annotated[str | None, Field(max_length=100, default=None)]


class SovietSupportApplicationResponse(SovietSupportApplicationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class SovietLeaderBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=100)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=100)]
    # Фотография члена Управляющего совета (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class SovietLeaderCreate(SovietLeaderBase):
    pass


class SovietLeaderUpdate(SovietLeaderBase):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class SovietLeaderResponse(SovietLeaderBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class SovietNewsBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=20)]
    # Подзаголовок
    subtitle: Annotated[str, Field(max_length=200)]
    # Сам текст новости (описание)
    description: Annotated[str, Field(max_length=1000)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=500)]


class SovietNewsCreate(SovietNewsBase):
    pass


class SovietNewsUpdate(SovietNewsBase):
    title: Annotated[str | None, Field(max_length=20, default=None)]
    subtitle: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class SovietNewsResponse(SovietNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class SovietQuestionBase(BaseModel):
    # Имя
    name: Annotated[str, Field(max_length=100)]
    # Номер телефона (я так полагаю опциональное поле)
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Текст сообщения/вопроса
    message: Annotated[str, Field(max_length=1000)]
    # Ответ на вопрос
    response: Annotated[str, Field(max_length=1000)] | None = None


class SovietQuestionCreate(SovietQuestionBase):
    pass


class SovietQuestionUpdate(SovietQuestionBase):
    name: Annotated[str | None, Field(max_length=10, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    message: Annotated[str | None, Field(max_length=100, default=None)]
    response: Annotated[str | None, Field(max_length=100, default=None)]


class SovietQuestionResponse(SovietQuestionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class SovietContactBase(BaseModel):
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Контактная эл. почта
    email: Annotated[str, Field(max_length=320)]
    # Ссылка на ТГ-канал
    tg_channel: Annotated[str, Field(max_length=50)] | None = None
    # Ссылка на сообщество ВК
    vk_group: Annotated[str, Field(max_length=50)] | None = None


class SovietContactCreate(SovietContactBase):
    pass


class SovietContactUpdate(SovietContactBase):
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    tg_channel: Annotated[str | None, Field(max_length=500, default=None)]
    vk_group: Annotated[str | None, Field(max_length=500, default=None)]


class SovietContactResponse(SovietContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class LearningDocumentBase(BaseModel):
    # Название/Заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class LearningDocumentCreate(LearningDocumentBase):
    pass


class LearningDocumentUpdate(LearningDocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class LearningDocumentResponse(LearningDocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class LearningEventBase(BaseModel):
    # Заголовок/название мероприятия
    title: Annotated[str, Field(max_length=200)]
    # Описание мероприятия
    description: Annotated[str, Field(max_length=1000)]
    # Изображение мероприятия
    image_url: Annotated[str, Field(max_length=50)]
    # Активно ли мероприятие
    is_active: bool = True
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: datetime
    # Локация
    location: Annotated[str, Field(max_length=200)] | None = None


class LearningEventCreate(LearningEventBase):
    pass


class LearningEventUpdate(LearningEventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class LearningEventResponse(LearningEventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class LearningApplicationBase(BaseModel):
    # Тип заявки ("Платное", "Бесплатное" или "Другое")
    application_type: Annotated[str, Field(max_length=50)]
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Номер телефона (я так понимаю опциональное поле)
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Сам текст заявки
    text: Annotated[str, Field(max_length=1000)]


class LearningApplicationCreate(LearningApplicationBase):
    pass


class LearningApplicationUpdate(LearningApplicationBase):
    application_type: Annotated[str | None, Field(max_length=50, default=None)]
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    text: Annotated[str | None, Field(max_length=10, default=None)]


class LearningApplicationResponse(LearningApplicationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class LearningNewsBase(BaseModel):
    # Заголовок новости
    title: Annotated[str, Field(max_length=200)]
    # Подзаголовок
    subtitle: Annotated[str, Field(max_length=20)]
    # Текст новости
    description: Annotated[str, Field(max_length=1000)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=500)]


class LearningNewsCreate(LearningNewsBase):
    pass


class LearningNewsUpdate(LearningNewsBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    subtitle: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class LearningNewsResponse(LearningNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class LearningQuestionBase(BaseModel):
    # Имя
    name: Annotated[str, Field(max_length=100)]
    # Номер телефона (скорее всего опционально)
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Текст вопроса
    message: Annotated[str, Field(max_length=1000)]
    # Ответ на вопрос
    response: Annotated[str, Field(max_length=1000)] | None = None


class LearningQuestionCreate(LearningQuestionBase):
    pass


class LearningQuestionUpdate(LearningQuestionBase):
    name: Annotated[str | None, Field(max_length=10, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    message: Annotated[str | None, Field(max_length=10, default=None)]
    response: Annotated[str | None, Field(max_length=100, default=None)]


class LearningQuestionResponse(LearningQuestionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class LearningContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Фотография ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None
    # Описание
    description: Annotated[str, Field(max_length=500)]
    # Контактная эл. почта
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]


class LearningContactCreate(LearningContactBase):
    pass


class LearningContactUpdate(LearningContactBase):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    description: Annotated[str | None, Field(max_length=500, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]


class LearningContactResponse(LearningContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OnlineConferenceRegulationBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=20)]
    # Сам файл регламента
    file_url: Annotated[str, Field(max_length=500)]


class OnlineConferenceRegulationCreate(OnlineConferenceRegulationBase):
    pass


class OnlineConferenceRegulationUpdate(OnlineConferenceRegulationBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class OnlineConferenceRegulationResponse(OnlineConferenceRegulationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OnlineConferenceParticipantBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=100)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=100)]
    # Фотография участника (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class OnlineConferenceParticipantCreate(OnlineConferenceParticipantBase):
    pass


class OnlineConferenceParticipantUpdate(OnlineConferenceParticipantBase):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OnlineConferenceParticipantResponse(OnlineConferenceParticipantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OnlineConferenceNewsBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=200)]
    # Подзаголовок
    subtitle: Annotated[str, Field(max_length=200)]
    # Сам текст новости (описание)
    description: Annotated[str, Field(max_length=1000)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=500)]


class OnlineConferenceNewsCreate(OnlineConferenceNewsBase):
    pass


class OnlineConferenceNewsUpdate(OnlineConferenceNewsBase):
    title: Annotated[str | None, Field(max_length=20, default=None)]
    subtitle: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OnlineConferenceNewsResponse(OnlineConferenceNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OnlineConferenceQuestionBase(BaseModel):
    # Имя
    name: Annotated[str, Field(max_length=100)]
    # Номер телефона (скорее всего опционально)
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Текст вопроса
    message: Annotated[str, Field(max_length=1000)]
    # Ответ на вопрос
    response: Annotated[str, Field(max_length=1000)] | None = None


class OnlineConferenceQuestionCreate(OnlineConferenceQuestionBase):
    pass


class OnlineConferenceQuestionUpdate(OnlineConferenceQuestionBase):
    name: Annotated[str | None, Field(max_length=10, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    message: Annotated[str | None, Field(max_length=10, default=None)]
    response: Annotated[str | None, Field(max_length=10, default=None)]


class OnlineConferenceQuestionResponse(OnlineConferenceQuestionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OnlineConferenceContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Описание
    description: Annotated[str, Field(max_length=500)]
    # Изображение ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Контактная эл. почта
    email: Annotated[str, Field(max_length=320)]


class OnlineConferenceContactCreate(OnlineConferenceContactBase):
    pass


class OnlineConferenceContactUpdate(OnlineConferenceContactBase):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=500, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]


class OnlineConferenceContactResponse(OnlineConferenceContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PodcastApplicationBase(BaseModel):
    # Тип заявки ("Образовательный", "Разговорный" или "Другое")
    application_type: Annotated[str, Field(max_length=50)]
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Номер телефона (скорее всего опционально)
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Сам текст запроса
    text: Annotated[str, Field(max_length=1000)]


class PodcastApplicationCreate(PodcastApplicationBase):
    pass


class PodcastApplicationUpdate(PodcastApplicationBase):
    application_type: Annotated[str | None, Field(max_length=50, default=None)]
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    text: Annotated[str | None, Field(max_length=10, default=None)]


class PodcastApplicationResponse(PodcastApplicationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PodcastParticipantBase(BaseModel):
    # Видео
    video_url: Annotated[str, Field(max_length=500)]
    # Гости (несколько ФИО)
    guests: list[str]


class PodcastParticipantCreate(PodcastParticipantBase):
    pass


class PodcastParticipantUpdate(PodcastParticipantBase):
    video_url: Annotated[str | None, Field(max_length=500, default=None)]
    guests: list[str] | None = None


class PodcastParticipantResponse(PodcastParticipantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PodcastNewsBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=20)]
    # Подзаголовок
    subtitle: Annotated[str, Field(max_length=20)]
    # Сам текст новости (описание)
    description: Annotated[str, Field(max_length=1000)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=50)]


class PodcastNewsCreate(PodcastNewsBase):
    pass


class PodcastNewsUpdate(PodcastNewsBase):
    title: Annotated[str | None, Field(max_length=20, default=None)]
    subtitle: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=50, default=None)]


class PodcastNewsResponse(PodcastNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PodcastContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Описание
    description: Annotated[str, Field(max_length=500)]
    # Фотография ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None
    # Контактный адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]


class PodcastContactCreate(PodcastContactBase):
    pass


class PodcastContactUpdate(PodcastContactBase):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=500, default=None)]
    image_url: Annotated[str | None, Field(max_length=50, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]


class PodcastContactResponse(PodcastContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProjectNewsBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=200)]
    # Подзаголовок
    subtitle: Annotated[str, Field(max_length=200)]
    # Текст новости
    description: Annotated[str, Field(max_length=100)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=50)]


class ProjectNewsCreate(ProjectNewsBase):
    pass


class ProjectNewsUpdate(ProjectNewsBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    subtitle: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=50, default=None)]


class ProjectNewsResponse(ProjectNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProjectReportBase(BaseModel):
    # Наименование образовательной организации
    organization_name: Annotated[str, Field(max_length=200)]
    # Видео отчета
    video_url: Annotated[str, Field(max_length=500)]


class ProjectReportCreate(ProjectReportBase):
    pass


class ProjectReportUpdate(ProjectReportBase):
    organization_name: Annotated[str | None, Field(max_length=20, default=None)]
    video_url: Annotated[str | None, Field(max_length=500, default=None)]


class ProjectReportResponse(ProjectReportBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class CompetitionDocumentBase(BaseModel):
    # Название документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class CompetitionDocumentCreate(CompetitionDocumentBase):
    pass


class CompetitionDocumentUpdate(CompetitionDocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class CompetitionDocumentResponse(CompetitionDocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class CompetitionContactBase(BaseModel):
    # Название ответственной организации
    organization_name: Annotated[str, Field(max_length=200)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Контактный адрес эл. почты
    email: Annotated[str, Field(max_length=320)]


class CompetitionContactCreate(CompetitionContactBase):
    pass


class CompetitionContactUpdate(CompetitionContactBase):
    organization_name: Annotated[str | None, Field(max_length=20, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]


class CompetitionContactResponse(CompetitionContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class JournalNewsBase(BaseModel):
    # Заголовок новости
    title: Annotated[str, Field(max_length=200)]
    # Подзаголовок новости
    subtitle: Annotated[str, Field(max_length=200)]
    # Текст новости
    description: Annotated[str, Field(max_length=1000)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=50)]


class JournalNewsCreate(JournalNewsBase):
    pass


class JournalNewsUpdate(JournalNewsBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    subtitle: Annotated[str | None, Field(max_length=20, default=None)]
    description: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class JournalNewsResponse(JournalNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class JournalContactBase(BaseModel):
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Контактный адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Адрес
    address: Annotated[str, Field(max_length=500)]


class JournalContactCreate(JournalContactBase):
    pass


class JournalContactUpdate(JournalContactBase):
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    address: Annotated[str | None, Field(max_length=50, default=None)]


class JournalContactResponse(JournalContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
