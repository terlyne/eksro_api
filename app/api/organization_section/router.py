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


# Organization Leaders
@router.get("/leaders/", response_model=list[OrganizationLeaderResponse])
async def get_leaders(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationLeaderRepository(session)
    items = await repo.get_all()
    return items


@router.get("/leaders/{item_id}/", response_model=OrganizationLeaderResponse)
async def get_leader_by_id(
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


@router.post("/leaders/", response_model=OrganizationLeaderResponse)
async def create_leader(
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


@router.put("/leaders/{item_id}/", response_model=OrganizationLeaderResponse)
async def update_leader(
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


@router.delete("/leaders/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_leader(
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


# Organization News
@router.get("/news/", response_model=list[OrganizationNewsResponse])
async def get_news(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = OrganizationNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/news/{item_id}/", response_model=OrganizationNewsResponse)
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


@router.post("/news/", response_model=OrganizationNewsResponse)
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


@router.put("/news/{item_id}/", response_model=OrganizationNewsResponse)
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


@router.delete("/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
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
@router.get("/questions/", response_model=list[OrganizationQuestionResponse])
async def get_questions(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationQuestionRepository(session)
    items = await repo.get_all()
    return items


@router.get("/questions/{item_id}/", response_model=OrganizationQuestionResponse)
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


@router.post("/questions/", response_model=OrganizationQuestionResponse)
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


@router.put("/questions/{item_id}/", response_model=OrganizationQuestionResponse)
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


@router.delete("/questions/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
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


# Organization Contacts
@router.get("/contacts/", response_model=list[OrganizationContactResponse])
async def get_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OrganizationContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/contacts/{item_id}/", response_model=OrganizationContactResponse)
async def get_contact_by_id(
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


@router.post("/contacts/", response_model=OrganizationContactResponse)
async def create_contact(
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


@router.put("/contacts/{item_id}/", response_model=OrganizationContactResponse)
async def update_contact(
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


@router.delete("/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
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
