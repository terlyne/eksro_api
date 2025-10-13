import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user, verify_active_param_access
from api.organization_section.repository import (
    OrganizationSupportDocumentRepository,
    OrganizationSupportEventRepository,
    OrganizationSupportApplicationRepository,
    OrganizationLeaderRepository,
    OrganizationNewsRepository,
    OrganizationQuestionRepository,
    OrganizationContactRepository,
    OrganizationEducationalProgramDocumentRepository,
    OrganizationEducationalProgramContactRepository,
    OrganizationThematicMeetingParticipantRepository,
    OrganizationThematicMeetingEventRepository,
    OrganizationThematicMeetingContactRepository,
    OrganizationEtiquetteInEducationDocumentRepository,
    OrganizationEtiquetteInEducationEventRepository,
    OrganizationEtiquetteInEducationContactRepository,
    OrganizationProfessionalLearningTrajectoryDocumentRepository,
    OrganizationProfessionalLearningTrajectoryParticipantRepository,
    OrganizationProfessionalLearningTrajectoryEventRepository,
    OrganizationProfessionalLearningTrajectoryContactRepository,
)
from api.organization_section.schemas import (
    OrganizationSupportDocumentCreate,
    OrganizationSupportDocumentResponse,
    OrganizationSupportDocumentUpdate,
    OrganizationSupportEventCreate,
    OrganizationSupportEventResponse,
    OrganizationSupportEventUpdate,
    OrganizationSupportApplicationCreate,
    OrganizationSupportApplicationResponse,
    OrganizationSupportApplicationUpdate,
    OrganizationLeaderCreate,
    OrganizationLeaderResponse,
    OrganizationLeaderUpdate,
    OrganizationNewsCreate,
    OrganizationNewsResponse,
    OrganizationNewsUpdate,
    OrganizationQuestionCreate,
    OrganizationQuestionResponse,
    OrganizationQuestionUpdate,
    OrganizationContactCreate,
    OrganizationContactResponse,
    OrganizationContactUpdate,
    OrganizationEducationalProgramDocumentResponse,
    OrganizationEducationalProgramDocumentCreate,
    OrganizationEducationalProgramDocumentUpdate,
    OrganizationEducationalProgramContactResponse,
    OrganizationEducationalProgramContactCreate,
    OrganizationEducationalProgramContactUpdate,
    OrganizationThematicMeetingParticipantResponse,
    OrganizationThematicMeetingParticipantCreate,
    OrganizationThematicMeetingParticipantUpdate,
    OrganizationThematicMeetingEventResponse,
    OrganizationThematicMeetingEventCreate,
    OrganizationThematicMeetingEventUpdate,
    OrganizationThematicMeetingContactResponse,
    OrganizationThematicMeetingContactCreate,
    OrganizationThematicMeetingContactUpdate,
    OrganizationEtiquetteInEducationDocumentResponse,
    OrganizationEtiquetteInEducationDocumentCreate,
    OrganizationEtiquetteInEducationDocumentUpdate,
    OrganizationEtiquetteInEducationEventResponse,
    OrganizationEtiquetteInEducationEventCreate,
    OrganizationEtiquetteInEducationEventUpdate,
    OrganizationEtiquetteInEducationContactResponse,
    OrganizationEtiquetteInEducationContactCreate,
    OrganizationEtiquetteInEducationContactUpdate,
    OrganizationProfessionalLearningTrajectoryDocumentResponse,
    OrganizationProfessionalLearningTrajectoryDocumentCreate,
    OrganizationProfessionalLearningTrajectoryDocumentUpdate,
    OrganizationProfessionalLearningTrajectoryParticipantResponse,
    OrganizationProfessionalLearningTrajectoryParticipantCreate,
    OrganizationProfessionalLearningTrajectoryParticipantUpdate,
    OrganizationProfessionalLearningTrajectoryEventResponse,
    OrganizationProfessionalLearningTrajectoryEventCreate,
    OrganizationProfessionalLearningTrajectoryEventUpdate,
    OrganizationProfessionalLearningTrajectoryContactResponse,
    OrganizationProfessionalLearningTrajectoryContactCreate,
    OrganizationProfessionalLearningTrajectoryContactUpdate,
)


router = APIRouter()


# Organization Support Documents
@router.get(
    "/support/documents/", response_model=list[OrganizationSupportDocumentResponse]
)
async def get_support_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationSupportDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/documents/{item_id}/", response_model=OrganizationSupportDocumentResponse
)
async def get_support_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationSupportDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки организации не найден",
        )
    return item


