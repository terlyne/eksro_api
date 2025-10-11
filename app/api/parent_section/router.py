import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.parent_section.repository import (
    ParentDocumentRepository,
    ParentContactRepository,
    ThematicMeetingParticipantRepository,
    ThematicMeetingEventRepository,
    ThematicMeetingContactRepository,
    EtiquetteInEducationDocumentRepository,
    EtiquetteInEducationEventRepository,
    EtiquetteInEducationContactRepository,
    ProfessionalLearningTrajectoryDocumentRepository,
    ProfessionalLearningTrajectoryParticipantRepository,
    ProfessionalLearningTrajectoryEventRepository,
    ProfessionalLearningTrajectoryContactRepository,
)
from api.parent_section.schemas import (
    ParentDocumentCreate,
    ParentDocumentResponse,
    ParentDocumentUpdate,
    ParentContactCreate,
    ParentContactResponse,
    ParentContactUpdate,
    ThematicMeetingParticipantCreate,
    ThematicMeetingParticipantResponse,
    ThematicMeetingParticipantUpdate,
    ThematicMeetingEventCreate,
    ThematicMeetingEventResponse,
    ThematicMeetingEventUpdate,
    ThematicMeetingContactCreate,
    ThematicMeetingContactResponse,
    ThematicMeetingContactUpdate,
    EtiquetteInEducationDocumentCreate,
    EtiquetteInEducationDocumentResponse,
    EtiquetteInEducationDocumentUpdate,
    EtiquetteInEducationEventCreate,
    EtiquetteInEducationEventResponse,
    EtiquetteInEducationEventUpdate,
    EtiquetteInEducationContactCreate,
    EtiquetteInEducationContactResponse,
    EtiquetteInEducationContactUpdate,
    ProfessionalLearningTrajectoryDocumentCreate,
    ProfessionalLearningTrajectoryDocumentResponse,
    ProfessionalLearningTrajectoryDocumentUpdate,
    ProfessionalLearningTrajectoryParticipantCreate,
    ProfessionalLearningTrajectoryParticipantResponse,
    ProfessionalLearningTrajectoryParticipantUpdate,
    ProfessionalLearningTrajectoryEventCreate,
    ProfessionalLearningTrajectoryEventResponse,
    ProfessionalLearningTrajectoryEventUpdate,
    ProfessionalLearningTrajectoryContactCreate,
    ProfessionalLearningTrajectoryContactResponse,
    ProfessionalLearningTrajectoryContactUpdate,
)


router = APIRouter()


# Parent Documents
@router.get("/parent-documents", response_model=list[ParentDocumentResponse])
async def get_parent_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get("/parent-documents/{item_id}", response_model=ParentDocumentResponse)
async def get_parent_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Родительский документ не найден",
        )
    return item


@router.post("/parent-documents", response_model=ParentDocumentResponse)
async def create_parent_document(
    title: Annotated[str, Form()],
    file: UploadFile,  # Файл документа
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем файл документа
    file_url = await file_service.save_file(
        upload_file=file,
        subdirectory=DOCUMENTS_FOLDER,
    )

    # Создаем запись о документе
    repo = ParentDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put("/parent-documents/{item_id}", response_model=ParentDocumentResponse)
async def update_parent_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Родительский документ не найден",
        )

    # Если загружен новый файл, удаляем старый и сохраняем новый
    file_url = None
    if file:
        # Удаляем старый файл
        await file_service.delete_file(current_item.file_url)
        # Сохраняем новый файл
        file_url = await file_service.save_file(
            upload_file=file,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о документе
    item = await repo.update(
        obj_id=item_id,
        title=title,
        file_url=file_url,
    )

    return item


@router.delete("/parent-documents/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parent_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Родительский документ не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Родительский документ не найден",
        )
    return {"message": "Родительский документ успешно удален"}


# Parent Contacts
@router.get("/parent-contacts", response_model=list[ParentContactResponse])
async def get_parent_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/parent-contacts/{item_id}", response_model=ParentContactResponse)
async def get_parent_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт родителя не найден",
        )
    return item


@router.post("/parent-contacts", response_model=ParentContactResponse)
async def create_parent_contact(
    full_name: Annotated[str, Form()],
    discipline: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        discipline=discipline,
        email=email,
        phone=phone,
    )
    return item


@router.put("/parent-contacts/{item_id}", response_model=ParentContactResponse)
async def update_parent_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    discipline: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        full_name=full_name,
        discipline=discipline,
        email=email,
        phone=phone,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт родителя не найден",
        )

    return item


