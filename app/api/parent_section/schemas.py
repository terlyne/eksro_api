from typing import Annotated
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ParentDocumentBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class ParentDocumentCreate(ParentDocumentBase):
    pass


class ParentDocumentUpdate(ParentDocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class ParentDocumentResponse(ParentDocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ParentContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Дисциплина ответственного лица
    discipline: Annotated[str, Field(max_length=200)]
    # Контактный Email
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]


class ParentContactCreate(ParentContactBase):
    pass


class ParentContactUpdate(ParentContactBase):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    discipline: Annotated[str | None, Field(max_length=200, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]


class ParentContactResponse(ParentContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ThematicMeetingParticipantBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=10)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=10)]
    # Фотография участника (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class ThematicMeetingParticipantCreate(ThematicMeetingParticipantBase):
    pass


class ThematicMeetingParticipantUpdate(ThematicMeetingParticipantBase):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class ThematicMeetingParticipantResponse(ThematicMeetingParticipantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ThematicMeetingEventBase(BaseModel):
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
    location: Annotated[str, Field(max_length=200)] | None = None


class ThematicMeetingEventCreate(ThematicMeetingEventBase):
    pass


class ThematicMeetingEventUpdate(ThematicMeetingEventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class ThematicMeetingEventResponse(ThematicMeetingEventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ThematicMeetingContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Должность
    position: Annotated[str, Field(max_length=20)]
    # Контактный Email
    email: Annotated[str, Field(max_length=320)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Фотография ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None


class ThematicMeetingContactCreate(ThematicMeetingContactBase):
    pass


class ThematicMeetingContactUpdate(ThematicMeetingContactBase):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    position: Annotated[str | None, Field(max_length=200, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class ThematicMeetingContactResponse(ThematicMeetingContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class EtiquetteInEducationDocumentBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class EtiquetteInEducationDocumentCreate(EtiquetteInEducationDocumentBase):
    pass


class EtiquetteInEducationDocumentUpdate(EtiquetteInEducationDocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class EtiquetteInEducationDocumentResponse(EtiquetteInEducationDocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class EtiquetteInEducationEventBase(BaseModel):
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
    location: Annotated[str, Field(max_length=200)] | None = None


class EtiquetteInEducationEventCreate(EtiquetteInEducationEventBase):
    pass


class EtiquetteInEducationEventUpdate(EtiquetteInEducationEventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class EtiquetteInEducationEventResponse(EtiquetteInEducationEventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class EtiquetteInEducationContactBase(BaseModel):
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


class EtiquetteInEducationContactCreate(EtiquetteInEducationContactBase):
    pass


class EtiquetteInEducationContactUpdate(EtiquetteInEducationContactBase):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    position: Annotated[str | None, Field(max_length=200, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class EtiquetteInEducationContactResponse(EtiquetteInEducationContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProfessionalLearningTrajectoryDocumentBase(BaseModel):
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class ProfessionalLearningTrajectoryDocumentCreate(
    ProfessionalLearningTrajectoryDocumentBase
):
    pass


class ProfessionalLearningTrajectoryDocumentUpdate(
    ProfessionalLearningTrajectoryDocumentBase
):
    title: Annotated[str | None, Field(max_length=20, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class ProfessionalLearningTrajectoryDocumentResponse(
    ProfessionalLearningTrajectoryDocumentBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProfessionalLearningTrajectoryParticipantBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=100)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=10)]
    # Фотография участника (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class ProfessionalLearningTrajectoryParticipantCreate(
    ProfessionalLearningTrajectoryParticipantBase
):
    pass


class ProfessionalLearningTrajectoryParticipantUpdate(
    ProfessionalLearningTrajectoryParticipantBase
):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class ProfessionalLearningTrajectoryParticipantResponse(
    ProfessionalLearningTrajectoryParticipantBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProfessionalLearningTrajectoryEventBase(BaseModel):
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
    location: Annotated[str, Field(max_length=200)] | None = None


class ProfessionalLearningTrajectoryEventCreate(
    ProfessionalLearningTrajectoryEventBase
):
    pass


class ProfessionalLearningTrajectoryEventUpdate(
    ProfessionalLearningTrajectoryEventBase
):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    event_date: datetime | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class ProfessionalLearningTrajectoryEventResponse(
    ProfessionalLearningTrajectoryEventBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProfessionalLearningTrajectoryContactBase(BaseModel):
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Должность
    position: Annotated[str, Field(max_length=200)]
    # Контактный Email (опционально)
    email: Annotated[str, Field(max_length=320)] | None = None
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]


class ProfessionalLearningTrajectoryContactCreate(
    ProfessionalLearningTrajectoryContactBase
):
    pass


class ProfessionalLearningTrajectoryContactUpdate(
    ProfessionalLearningTrajectoryContactBase
):
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    position: Annotated[str | None, Field(max_length=200, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]


class ProfessionalLearningTrajectoryContactResponse(
    ProfessionalLearningTrajectoryContactBase
):
    id: uuid.UUID

    class Config:
        from_attributes = True