@router.post("/support/documents/", response_model=OrganizationSupportDocumentResponse)
async def create_support_document(
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
    repo = OrganizationSupportDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/support/documents/{item_id}/", response_model=OrganizationSupportDocumentResponse
)
async def update_support_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки организации не найден",
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


@router.delete("/support/documents/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_support_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки организации не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки организации не найден",
        )
    return {"message": "Документ поддержки организации успешно удален"}


# Organization Support Events
@router.get("/support/events/", response_model=list[OrganizationSupportEventResponse])
async def get_support_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationSupportEventRepository(session)
    items = await repo.find_all(is_active=is_active)
    return items


@router.get(
    "/support/events/{item_id}/", response_model=OrganizationSupportEventResponse
)
async def get_support_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationSupportEventRepository(session)
    item = await repo.find_one(id=item_id, is_active=is_active)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки организации не найдено",
        )
    return item


@router.post("/support/events/", response_model=OrganizationSupportEventResponse)
async def create_support_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    event_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY hh:mm
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

    repo = OrganizationSupportEventRepository(session)
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
    "/support/events/{item_id}/", response_model=OrganizationSupportEventResponse
)
async def update_support_event(
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
    repo = OrganizationSupportEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки организации не найдено",
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


@router.delete("/support/events/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_support_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки организации не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки организации не найдено",
        )
    return {"message": "Мероприятие поддержки организации успешно удалено"}


# Organization Support Applications
@router.get(
    "/support/applications/",
    response_model=list[OrganizationSupportApplicationResponse],
)
async def get_support_applications(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportApplicationRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/applications/{item_id}/",
    response_model=OrganizationSupportApplicationResponse,
)
async def get_support_application_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportApplicationRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на поддержку организации не найдена",
        )
    return item