@router.delete("/parent-contacts/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parent_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ParentContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт родителя не найден",
        )
    return {"message": "Контакт родителя успешно удален"}


# Thematic Meeting Participants
@router.get(
    "/thematic-meeting-participants",
    response_model=list[ThematicMeetingParticipantResponse],
)
async def get_thematic_meeting_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingParticipantRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/thematic-meeting-participants/{item_id}",
    response_model=ThematicMeetingParticipantResponse,
)
async def get_thematic_meeting_participant_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingParticipantRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник тематической встречи не найден",
        )
    return item


@router.post(
    "/thematic-meeting-participants", response_model=ThematicMeetingParticipantResponse
)
async def create_thematic_meeting_participant(
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = ThematicMeetingParticipantRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put(
    "/thematic-meeting-participants/{item_id}",
    response_model=ThematicMeetingParticipantResponse,
)
async def update_thematic_meeting_participant(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник тематической встречи не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию об участнике
    item = await repo.update(
        obj_id=item_id,
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )

    return item


@router.delete(
    "/thematic-meeting-participants/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_thematic_meeting_participant(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник тематической встречи не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись об участнике
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник тематической встречи не найден",
        )
    return {"message": "Участник тематической встречи успешно удален"}


# Thematic Meeting Events
@router.get(
    "/thematic-meeting-events", response_model=list[ThematicMeetingEventResponse]
)
async def get_thematic_meeting_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingEventRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/thematic-meeting-events/{item_id}", response_model=ThematicMeetingEventResponse
)
async def get_thematic_meeting_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingEventRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие тематической встречи не найдено",
        )
    return item


@router.post("/thematic-meeting-events", response_model=ThematicMeetingEventResponse)
async def create_thematic_meeting_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    event_date: Annotated[str, Form()],  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool, Form()] = True,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = ThematicMeetingEventRepository(session)
    item = await repo.create(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )
    return item


@router.put(
    "/thematic-meeting-events/{item_id}", response_model=ThematicMeetingEventResponse
)
async def update_thematic_meeting_event(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    event_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие тематической встречи не найдено",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о мероприятии
    item = await repo.update(
        obj_id=item_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )

    return item


@router.delete(
    "/thematic-meeting-events/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_thematic_meeting_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие тематической встречи не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие тематической встречи не найдено",
        )
    return {"message": "Мероприятие тематической встречи успешно удалено"}


# Thematic Meeting Contacts
@router.get(
    "/thematic-meeting-contacts", response_model=list[ThematicMeetingContactResponse]
)
async def get_thematic_meeting_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/thematic-meeting-contacts/{item_id}",
    response_model=ThematicMeetingContactResponse,
)
async def get_thematic_meeting_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт тематической встречи не найден",
        )
    return item


@router.post(
    "/thematic-meeting-contacts", response_model=ThematicMeetingContactResponse
)
async def create_thematic_meeting_contact(
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = ThematicMeetingContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        position=position,
        email=email,
        phone=phone,
        image_url=image_url,
    )
    return item


@router.put(
    "/thematic-meeting-contacts/{item_id}",
    response_model=ThematicMeetingContactResponse,
)
async def update_thematic_meeting_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт тематической встречи не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о контакте
    item = await repo.update(
        obj_id=item_id,
        full_name=full_name,
        position=position,
        email=email,
        phone=phone,
        image_url=image_url,
    )

    return item


@router.delete(
    "/thematic-meeting-contacts/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_thematic_meeting_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ThematicMeetingContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт тематической встречи не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о контакте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт тематической встречи не найден",
        )
    return {"message": "Контакт тематической встречи успешно удален"}


# Etiquette in Education Documents
@router.get(
    "/etiquette-in-education-documents",
    response_model=list[EtiquetteInEducationDocumentResponse],
)
async def get_etiquette_in_education_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/etiquette-in-education-documents/{item_id}",
    response_model=EtiquetteInEducationDocumentResponse,
)
async def get_etiquette_in_education_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ этикета в образовании не найден",
        )
    return item


