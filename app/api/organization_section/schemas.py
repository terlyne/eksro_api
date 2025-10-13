from typing import Annotated
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class OrganizationSupportDocumentBase(BaseModel):
    # Заголовок/название документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class OrganizationSupportDocumentCreate(OrganizationSupportDocumentBase):
    pass


class OrganizationSupportDocumentUpdate(OrganizationSupportDocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationSupportDocumentResponse(OrganizationSupportDocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationSupportEventBase(BaseModel):
    # Заголовок/название мероприятия
    title: Annotated[str, Field(max_length=200)]
    # Описание мероприятия
    description: Annotated[str, Field(max_length=100)]
    # Изображение мероприятия
    image_url: Annotated[str, Field(max_length=500)]
    # Активно ли мероприятие
    is_active: bool = True
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: datetime
    # Локация
    location: Annotated[str, Field(max_length=200)] | None = None


class OrganizationSupportEventCreate(OrganizationSupportEventBase):
    pass


class OrganizationSupportEventUpdate(OrganizationSupportEventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class OrganizationSupportEventResponse(OrganizationSupportEventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationSupportApplicationBase(BaseModel):
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


class OrganizationSupportApplicationCreate(OrganizationSupportApplicationBase):
    pass


class OrganizationSupportApplicationUpdate(OrganizationSupportApplicationBase):
    application_type: Annotated[str | None, Field(max_length=50, default=None)]
    full_name: Annotated[str | None, Field(max_length=200, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    text: Annotated[str | None, Field(max_length=100, default=None)]


class OrganizationSupportApplicationResponse(OrganizationSupportApplicationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationLeaderBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=10)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=100)]
    # Фотография члена Управляющего совета (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class OrganizationLeaderCreate(OrganizationLeaderBase):
    pass


class OrganizationLeaderUpdate(OrganizationLeaderBase):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationLeaderResponse(OrganizationLeaderBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationNewsBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=20)]
    # Подзаголовок
    subtitle: Annotated[str, Field(max_length=200)]
    # Сам текст новости (описание)
    description: Annotated[str, Field(max_length=1000)]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=500)]


class OrganizationNewsCreate(OrganizationNewsBase):
    pass


class OrganizationNewsUpdate(OrganizationNewsBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    subtitle: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationNewsResponse(OrganizationNewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationQuestionBase(BaseModel):
    # Имя
    name: Annotated[str, Field(max_length=100)]
    # Номер телефона (опционально)
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Текст сообщения/вопроса
    message: Annotated[str, Field(max_length=1000)]
    # Ответ на вопрос
    response: Annotated[str, Field(max_length=1000)] | None = None


class OrganizationQuestionCreate(OrganizationQuestionBase):
    pass


class OrganizationQuestionUpdate(OrganizationQuestionBase):
    name: Annotated[str | None, Field(max_length=10, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    message: Annotated[str | None, Field(max_length=100, default=None)]
    response: Annotated[str | None, Field(max_length=1000, default=None)]


class OrganizationQuestionResponse(OrganizationQuestionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationContactBase(BaseModel):
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Контактная эл. почта
    email: Annotated[str, Field(max_length=320)]
    # Ссылка на ТГ-канал
    tg_channel: Annotated[str, Field(max_length=500)] | None = None
    # Ссылка на сообщество ВК
    vk_group: Annotated[str, Field(max_length=500)] | None = None


class OrganizationContactCreate(OrganizationContactBase):
    pass


class OrganizationContactUpdate(OrganizationContactBase):
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    tg_channel: Annotated[str | None, Field(max_length=500, default=None)]
    vk_group: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationContactResponse(OrganizationContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationEducationalProgramDocumentBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class OrganizationEducationalProgramDocumentCreate(
    OrganizationEducationalProgramDocumentBase
):
    pass


class OrganizationEducationalProgramDocumentUpdate(
    OrganizationEducationalProgramDocumentBase
):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationEducationalProgramDocumentResponse(
    OrganizationEducationalProgramDocumentBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationEducationalProgramContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Дисциплина ответственного лица
    discipline: Annotated[str, Field(max_length=200)]
    # Контактный Email
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]


class OrganizationEducationalProgramContactCreate(
    OrganizationEducationalProgramContactBase
):
    pass


class OrganizationEducationalProgramContactUpdate(
    OrganizationEducationalProgramContactBase
):
    full_name: Annotated[str | None, Field(max_length=200, default=None)]
    discipline: Annotated[str | None, Field(max_length=20, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]


class OrganizationEducationalProgramContactResponse(
    OrganizationEducationalProgramContactBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationThematicMeetingParticipantBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=10)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=10)]
    # Фотография участника (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class OrganizationThematicMeetingParticipantCreate(
    OrganizationThematicMeetingParticipantBase
):
    pass


class OrganizationThematicMeetingParticipantUpdate(
    OrganizationThematicMeetingParticipantBase
):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationThematicMeetingParticipantResponse(
    OrganizationThematicMeetingParticipantBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationThematicMeetingEventBase(BaseModel):
    # Заголовок/название мероприятия
    title: Annotated[str, Field(max_length=200)]
    # Описание мероприятия
    description: Annotated[str, Field(max_length=100)]
    # Изображение мероприятия
    image_url: Annotated[str, Field(max_length=500)]
    # Активно ли мероприятие
    is_active: bool = True
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: datetime
    # Локация
    location: Annotated[str, Field(max_length=20)] | None = None


class OrganizationThematicMeetingEventCreate(OrganizationThematicMeetingEventBase):
    pass


class OrganizationThematicMeetingEventUpdate(OrganizationThematicMeetingEventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class OrganizationThematicMeetingEventResponse(OrganizationThematicMeetingEventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationThematicMeetingContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Должность
    position: Annotated[str, Field(max_length=200)]
    # Контактный Email
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Фотография ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None


class OrganizationThematicMeetingContactCreate(OrganizationThematicMeetingContactBase):
    pass


class OrganizationThematicMeetingContactUpdate(OrganizationThematicMeetingContactBase):
    full_name: Annotated[str | None, Field(max_length=200, default=None)]
    position: Annotated[str | None, Field(max_length=200, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationThematicMeetingContactResponse(
    OrganizationThematicMeetingContactBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationEtiquetteInEducationDocumentBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class OrganizationEtiquetteInEducationDocumentCreate(
    OrganizationEtiquetteInEducationDocumentBase
):
    pass


class OrganizationEtiquetteInEducationDocumentUpdate(
    OrganizationEtiquetteInEducationDocumentBase
):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationEtiquetteInEducationDocumentResponse(
    OrganizationEtiquetteInEducationDocumentBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationEtiquetteInEducationEventBase(BaseModel):
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
    location: Annotated[str, Field(max_length=20)] | None = None


class OrganizationEtiquetteInEducationEventCreate(
    OrganizationEtiquetteInEducationEventBase
):
    pass


class OrganizationEtiquetteInEducationEventUpdate(
    OrganizationEtiquetteInEducationEventBase
):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class OrganizationEtiquetteInEducationEventResponse(
    OrganizationEtiquetteInEducationEventBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationEtiquetteInEducationContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Должность
    position: Annotated[str, Field(max_length=200)]
    # Контактный Email
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Фотография ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None


class OrganizationEtiquetteInEducationContactCreate(
    OrganizationEtiquetteInEducationContactBase
):
    pass


class OrganizationEtiquetteInEducationContactUpdate(
    OrganizationEtiquetteInEducationContactBase
):
    full_name: Annotated[str | None, Field(max_length=200, default=None)]
    position: Annotated[str | None, Field(max_length=20, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationEtiquetteInEducationContactResponse(
    OrganizationEtiquetteInEducationContactBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationProfessionalLearningTrajectoryDocumentBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class OrganizationProfessionalLearningTrajectoryDocumentCreate(
    OrganizationProfessionalLearningTrajectoryDocumentBase
):
    pass


class OrganizationProfessionalLearningTrajectoryDocumentUpdate(
    OrganizationProfessionalLearningTrajectoryDocumentBase
):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationProfessionalLearningTrajectoryDocumentResponse(
    OrganizationProfessionalLearningTrajectoryDocumentBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationProfessionalLearningTrajectoryParticipantBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=10)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=100)]
    # Фотография участника (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class OrganizationProfessionalLearningTrajectoryParticipantCreate(
    OrganizationProfessionalLearningTrajectoryParticipantBase
):
    pass


class OrganizationProfessionalLearningTrajectoryParticipantUpdate(
    OrganizationProfessionalLearningTrajectoryParticipantBase
):
    first_name: Annotated[str | None, Field(max_length=100, default=None)]
    last_name: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class OrganizationProfessionalLearningTrajectoryParticipantResponse(
    OrganizationProfessionalLearningTrajectoryParticipantBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationProfessionalLearningTrajectoryEventBase(BaseModel):
    # Заголовок/название мероприятия
    title: Annotated[str, Field(max_length=200)]
    # Описание мероприятия
    description: Annotated[str, Field(max_length=100)]
    # Изображение мероприятия
    image_url: Annotated[str, Field(max_length=500)]
    # Активно ли мероприятие
    is_active: bool = True
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: datetime
    # Локация
    location: Annotated[str, Field(max_length=20)] | None = None


class OrganizationProfessionalLearningTrajectoryEventCreate(
    OrganizationProfessionalLearningTrajectoryEventBase
):
    pass


class OrganizationProfessionalLearningTrajectoryEventUpdate(
    OrganizationProfessionalLearningTrajectoryEventBase
):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class OrganizationProfessionalLearningTrajectoryEventResponse(
    OrganizationProfessionalLearningTrajectoryEventBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrganizationProfessionalLearningTrajectoryContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Должность
    position: Annotated[str, Field(max_length=200)]
    # Контактный Email (опционально)
    email: Annotated[str, Field(max_length=320)] | None = None
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]


class OrganizationProfessionalLearningTrajectoryContactCreate(
    OrganizationProfessionalLearningTrajectoryContactBase
):
    pass


class OrganizationProfessionalLearningTrajectoryContactUpdate(
    OrganizationProfessionalLearningTrajectoryContactBase
):
    full_name: Annotated[str | None, Field(max_length=200, default=None)]
    position: Annotated[str | None, Field(max_length=200, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]


class OrganizationProfessionalLearningTrajectoryContactResponse(
    OrganizationProfessionalLearningTrajectoryContactBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True