@router.post(
    "/support/applications/", response_model=OrganizationSupportApplicationResponse
)
async def create_support_application(
    application_type: Annotated[
        str, Form()
    ],  # "Консультация", "Вступление в УС", "Другое"
    full_name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    text: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationSupportApplicationRepository(session)
    item = await repo.create(
        application_type=application_type,
        full_name=full_name,
        phone=phone,
        email=email,
        text=text,
    )
    return item


@router.put(
    "/support/applications/{item_id}/",
    response_model=OrganizationSupportApplicationResponse,
)
async def update_support_application(
    item_id: uuid.UUID,
    application_type: Annotated[
        str | None, Form()
    ] = None,  # "Консультация", "Вступление в УС", "Другое"
    full_name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    text: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportApplicationRepository(session)
    item = await repo.update(
        obj_id=item_id,
        application_type=application_type,
        full_name=full_name,
        phone=phone,
        email=email,
        text=text,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на поддержку организации не найдена",
        )

    return item


@router.delete(
    "/support/applications/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_support_application(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationSupportApplicationRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на поддержку организации не найдена",
        )
    return {"message": "Заявка на поддержку организации успешно удалена"}


# Organization Support Contacts
@router.get("/support/contacts/", response_model=list[OrganizationContactResponse])
async def get_support_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/support/contacts/{item_id}/", response_model=OrganizationContactResponse)
async def get_support_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт организации не найден",
        )
    return item


@router.post("/support/contacts/", response_model=OrganizationContactResponse)
async def create_support_contact(
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    tg_channel: Annotated[str | None, Form()] = None,
    vk_group: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationContactRepository(session)
    item = await repo.create(
        phone=phone,
        email=email,
        tg_channel=tg_channel,
        vk_group=vk_group,
    )
    return item


@router.put("/support/contacts/{item_id}/", response_model=OrganizationContactResponse)
async def update_support_contact(
    item_id: uuid.UUID,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    tg_channel: Annotated[str | None, Form()] = None,
    vk_group: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        phone=phone,
        email=email,
        tg_channel=tg_channel,
        vk_group=vk_group,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт организации не найден",
        )

    return item


@router.delete("/support/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_support_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт организации не найден",
        )
    return {"message": "Контакт организации успешно удален"}


# Organization Support Leaders
@router.get("/support/leaders/", response_model=list[OrganizationLeaderResponse])
async def get_support_leaders(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationLeaderRepository(session)
    items = await repo.get_all()
    return items


@router.get("/support/leaders/{item_id}/", response_model=OrganizationLeaderResponse)
async def get_support_leader_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationLeaderRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель организации не найден",
        )
    return item


@router.post("/support/leaders/", response_model=OrganizationLeaderResponse)
async def create_support_leader(
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

    repo = OrganizationLeaderRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put("/support/leaders/{item_id}/", response_model=OrganizationLeaderResponse)
async def update_support_leader(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationLeaderRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель организации не найден",
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

    # Обновляем информацию о руководителе
    item = await repo.update(
        obj_id=item_id,
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )

    return item


@router.delete("/support/leaders/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_support_leader(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationLeaderRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель организации не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о руководителе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель организации не найден",
        )
    return {"message": "Руководитель организации успешно удален"}


# Organization Support News
@router.get("/support/news/", response_model=list[OrganizationNewsResponse])
async def get_news(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/support/news/{item_id}/", response_model=OrganizationNewsResponse)
async def get_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость организации не найдена",
        )
    return item


@router.post("/support/news/", response_model=OrganizationNewsResponse)
async def create_news(
    title: Annotated[str, Form()],
    subtitle: Annotated[str, Form()],
    description: Annotated[str, Form()],
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

    repo = OrganizationNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put("/support/news/{item_id}/", response_model=OrganizationNewsResponse)
async def update_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость организации не найдена",
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

    # Обновляем информацию о новости
    item = await repo.update(
        obj_id=item_id,
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )

    return item


@router.delete("/support/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость организации не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость организации не найдена",
        )
    return {"message": "Новость организации успешно удалена"}


# Organization Questions
@router.get("/support/questions/", response_model=list[OrganizationQuestionResponse])
async def get_questions(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationQuestionRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/questions/{item_id}/", response_model=OrganizationQuestionResponse
)
async def get_question_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationQuestionRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос организации не найден",
        )
    return item


@router.post("/support/questions/", response_model=OrganizationQuestionResponse)
async def create_question(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    message: Annotated[str, Form()],
    phone: Annotated[str | None, Form()] = None,
    response: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationQuestionRepository(session)
    item = await repo.create(
        name=name,
        email=email,
        message=message,
        phone=phone,
        response=response,
        is_answered=bool(
            response
        ),  # Автоматически устанавливаем флаг ответа, если есть ответ
    )
    return item


@router.put(
    "/support/questions/{item_id}/", response_model=OrganizationQuestionResponse
)
async def update_question(
    item_id: uuid.UUID,
    name: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    message: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    response: Annotated[str | None, Form()] = None,
    is_answered: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationQuestionRepository(session)

    # Если есть ответ, автоматически устанавливаем флаг ответа
    if response is not None:
        is_answered = True

    item = await repo.update(
        obj_id=item_id,
        name=name,
        email=email,
        message=message,
        phone=phone,
        response=response,
        is_answered=is_answered,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос организации не найден",
        )

    return item


@router.delete("/support/questions/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationQuestionRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос организации не найден",
        )
    return {"message": "Вопрос организации успешно удален"}


# Organization Educational Program Documents
@router.get(
    "/support/educational-programs/documents/",
    response_model=list[OrganizationEducationalProgramDocumentResponse],
)
async def get_educational_program_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEducationalProgramDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/educational-programs/documents/{item_id}/",
    response_model=OrganizationEducationalProgramDocumentResponse,
)
async def get_educational_program_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEducationalProgramDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ образовательной программы не найден",
        )
    return item


@router.post(
    "/support/educational-programs/documents/",
    response_model=OrganizationEducationalProgramDocumentResponse,
)
async def create_educational_program_document(
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
    repo = OrganizationEducationalProgramDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/support/educational-programs/documents/{item_id}/",
    response_model=OrganizationEducationalProgramDocumentResponse,
)
async def update_educational_program_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEducationalProgramDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ образовательной программы не найден",
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
    "/support/educational-programs/documents/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_educational_program_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEducationalProgramDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ образовательной программы не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ образовательной программы не найден",
        )
    return {"message": "Документ образовательной программы успешно удален"}


# Organization Educational Program Contacts
@router.get(
    "/support/educational-programs/contacts/",
    response_model=list[OrganizationEducationalProgramContactResponse],
)
async def get_educational_program_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEducationalProgramContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/educational-programs/contacts/{item_id}/",
    response_model=OrganizationEducationalProgramContactResponse,
)
async def get_educational_program_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEducationalProgramContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт образовательной программы не найден",
        )
    return item


@router.post(
    "/support/educational-programs/contacts/",
    response_model=OrganizationEducationalProgramContactResponse,
)
async def create_educational_program_contact(
    full_name: Annotated[str, Form()],
    discipline: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEducationalProgramContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        discipline=discipline,
        phone=phone,
        email=email,
    )
    return item


@router.put(
    "/support/educational-programs/contacts/{item_id}/",
    response_model=OrganizationEducationalProgramContactResponse,
)
async def update_educational_program_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    discipline: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEducationalProgramContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        full_name=full_name,
        discipline=discipline,
        phone=phone,
        email=email,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт образовательной программы не найден",
        )

    return item