@router.post(
    "/etiquette-in-education-documents",
    response_model=EtiquetteInEducationDocumentResponse,
)
async def create_etiquette_in_education_document(
    title: Annotated[str, Form()],
    file: UploadFile,  # Файл документа
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем файл документа
    file_url = await file_service.save_file(
        upload_file=file,
        subdirectory=DOCUMENTS_FOLDER,
    )

    repo = EtiquetteInEducationDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/etiquette-in-education-documents/{item_id}",
    response_model=EtiquetteInEducationDocumentResponse,
)
async def update_etiquette_in_education_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ этикета в образовании не найден",
        )

    # Если загружен новый файл, удаляем старый и сохраняем новый
    file_url = None
    if file:
        # Удаляем старый файл
        await file_service.delete_file(current_item.file_url)
        # Сохраняем новый файл
        file_url = await file_service.save_file(
            upload_file=file,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о документе
    item = await repo.update(
        obj_id=item_id,
        title=title,
        file_url=file_url,
    )

    return item


@router.delete(
    "/etiquette-in-education-documents/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_etiquette_in_education_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ этикета в образовании не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ этикета в образовании не найден",
        )
    return {"message": "Документ этикета в образовании успешно удален"}


# Etiquette in Education Events
@router.get(
    "/etiquette-in-education-events",
    response_model=list[EtiquetteInEducationEventResponse],
)
async def get_etiquette_in_education_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationEventRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/etiquette-in-education-events/{item_id}",
    response_model=EtiquetteInEducationEventResponse,
)
async def get_etiquette_in_education_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationEventRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие этикета в образовании не найдено",
        )
    return item


@router.post(
    "/etiquette-in-education-events", response_model=EtiquetteInEducationEventResponse
)
async def create_etiquette_in_education_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    event_date: Annotated[str, Form()],  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool, Form()] = True,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = EtiquetteInEducationEventRepository(session)
    item = await repo.create(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )
    return item


@router.put(
    "/etiquette-in-education-events/{item_id}",
    response_model=EtiquetteInEducationEventResponse,
)
async def update_etiquette_in_education_event(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    event_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие этикета в образовании не найдено",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о мероприятии
    item = await repo.update(
        obj_id=item_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )

    return item


@router.delete(
    "/etiquette-in-education-events/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_etiquette_in_education_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие этикета в образовании не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие этикета в образовании не найдено",
        )
    return {"message": "Мероприятие этикета в образовании успешно удалено"}


# Etiquette in Education Contacts
@router.get(
    "/etiquette-in-education-contacts",
    response_model=list[EtiquetteInEducationContactResponse],
)
async def get_etiquette_in_education_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/etiquette-in-education-contacts/{item_id}",
    response_model=EtiquetteInEducationContactResponse,
)
async def get_etiquette_in_education_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт этикета в образовании не найден",
        )
    return item


@router.post(
    "/etiquette-in-education-contacts",
    response_model=EtiquetteInEducationContactResponse,
)
async def create_etiquette_in_education_contact(
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = EtiquetteInEducationContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        position=position,
        email=email,
        phone=phone,
        image_url=image_url,
    )
    return item


@router.put(
    "/etiquette-in-education-contacts/{item_id}",
    response_model=EtiquetteInEducationContactResponse,
)
async def update_etiquette_in_education_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт этикета в образовании не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о контакте
    item = await repo.update(
        obj_id=item_id,
        full_name=full_name,
        position=position,
        email=email,
        phone=phone,
        image_url=image_url,
    )

    return item


@router.delete(
    "/etiquette-in-education-contacts/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_etiquette_in_education_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = EtiquetteInEducationContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт этикета в образовании не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о контакте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт этикета в образовании не найден",
        )
    return {"message": "Контакт этикета в образовании успешно удален"}


# Professional Learning Trajectory Documents
@router.get(
    "/professional-learning-trajectory-documents",
    response_model=list[ProfessionalLearningTrajectoryDocumentResponse],
)
async def get_professional_learning_trajectory_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/professional-learning-trajectory-documents/{item_id}",
    response_model=ProfessionalLearningTrajectoryDocumentResponse,
)
async def get_professional_learning_trajectory_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ профессиональной траектории обучения не найден",
        )
    return item