@router.delete(
    "/support/educational-programs/contacts/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_educational_program_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEducationalProgramContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт образовательной программы не найден",
        )
    return {"message": "Контакт образовательной программы успешно удален"}


# Organization Thematic Meeting Participants
@router.get(
    "/support/thematic-meetings/participants/",
    response_model=list[OrganizationThematicMeetingParticipantResponse],
)
async def get_thematic_meeting_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationThematicMeetingParticipantRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/thematic-meetings/participants/{item_id}/",
    response_model=OrganizationThematicMeetingParticipantResponse,
)
async def get_thematic_meeting_participant_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationThematicMeetingParticipantRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник тематической встречи не найден",
        )
    return item


@router.post(
    "/support/thematic-meetings/participants/",
    response_model=OrganizationThematicMeetingParticipantResponse,
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

    repo = OrganizationThematicMeetingParticipantRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put(
    "/support/thematic-meetings/participants/{item_id}/",
    response_model=OrganizationThematicMeetingParticipantResponse,
)
async def update_thematic_meeting_participant(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationThematicMeetingParticipantRepository(session)
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
    "/support/thematic-meetings/participants/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_thematic_meeting_participant(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationThematicMeetingParticipantRepository(session)
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


# Organization Thematic Meeting Events
@router.get(
    "/support/thematic-meetings/events/",
    response_model=list[OrganizationThematicMeetingEventResponse],
)
async def get_thematic_meeting_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationThematicMeetingEventRepository(session)
    items = await repo.find_all(is_active=is_active)
    return items


@router.get(
    "/support/thematic-meetings/events/{item_id}/",
    response_model=OrganizationThematicMeetingEventResponse,
)
async def get_thematic_meeting_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationThematicMeetingEventRepository(session)
    item = await repo.find_one(id=item_id, is_active=is_active)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие тематической встречи не найдено",
        )
    return item


@router.post(
    "/support/thematic-meetings/events/",
    response_model=OrganizationThematicMeetingEventResponse,
)
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

    repo = OrganizationThematicMeetingEventRepository(session)
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
    "/support/thematic-meetings/events/{item_id}/",
    response_model=OrganizationThematicMeetingEventResponse,
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
    repo = OrganizationThematicMeetingEventRepository(session)
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
    "/support/thematic-meetings/events/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_thematic_meeting_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationThematicMeetingEventRepository(session)
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


# Organization Thematic Meeting Contacts
@router.get(
    "/support/thematic-meetings/contacts/",
    response_model=list[OrganizationThematicMeetingContactResponse],
)
async def get_thematic_meeting_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationThematicMeetingContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/thematic-meetings/contacts/{item_id}/",
    response_model=OrganizationThematicMeetingContactResponse,
)
async def get_thematic_meeting_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationThematicMeetingContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт тематической встречи не найден",
        )
    return item


@router.post(
    "/support/thematic-meetings/contacts/",
    response_model=OrganizationThematicMeetingContactResponse,
)
async def create_thematic_meeting_contact(
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
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

    repo = OrganizationThematicMeetingContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
        image_url=image_url,
    )
    return item


@router.put(
    "/support/thematic-meetings/contacts/{item_id}/",
    response_model=OrganizationThematicMeetingContactResponse,
)
async def update_thematic_meeting_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationThematicMeetingContactRepository(session)
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
        phone=phone,
        email=email,
        image_url=image_url,
    )

    return item


@router.delete(
    "/support/thematic-meetings/contacts/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_thematic_meeting_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationThematicMeetingContactRepository(session)
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


# Organization Etiquette in Education Documents
@router.get(
    "/support/etiquette-in-education/documents/",
    response_model=list[OrganizationEtiquetteInEducationDocumentResponse],
)
async def get_etiquette_in_education_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEtiquetteInEducationDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/etiquette-in-education/documents/{item_id}/",
    response_model=OrganizationEtiquetteInEducationDocumentResponse,
)
async def get_etiquette_in_education_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEtiquetteInEducationDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Этикет в образовании' не найден",
        )
    return item