@router.post(
    "/professional-learning-trajectory-documents",
    response_model=ProfessionalLearningTrajectoryDocumentResponse,
)
async def create_professional_learning_trajectory_document(
    title: Annotated[str, Form()],
    file: UploadFile,  # Файл документа
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем файл документа
    file_url = await file_service.save_file(
        upload_file=file,
        subdirectory=DOCUMENTS_FOLDER,
    )

    repo = ProfessionalLearningTrajectoryDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/professional-learning-trajectory-documents/{item_id}",
    response_model=ProfessionalLearningTrajectoryDocumentResponse,
)
async def update_professional_learning_trajectory_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ профессиональной траектории обучения не найден",
        )

    # Если загружен новый файл, удаляем старый и сохраняем новый
    file_url = None
    if file:
        # Удаляем старый файл
        await file_service.delete_file(current_item.file_url)
        # Сохраняем новый файл
        file_url = await file_service.save_file(
            upload_file=file,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о документе
    item = await repo.update(
        obj_id=item_id,
        title=title,
        file_url=file_url,
    )

    return item


@router.delete(
    "/professional-learning-trajectory-documents/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ профессиональной траектории обучения не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ профессиональной траектории обучения не найден",
        )
    return {"message": "Документ профессиональной траектории обучения успешно удален"}


# Professional Learning Trajectory Participants
@router.get(
    "/professional-learning-trajectory-participants",
    response_model=list[ProfessionalLearningTrajectoryParticipantResponse],
)
async def get_professional_learning_trajectory_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryParticipantRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/professional-learning-trajectory-participants/{item_id}",
    response_model=ProfessionalLearningTrajectoryParticipantResponse,
)
async def get_professional_learning_trajectory_participant_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryParticipantRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник профессиональной траектории обучения не найден",
        )
    return item


@router.post(
    "/professional-learning-trajectory-participants",
    response_model=ProfessionalLearningTrajectoryParticipantResponse,
)
async def create_professional_learning_trajectory_participant(
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = ProfessionalLearningTrajectoryParticipantRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put(
    "/professional-learning-trajectory-participants/{item_id}",
    response_model=ProfessionalLearningTrajectoryParticipantResponse,
)
async def update_professional_learning_trajectory_participant(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник профессиональной траектории обучения не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию об участнике
    item = await repo.update(
        obj_id=item_id,
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )

    return item


@router.delete(
    "/professional-learning-trajectory-participants/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_participant(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник профессиональной траектории обучения не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись об участнике
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник профессиональной траектории обучения не найден",
        )
    return {"message": "Участник профессиональной траектории обучения успешно удален"}


# Professional Learning Trajectory Events
@router.get(
    "/professional-learning-trajectory-events",
    response_model=list[ProfessionalLearningTrajectoryEventResponse],
)
async def get_professional_learning_trajectory_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryEventRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/professional-learning-trajectory-events/{item_id}",
    response_model=ProfessionalLearningTrajectoryEventResponse,
)
async def get_professional_learning_trajectory_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryEventRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие профессиональной траектории обучения не найдено",
        )
    return item


@router.post(
    "/professional-learning-trajectory-events",
    response_model=ProfessionalLearningTrajectoryEventResponse,
)
async def create_professional_learning_trajectory_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    event_date: Annotated[str, Form()],  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool, Form()] = True,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    repo = ProfessionalLearningTrajectoryEventRepository(session)
    item = await repo.create(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )
    return item


@router.put(
    "/professional-learning-trajectory-events/{item_id}",
    response_model=ProfessionalLearningTrajectoryEventResponse,
)
async def update_professional_learning_trajectory_event(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    event_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие профессиональной траектории обучения не найдено",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_item.image_url:
            await file_service.delete_file(current_item.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о мероприятии
    item = await repo.update(
        obj_id=item_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )

    return item


@router.delete(
    "/professional-learning-trajectory-events/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие профессиональной траектории обучения не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие профессиональной траектории обучения не найдено",
        )
    return {
        "message": "Мероприятие профессиональной траектории обучения успешно удалено"
    }


# Professional Learning Trajectory Contacts
@router.get(
    "/professional-learning-trajectory-contacts",
    response_model=list[ProfessionalLearningTrajectoryContactResponse],
)
async def get_professional_learning_trajectory_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/professional-learning-trajectory-contacts/{item_id}",
    response_model=ProfessionalLearningTrajectoryContactResponse,
)
async def get_professional_learning_trajectory_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт профессиональной траектории обучения не найден",
        )
    return item


@router.post(
    "/professional-learning-trajectory-contacts",
    response_model=ProfessionalLearningTrajectoryContactResponse,
)
async def create_professional_learning_trajectory_contact(
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        position=position,
        email=email,
        phone=phone,
    )
    return item


@router.put(
    "/professional-learning-trajectory-contacts/{item_id}",
    response_model=ProfessionalLearningTrajectoryContactResponse,
)
async def update_professional_learning_trajectory_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        full_name=full_name,
        position=position,
        email=email,
        phone=phone,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт профессиональной траектории обучения не найден",
        )

    return item


@router.delete(
    "/professional-learning-trajectory-contacts/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProfessionalLearningTrajectoryContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт профессиональной траектории обучения не найден",
        )
    return {"message": "Контакт профессиональной траектории обучения успешно удален"}