@router.post(
    "/support/etiquette-in-education/documents/",
    response_model=OrganizationEtiquetteInEducationDocumentResponse,
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

    repo = OrganizationEtiquetteInEducationDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/support/etiquette-in-education/documents/{item_id}/",
    response_model=OrganizationEtiquetteInEducationDocumentResponse,
)
async def update_etiquette_in_education_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEtiquetteInEducationDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Этикет в образовании' не найден",
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
    "/support/etiquette-in-education/documents/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_etiquette_in_education_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEtiquetteInEducationDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Этикет в образовании' не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Этикет в образовании' не найден",
        )
    return {"message": "Документ проекта 'Этикет в образовании' успешно удален"}


# Organization Etiquette in Education Events
@router.get(
    "/support/etiquette-in-education/events/",
    response_model=list[OrganizationEtiquetteInEducationEventResponse],
)
async def get_etiquette_in_education_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationEtiquetteInEducationEventRepository(session)
    items = await repo.find_all(is_active=is_active)
    return items


@router.get(
    "/support/etiquette-in-education/events/{item_id}/",
    response_model=OrganizationEtiquetteInEducationEventResponse,
)
async def get_etiquette_in_education_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationEtiquetteInEducationEventRepository(session)
    item = await repo.find_one(id=item_id, is_active=is_active)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Этикет в образовании' не найдено",
        )
    return item


@router.post(
    "/support/etiquette-in-education/events/",
    response_model=OrganizationEtiquetteInEducationEventResponse,
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

    repo = OrganizationEtiquetteInEducationEventRepository(session)
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
    "/support/etiquette-in-education/events/{item_id}/",
    response_model=OrganizationEtiquetteInEducationEventResponse,
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
    repo = OrganizationEtiquetteInEducationEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Этикет в образовании' не найдено",
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
    "/support/etiquette-in-education/events/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_etiquette_in_education_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEtiquetteInEducationEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Этикет в образовании' не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Этикет в образовании' не найдено",
        )
    return {"message": "Мероприятие проекта 'Этикет в образовании' успешно удалено"}


# Organization Etiquette in Education Contacts
@router.get(
    "/support/etiquette-in-education/contacts/",
    response_model=list[OrganizationEtiquetteInEducationContactResponse],
)
async def get_etiquette_in_education_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEtiquetteInEducationContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/etiquette-in-education/contacts/{item_id}/",
    response_model=OrganizationEtiquetteInEducationContactResponse,
)
async def get_etiquette_in_education_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationEtiquetteInEducationContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Этикет в образовании' не найден",
        )
    return item


@router.post(
    "/support/etiquette-in-education/contacts/",
    response_model=OrganizationEtiquetteInEducationContactResponse,
)
async def create_etiquette_in_education_contact(
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
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

    repo = OrganizationEtiquetteInEducationContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
        image_url=image_url,
    )
    return item


@router.put(
    "/support/etiquette-in-education/contacts/{item_id}/",
    response_model=OrganizationEtiquetteInEducationContactResponse,
)
async def update_etiquette_in_education_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEtiquetteInEducationContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Этикет в образовании' не найден",
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
        phone=phone,
        email=email,
        image_url=image_url,
    )

    return item


@router.delete(
    "/support/etiquette-in-education/contacts/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_etiquette_in_education_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationEtiquetteInEducationContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Этикет в образовании' не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о контакте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Этикет в образовании' не найден",
        )
    return {"message": "Контакт проекта 'Этикет в образовании' успешно удален"}


# Organization Professional Learning Trajectory Documents
@router.get(
    "/support/professional-learning-trajectory/documents/",
    response_model=list[OrganizationProfessionalLearningTrajectoryDocumentResponse],
)
async def get_professional_learning_trajectory_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationProfessionalLearningTrajectoryDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/professional-learning-trajectory/documents/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryDocumentResponse,
)
async def get_professional_learning_trajectory_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationProfessionalLearningTrajectoryDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Профессиональная траектория обучения ребенка' не найден",
        )
    return item


@router.post(
    "/support/professional-learning-trajectory/documents/",
    response_model=OrganizationProfessionalLearningTrajectoryDocumentResponse,
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

    repo = OrganizationProfessionalLearningTrajectoryDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/support/professional-learning-trajectory/documents/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryDocumentResponse,
)
async def update_professional_learning_trajectory_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Профессиональная траектория обучения ребенка' не найден",
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
    "/support/professional-learning-trajectory/documents/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Профессиональная траектория обучения ребенка' не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ проекта 'Профессиональная траектория обучения ребенка' не найден",
        )
    return {
        "message": "Документ проекта 'Профессиональная траектория обучения ребенка' успешно удален"
    }


# Organization Professional Learning Trajectory Participants
@router.get(
    "/support/professional-learning-trajectory/participants/",
    response_model=list[OrganizationProfessionalLearningTrajectoryParticipantResponse],
)
async def get_professional_learning_trajectory_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationProfessionalLearningTrajectoryParticipantRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/professional-learning-trajectory/participants/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryParticipantResponse,
)
async def get_professional_learning_trajectory_participant_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationProfessionalLearningTrajectoryParticipantRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник проекта 'Профессиональная траектория обучения ребенка' не найден",
        )
    return item


@router.post(
    "/support/professional-learning-trajectory/participants/",
    response_model=OrganizationProfessionalLearningTrajectoryParticipantResponse,
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

    repo = OrganizationProfessionalLearningTrajectoryParticipantRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put(
    "/support/professional-learning-trajectory/participants/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryParticipantResponse,
)
async def update_professional_learning_trajectory_participant(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник проекта 'Профессиональная траектория обучения ребенка' не найден",
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
    "/support/professional-learning-trajectory/participants/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_participant(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник проекта 'Профессиональная траектория обучения ребенка' не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись об участнике
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник проекта 'Профессиональная траектория обучения ребенка' не найден",
        )
    return {
        "message": "Участник проекта 'Профессиональная траектория обучения ребенка' успешно удален"
    }


# Organization Professional Learning Trajectory Events
@router.get(
    "/support/professional-learning-trajectory/events/",
    response_model=list[OrganizationProfessionalLearningTrajectoryEventResponse],
)
async def get_professional_learning_trajectory_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationProfessionalLearningTrajectoryEventRepository(session)
    items = await repo.find_all(is_active=is_active)
    return items


@router.get(
    "/support/professional-learning-trajectory/events/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryEventResponse,
)
async def get_professional_learning_trajectory_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = OrganizationProfessionalLearningTrajectoryEventRepository(session)
    item = await repo.find_one(id=item_id, is_active=is_active)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Профессиональная траектория обучения ребенка' не найдено",
        )
    return item


@router.post(
    "/support/professional-learning-trajectory/events/",
    response_model=OrganizationProfessionalLearningTrajectoryEventResponse,
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

    repo = OrganizationProfessionalLearningTrajectoryEventRepository(session)
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
    "/support/professional-learning-trajectory/events/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryEventResponse,
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
    repo = OrganizationProfessionalLearningTrajectoryEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Профессиональная траектория обучения ребенка' не найдено",
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
    "/support/professional-learning-trajectory/events/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Профессиональная траектория обучения ребенка' не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие проекта 'Профессиональная траектория обучения ребенка' не найдено",
        )
    return {
        "message": "Мероприятие проекта 'Профессиональная траектория обучения ребенка' успешно удалено"
    }


# Organization Professional Learning Trajectory Contacts
@router.get(
    "/support/professional-learning-trajectory/contacts/",
    response_model=list[OrganizationProfessionalLearningTrajectoryContactResponse],
)
async def get_professional_learning_trajectory_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationProfessionalLearningTrajectoryContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support/professional-learning-trajectory/contacts/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryContactResponse,
)
async def get_professional_learning_trajectory_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationProfessionalLearningTrajectoryContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Профессиональная траектория обучения ребенка' не найден",
        )
    return item


@router.post(
    "/support/professional-learning-trajectory/contacts/",
    response_model=OrganizationProfessionalLearningTrajectoryContactResponse,
)
async def create_professional_learning_trajectory_contact(
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
    )
    return item


@router.put(
    "/support/professional-learning-trajectory/contacts/{item_id}/",
    response_model=OrganizationProfessionalLearningTrajectoryContactResponse,
)
async def update_professional_learning_trajectory_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Профессиональная траектория обучения ребенка' не найден",
        )

    return item


@router.delete(
    "/support/professional-learning-trajectory/contacts/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_professional_learning_trajectory_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationProfessionalLearningTrajectoryContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт проекта 'Профессиональная траектория обучения ребенка' не найден",
        )
    return {
        "message": "Контакт проекта 'Профессиональная траектория обучения ребенка' успешно удален"
    }
