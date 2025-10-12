import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user, verify_active_param_access
from api.soviet_section.repository import (
    SovietSupportDocumentRepository,
    SovietSupportEventRepository,
    SovietSupportApplicationRepository,
    SovietLeaderRepository,
    SovietNewsRepository,
    SovietQuestionRepository,
    SovietContactRepository,
    LearningDocumentRepository,
    LearningEventRepository,
    LearningApplicationRepository,
    LearningNewsRepository,
    LearningQuestionRepository,
    LearningContactRepository,
    OnlineConferenceRegulationRepository,
    OnlineConferenceParticipantRepository,
    OnlineConferenceNewsRepository,
    OnlineConferenceQuestionRepository,
    OnlineConferenceContactRepository,
    PodcastApplicationRepository,
    PodcastParticipantRepository,
    PodcastNewsRepository,
    PodcastContactRepository,
    ProjectNewsRepository,
    ProjectReportRepository,
    CompetitionDocumentRepository,
    CompetitionContactRepository,
    JournalNewsRepository,
    JournalContactRepository,
)
from api.soviet_section.schemas import (
    SovietSupportDocumentCreate,
    SovietSupportDocumentResponse,
    SovietSupportDocumentUpdate,
    SovietSupportEventCreate,
    SovietSupportEventResponse,
    SovietSupportEventUpdate,
    SovietSupportApplicationCreate,
    SovietSupportApplicationResponse,
    SovietSupportApplicationUpdate,
    SovietLeaderCreate,
    SovietLeaderResponse,
    SovietLeaderUpdate,
    SovietNewsCreate,
    SovietNewsResponse,
    SovietNewsUpdate,
    SovietQuestionCreate,
    SovietQuestionResponse,
    SovietQuestionUpdate,
    SovietContactCreate,
    SovietContactResponse,
    SovietContactUpdate,
    LearningDocumentCreate,
    LearningDocumentResponse,
    LearningDocumentUpdate,
    LearningEventCreate,
    LearningEventResponse,
    LearningEventUpdate,
    LearningApplicationCreate,
    LearningApplicationResponse,
    LearningApplicationUpdate,
    LearningNewsCreate,
    LearningNewsResponse,
    LearningNewsUpdate,
    LearningQuestionCreate,
    LearningQuestionResponse,
    LearningQuestionUpdate,
    LearningContactCreate,
    LearningContactResponse,
    LearningContactUpdate,
    OnlineConferenceRegulationCreate,
    OnlineConferenceRegulationResponse,
    OnlineConferenceRegulationUpdate,
    OnlineConferenceParticipantCreate,
    OnlineConferenceParticipantResponse,
    OnlineConferenceParticipantUpdate,
    OnlineConferenceNewsCreate,
    OnlineConferenceNewsResponse,
    OnlineConferenceNewsUpdate,
    OnlineConferenceQuestionCreate,
    OnlineConferenceQuestionResponse,
    OnlineConferenceQuestionUpdate,
    OnlineConferenceContactCreate,
    OnlineConferenceContactResponse,
    OnlineConferenceContactUpdate,
    PodcastApplicationCreate,
    PodcastApplicationResponse,
    PodcastApplicationUpdate,
    PodcastParticipantCreate,
    PodcastParticipantResponse,
    PodcastParticipantUpdate,
    PodcastNewsCreate,
    PodcastNewsResponse,
    PodcastNewsUpdate,
    PodcastContactCreate,
    PodcastContactResponse,
    PodcastContactUpdate,
    ProjectNewsCreate,
    ProjectNewsResponse,
    ProjectNewsUpdate,
    ProjectReportCreate,
    ProjectReportResponse,
    ProjectReportUpdate,
    CompetitionDocumentCreate,
    CompetitionDocumentResponse,
    CompetitionDocumentUpdate,
    CompetitionContactCreate,
    CompetitionContactResponse,
    CompetitionContactUpdate,
    JournalNewsCreate,
    JournalNewsResponse,
    JournalNewsUpdate,
    JournalContactCreate,
    JournalContactResponse,
    JournalContactUpdate,
)


router = APIRouter()


# Soviet Support Documents
@router.get("/support-documents/", response_model=list[SovietSupportDocumentResponse])
async def get_soviet_support_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = SovietSupportDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support-documents/{item_id}/", response_model=SovietSupportDocumentResponse
)
async def get_soviet_support_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = SovietSupportDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки совета не найден",
        )
    return item


@router.post("/support-documents/", response_model=SovietSupportDocumentResponse)
async def create_soviet_support_document(
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
    repo = SovietSupportDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/support-documents/{item_id}/", response_model=SovietSupportDocumentResponse
)
async def update_soviet_support_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietSupportDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки совета не найден",
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


@router.delete("/support-documents/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_soviet_support_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietSupportDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки совета не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ поддержки совета не найден",
        )
    return {"message": "Документ поддержки совета успешно удален"}


# Soviet Support Events
@router.get("/support-events/", response_model=list[SovietSupportEventResponse])
async def get_soviet_support_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = SovietSupportEventRepository(session)
    items = await repo.find_all(is_active=is_active)
    return items


@router.get("/support-events/{item_id}/", response_model=SovietSupportEventResponse)
async def get_soviet_support_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    repo = SovietSupportEventRepository(session)
    item = await repo.find_one(id=item_id, is_active=is_active)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки совета не найдено",
        )
    return item


@router.post("/support-events/", response_model=SovietSupportEventResponse)
async def create_soviet_support_event(
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

    repo = SovietSupportEventRepository(session)
    item = await repo.create(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )
    return item


@router.put("/support-events/{item_id}/", response_model=SovietSupportEventResponse)
async def update_soviet_support_event(
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
    repo = SovietSupportEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки совета не найдено",
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


@router.delete("/support-events/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_soviet_support_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietSupportEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки совета не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие поддержки совета не найдено",
        )
    return {"message": "Мероприятие поддержки совета успешно удалено"}


# Soviet Support Applications
@router.get(
    "/support-applications/", response_model=list[SovietSupportApplicationResponse]
)
async def get_soviet_support_applications(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietSupportApplicationRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/support-applications/{item_id}/", response_model=SovietSupportApplicationResponse
)
async def get_soviet_support_application_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietSupportApplicationRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на поддержку совета не найдена",
        )
    return item


@router.post("/support-applications/", response_model=SovietSupportApplicationResponse)
async def create_soviet_support_application(
    application_type: Annotated[
        str, Form()
    ],  # "Консультация", "Вступление в УС", "Другое"
    full_name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    text: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = SovietSupportApplicationRepository(session)
    item = await repo.create(
        application_type=application_type,
        full_name=full_name,
        phone=phone,
        email=email,
        text=text,
    )
    return item


@router.put(
    "/support-applications/{item_id}/", response_model=SovietSupportApplicationResponse
)
async def update_soviet_support_application(
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
    repo = SovietSupportApplicationRepository(session)
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
            detail="Заявка на поддержку совета не найдена",
        )

    return item


@router.delete(
    "/support-applications/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_soviet_support_application(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietSupportApplicationRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на поддержку совета не найдена",
        )
    return {"message": "Заявка на поддержку совета успешно удалена"}


# Soviet Leaders
@router.get("/leaders/", response_model=list[SovietLeaderResponse])
async def get_soviet_leaders(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietLeaderRepository(session)
    items = await repo.get_all()
    return items


@router.get("/leaders/{item_id}/", response_model=SovietLeaderResponse)
async def get_soviet_leader_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietLeaderRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель совета не найден",
        )
    return item


@router.post("/leaders/", response_model=SovietLeaderResponse)
async def create_soviet_leader(
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

    repo = SovietLeaderRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put("/leaders/{item_id}/", response_model=SovietLeaderResponse)
async def update_soviet_leader(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietLeaderRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель совета не найден",
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
async def delete_soviet_leader(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietLeaderRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель совета не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о руководителе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель совета не найден",
        )
    return {"message": "Руководитель совета успешно удален"}


# Soviet News
@router.get("/news/", response_model=list[SovietNewsResponse])
async def get_soviet_news(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/news/{item_id}/", response_model=SovietNewsResponse)
async def get_soviet_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость совета не найдена",
        )
    return item


@router.post("/news/", response_model=SovietNewsResponse)
async def create_soviet_news(
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

    repo = SovietNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put("/news/{item_id}/", response_model=SovietNewsResponse)
async def update_soviet_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость совета не найдена",
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
async def delete_soviet_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость совета не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость совета не найдена",
        )
    return {"message": "Новость совета успешно удалена"}


# Soviet Questions
@router.get("/questions/", response_model=list[SovietQuestionResponse])
async def get_soviet_questions(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietQuestionRepository(session)
    items = await repo.get_all()
    return items


@router.get("/questions/{item_id}/", response_model=SovietQuestionResponse)
async def get_soviet_question_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietQuestionRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос совета не найден",
        )
    return item


@router.post("/questions/", response_model=SovietQuestionResponse)
async def create_soviet_question(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    message: Annotated[str, Form()],
    phone: Annotated[str | None, Form()] = None,
    response: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietQuestionRepository(session)
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


@router.put("/questions/{item_id}/", response_model=SovietQuestionResponse)
async def update_soviet_question(
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
    repo = SovietQuestionRepository(session)

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
            detail="Вопрос совета не найден",
        )

    return item


@router.delete("/questions/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_soviet_question(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietQuestionRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос совета не найден",
        )
    return {"message": "Вопрос совета успешно удален"}


# Soviet Contacts
@router.get("/contacts/", response_model=list[SovietContactResponse])
async def get_soviet_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/contacts/{item_id}/", response_model=SovietContactResponse)
async def get_soviet_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт совета не найден",
        )
    return item


@router.post("/contacts/", response_model=SovietContactResponse)
async def create_soviet_contact(
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    tg_channel: Annotated[str | None, Form()] = None,
    vk_group: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietContactRepository(session)
    item = await repo.create(
        phone=phone,
        email=email,
        tg_channel=tg_channel,
        vk_group=vk_group,
    )
    return item


@router.put("/contacts/{item_id}/", response_model=SovietContactResponse)
async def update_soviet_contact(
    item_id: uuid.UUID,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    tg_channel: Annotated[str | None, Form()] = None,
    vk_group: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietContactRepository(session)
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
            detail="Контакт совета не найден",
        )

    return item


@router.delete("/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_soviet_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = SovietContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт совета не найден",
        )
    return {"message": "Контакт совета успешно удален"}


# Learning Documents
@router.get("/learning/documents/", response_model=list[LearningDocumentResponse])
async def get_learning_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get("/learning/documents/{item_id}/", response_model=LearningDocumentResponse)
async def get_learning_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный документ не найден",
        )
    return item


@router.post("/learning/documents/", response_model=LearningDocumentResponse)
async def create_learning_document(
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
    repo = LearningDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put("/learning/documents/{item_id}/", response_model=LearningDocumentResponse)
async def update_learning_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный документ не найден",
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


@router.delete("/learning/documents/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный документ не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный документ не найден",
        )
    return {"message": "Учебный документ успешно удален"}


# Learning Events
@router.get("/learning/events/", response_model=list[LearningEventResponse])
async def get_learning_events(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningEventRepository(session)
    items = await repo.get_all()
    return items


@router.get("/learning/events/{item_id}/", response_model=LearningEventResponse)
async def get_learning_event_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningEventRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебное мероприятие не найдено",
        )
    return item


@router.post("/learning/events/", response_model=LearningEventResponse)
async def create_learning_event(
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

    repo = LearningEventRepository(session)
    item = await repo.create(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )
    return item


@router.put("/learning/events/{item_id}/", response_model=LearningEventResponse)
async def update_learning_event(
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
    repo = LearningEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебное мероприятие не найдено",
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


@router.delete("/learning/events/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_event(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningEventRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебное мероприятие не найдено",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о мероприятии
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебное мероприятие не найдено",
        )
    return {"message": "Учебное мероприятие успешно удалено"}


# Learning Applications
@router.get("/learning/applications/", response_model=list[LearningApplicationResponse])
async def get_learning_applications(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningApplicationRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/learning/applications/{item_id}/", response_model=LearningApplicationResponse
)
async def get_learning_application_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningApplicationRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебная заявка не найдена",
        )
    return item


@router.post("/learning/applications/", response_model=LearningApplicationResponse)
async def create_learning_application(
    application_type: Annotated[str, Form()],  # "Платное", "Бесплатное" или "Другое"
    full_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    text: Annotated[str, Form()],
    phone: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningApplicationRepository(session)
    item = await repo.create(
        application_type=application_type,
        full_name=full_name,
        phone=phone,
        email=email,
        text=text,
    )
    return item


@router.put(
    "/learning/applications/{item_id}/", response_model=LearningApplicationResponse
)
async def update_learning_application(
    item_id: uuid.UUID,
    application_type: Annotated[
        str | None, Form()
    ] = None,  # "Платное", "Бесплатное" или "Другое"
    full_name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    text: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningApplicationRepository(session)
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
            detail="Учебная заявка не найдена",
        )

    return item


@router.delete(
    "/learning/applications/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_learning_application(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningApplicationRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебная заявка не найдена",
        )
    return {"message": "Учебная заявка успешно удалена"}


# Learning News
@router.get("/learning/news/", response_model=list[LearningNewsResponse])
async def get_learning_news(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/learning/news/{item_id}/", response_model=LearningNewsResponse)
async def get_learning_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебная новость не найдена",
        )
    return item


@router.post("/learning/news/", response_model=LearningNewsResponse)
async def create_learning_news(
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

    repo = LearningNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put("/learning/news/{item_id}/", response_model=LearningNewsResponse)
async def update_learning_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебная новость не найдена",
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


@router.delete("/learning/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебная новость не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебная новость не найдена",
        )
    return {"message": "Учебная новость успешно удалена"}


# Learning Questions
@router.get("/learning/questions/", response_model=list[LearningQuestionResponse])
async def get_learning_questions(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningQuestionRepository(session)
    items = await repo.get_all()
    return items


@router.get("/learning/questions/{item_id}/", response_model=LearningQuestionResponse)
async def get_learning_question_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningQuestionRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный вопрос не найден",
        )
    return item


@router.post("/learning/questions/", response_model=LearningQuestionResponse)
async def create_learning_question(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    message: Annotated[str, Form()],
    phone: Annotated[str | None, Form()] = None,
    response: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningQuestionRepository(session)
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


@router.put("/learning/questions/{item_id}/", response_model=LearningQuestionResponse)
async def update_learning_question(
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
    repo = LearningQuestionRepository(session)

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
            detail="Учебный вопрос не найден",
        )

    return item


@router.delete("/learning/questions/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_question(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningQuestionRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный вопрос не найден",
        )
    return {"message": "Учебный вопрос успешно удален"}


# Learning Contacts
@router.get("/learning/contacts/", response_model=list[LearningContactResponse])
async def get_learning_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/learning/contacts/{item_id}/", response_model=LearningContactResponse)
async def get_learning_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный контакт не найден",
        )
    return item


@router.post("/learning/contacts/", response_model=LearningContactResponse)
async def create_learning_contact(
    full_name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
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

    repo = LearningContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        description=description,
        email=email,
        phone=phone,
        image_url=image_url,
    )
    return item


@router.put("/learning/contacts/{item_id}/", response_model=LearningContactResponse)
async def update_learning_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный контакт не найден",
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
        description=description,
        email=email,
        phone=phone,
        image_url=image_url,
    )

    return item


@router.delete("/learning/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = LearningContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный контакт не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о контакте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Учебный контакт не найден",
        )
    return {"message": "Учебный контакт успешно удален"}


# Online Conference Regulations
@router.get(
    "/online-conference/regulations/",
    response_model=list[OnlineConferenceRegulationResponse],
)
async def get_online_conference_regulations(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceRegulationRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/online-conference/regulations/{item_id}/",
    response_model=OnlineConferenceRegulationResponse,
)
async def get_online_conference_regulation_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceRegulationRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Регламент онлайн-конференции не найден",
        )
    return item


@router.post(
    "/online-conference/regulations/", response_model=OnlineConferenceRegulationResponse
)
async def create_online_conference_regulation(
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

    # Создаем запись о регламенте
    repo = OnlineConferenceRegulationRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/online-conference/regulations/{item_id}/",
    response_model=OnlineConferenceRegulationResponse,
)
async def update_online_conference_regulation(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceRegulationRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Регламент онлайн-конференции не найден",
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

    # Обновляем информацию о регламенте
    item = await repo.update(
        obj_id=item_id,
        title=title,
        file_url=file_url,
    )

    return item


@router.delete(
    "/online-conference/regulations/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_online_conference_regulation(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceRegulationRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Регламент онлайн-конференции не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о регламенте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Регламент онлайн-конференции не найден",
        )
    return {"message": "Регламент онлайн-конференции успешно удален"}


# Online Conference Participants
@router.get(
    "/online-conference/participants/",
    response_model=list[OnlineConferenceParticipantResponse],
)
async def get_online_conference_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceParticipantRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/online-conference/participants/{item_id}/",
    response_model=OnlineConferenceParticipantResponse,
)
async def get_online_conference_participant_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceParticipantRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник онлайн-конференции не найден",
        )
    return item


@router.post(
    "/online-conference/participants/",
    response_model=OnlineConferenceParticipantResponse,
)
async def create_online_conference_participant(
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

    repo = OnlineConferenceParticipantRepository(session)
    item = await repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return item


@router.put(
    "/online-conference/participants/{item_id}/",
    response_model=OnlineConferenceParticipantResponse,
)
async def update_online_conference_participant(
    item_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник онлайн-конференции не найден",
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
    "/online-conference/participants/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_online_conference_participant(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceParticipantRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник онлайн-конференции не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись об участнике
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник онлайн-конференции не найден",
        )
    return {"message": "Участник онлайн-конференции успешно удален"}


# Online Conference News
@router.get(
    "/online-conference/news/", response_model=list[OnlineConferenceNewsResponse]
)
async def get_online_conference_news(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/online-conference/news/{item_id}/", response_model=OnlineConferenceNewsResponse
)
async def get_online_conference_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость онлайн-конференции не найдена",
        )
    return item


@router.post("/online-conference/news/", response_model=OnlineConferenceNewsResponse)
async def create_online_conference_news(
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

    repo = OnlineConferenceNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put(
    "/online-conference/news/{item_id}/", response_model=OnlineConferenceNewsResponse
)
async def update_online_conference_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость онлайн-конференции не найдена",
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


@router.delete(
    "/online-conference/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_online_conference_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость онлайн-конференции не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость онлайн-конференции не найдена",
        )
    return {"message": "Новость онлайн-конференции успешно удалена"}


# Online Conference Questions
@router.get(
    "/online-conference/questions/",
    response_model=list[OnlineConferenceQuestionResponse],
)
async def get_online_conference_questions(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceQuestionRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/online-conference/questions/{item_id}/",
    response_model=OnlineConferenceQuestionResponse,
)
async def get_online_conference_question_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceQuestionRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос онлайн-конференции не найден",
        )
    return item


@router.post(
    "/online-conference/questions/", response_model=OnlineConferenceQuestionResponse
)
async def create_online_conference_question(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    message: Annotated[str, Form()],
    phone: Annotated[str | None, Form()] = None,
    response: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceQuestionRepository(session)
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
    "/online-conference/questions/{item_id}/",
    response_model=OnlineConferenceQuestionResponse,
)
async def update_online_conference_question(
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
    repo = OnlineConferenceQuestionRepository(session)

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
            detail="Вопрос онлайн-конференции не найден",
        )

    return item


@router.delete(
    "/online-conference/questions/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_online_conference_question(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceQuestionRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос онлайн-конференции не найден",
        )
    return {"message": "Вопрос онлайн-конференции успешно удален"}


# Online Conference Contacts
@router.get(
    "/online-conference/contacts/", response_model=list[OnlineConferenceContactResponse]
)
async def get_online_conference_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/online-conference/contacts/{item_id}/",
    response_model=OnlineConferenceContactResponse,
)
async def get_online_conference_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт онлайн-конференции не найден",
        )
    return item


@router.post(
    "/online-conference/contacts/", response_model=OnlineConferenceContactResponse
)
async def create_online_conference_contact(
    full_name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
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

    repo = OnlineConferenceContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        description=description,
        email=email,
        phone=phone,
        image_url=image_url,
    )
    return item


@router.put(
    "/online-conference/contacts/{item_id}/",
    response_model=OnlineConferenceContactResponse,
)
async def update_online_conference_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт онлайн-конференции не найден",
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
        description=description,
        email=email,
        phone=phone,
        image_url=image_url,
    )

    return item


@router.delete(
    "/online-conference/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_online_conference_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = OnlineConferenceContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт онлайн-конференции не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о контакте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт онлайн-конференции не найден",
        )
    return {"message": "Контакт онлайн-конференции успешно удален"}


# Podcast Applications
@router.get("/podcast/applications/", response_model=list[PodcastApplicationResponse])
async def get_podcast_applications(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastApplicationRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/podcast/applications/{item_id}/", response_model=PodcastApplicationResponse
)
async def get_podcast_application_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastApplicationRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на подкаст не найдена",
        )
    return item


@router.post("/podcast/applications/", response_model=PodcastApplicationResponse)
async def create_podcast_application(
    application_type: Annotated[
        str, Form()
    ],  # "Образовательный", "Разговорный" или "Другое"
    full_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    text: Annotated[str, Form()],
    phone: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastApplicationRepository(session)
    item = await repo.create(
        application_type=application_type,
        full_name=full_name,
        phone=phone,
        email=email,
        text=text,
    )
    return item


@router.put(
    "/podcast/applications/{item_id}/", response_model=PodcastApplicationResponse
)
async def update_podcast_application(
    item_id: uuid.UUID,
    application_type: Annotated[
        str | None, Form()
    ] = None,  # "Образовательный", "Разговорный" или "Другое"
    full_name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    text: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastApplicationRepository(session)
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
            detail="Заявка на подкаст не найдена",
        )

    return item


@router.delete(
    "/podcast/applications/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_podcast_application(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastApplicationRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка на подкаст не найдена",
        )
    return {"message": "Заявка на подкаст успешно удалена"}


# Podcast Participants
@router.get("/podcast/participants/", response_model=list[PodcastParticipantResponse])
async def get_podcast_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastParticipantRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/podcast/participants/{item_id}/", response_model=PodcastParticipantResponse
)
async def get_podcast_participant_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastParticipantRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник подкаста не найден",
        )
    return item


@router.post("/podcast/participants/", response_model=PodcastParticipantResponse)
async def create_podcast_participant(
    video_url: Annotated[str, Form()],
    guests: Annotated[list[str], Form()],  # Список гостей
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastParticipantRepository(session)
    item = await repo.create(
        video_url=video_url,
        guests=guests,
    )
    return item


@router.put(
    "/podcast/participants/{item_id}/", response_model=PodcastParticipantResponse
)
async def update_podcast_participant(
    item_id: uuid.UUID,
    video_url: Annotated[str | None, Form()] = None,
    guests: Annotated[list[str] | None, Form()] = None,  # Список гостей
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastParticipantRepository(session)
    item = await repo.update(
        obj_id=item_id,
        video_url=video_url,
        guests=guests,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник подкаста не найден",
        )

    return item


@router.delete(
    "/podcast/participants/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_podcast_participant(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastParticipantRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник подкаста не найден",
        )
    return {"message": "Участник подкаста успешно удален"}


# Podcast News
@router.get("/podcast/news/", response_model=list[PodcastNewsResponse])
async def get_podcast_news(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/podcast/news/{item_id}/", response_model=PodcastNewsResponse)
async def get_podcast_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость подкаста не найдена",
        )
    return item


@router.post("/podcast/news/", response_model=PodcastNewsResponse)
async def create_podcast_news(
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

    repo = PodcastNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put("/podcast/news/{item_id}/", response_model=PodcastNewsResponse)
async def update_podcast_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость подкаста не найдена",
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


@router.delete("/podcast/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_podcast_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость подкаста не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость подкаста не найдена",
        )
    return {"message": "Новость подкаста успешно удалена"}


# Podcast Contacts
@router.get("/podcast/contacts/", response_model=list[PodcastContactResponse])
async def get_podcast_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/podcast/contacts/{item_id}/", response_model=PodcastContactResponse)
async def get_podcast_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт подкаста не найден",
        )
    return item


@router.post("/podcast/contacts/", response_model=PodcastContactResponse)
async def create_podcast_contact(
    full_name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
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

    repo = PodcastContactRepository(session)
    item = await repo.create(
        full_name=full_name,
        description=description,
        email=email,
        phone=phone,
        image_url=image_url,
    )
    return item


@router.put("/podcast/contacts/{item_id}/", response_model=PodcastContactResponse)
async def update_podcast_contact(
    item_id: uuid.UUID,
    full_name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт подкаста не найден",
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
        description=description,
        email=email,
        phone=phone,
        image_url=image_url,
    )

    return item


@router.delete("/podcast/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_podcast_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = PodcastContactRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт подкаста не найден",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о контакте
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт подкаста не найден",
        )
    return {"message": "Контакт подкаста успешно удален"}


# Project News
@router.get("/project/news/", response_model=list[ProjectNewsResponse])
async def get_project_news(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/project/news/{item_id}/", response_model=ProjectNewsResponse)
async def get_project_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость проекта не найдена",
        )
    return item


@router.post("/project/news/", response_model=ProjectNewsResponse)
async def create_project_news(
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

    repo = ProjectNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put("/project/news/{item_id}/", response_model=ProjectNewsResponse)
async def update_project_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость проекта не найдена",
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


@router.delete("/project/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость проекта не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость проекта не найдена",
        )
    return {"message": "Новость проекта успешно удалена"}


# Project Reports
@router.get("/project/reports/", response_model=list[ProjectReportResponse])
async def get_project_reports(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectReportRepository(session)
    items = await repo.get_all()
    return items


@router.get("/project/reports/{item_id}/", response_model=ProjectReportResponse)
async def get_project_report_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectReportRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет проекта не найден",
        )
    return item


@router.post("/project/reports/", response_model=ProjectReportResponse)
async def create_project_report(
    organization_name: Annotated[str, Form()],
    video_url: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectReportRepository(session)
    item = await repo.create(
        organization_name=organization_name,
        video_url=video_url,
    )
    return item


@router.put("/project/reports/{item_id}/", response_model=ProjectReportResponse)
async def update_project_report(
    item_id: uuid.UUID,
    organization_name: Annotated[str | None, Form()] = None,
    video_url: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectReportRepository(session)
    item = await repo.update(
        obj_id=item_id,
        organization_name=organization_name,
        video_url=video_url,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет проекта не найден",
        )

    return item


@router.delete("/project/reports/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_report(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = ProjectReportRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет проекта не найден",
        )
    return {"message": "Отчет проекта успешно удален"}


# Competition Documents
@router.get("/competition/documents/", response_model=list[CompetitionDocumentResponse])
async def get_competition_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionDocumentRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/competition/documents/{item_id}/", response_model=CompetitionDocumentResponse
)
async def get_competition_document_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionDocumentRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ конкурса не найден",
        )
    return item


@router.post("/competition/documents/", response_model=CompetitionDocumentResponse)
async def create_competition_document(
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
    repo = CompetitionDocumentRepository(session)
    item = await repo.create(
        title=title,
        file_url=file_url,
    )
    return item


@router.put(
    "/competition/documents/{item_id}/", response_model=CompetitionDocumentResponse
)
async def update_competition_document(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ конкурса не найден",
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
    "/competition/documents/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_competition_document(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionDocumentRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ конкурса не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_item.file_url)

    # Удаляем запись о документе
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ конкурса не найден",
        )
    return {"message": "Документ конкурса успешно удален"}


# Competition Contacts
@router.get("/competition/contacts/", response_model=list[CompetitionContactResponse])
async def get_competition_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionContactRepository(session)
    items = await repo.get_all()
    return items


@router.get(
    "/competition/contacts/{item_id}/", response_model=CompetitionContactResponse
)
async def get_competition_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт конкурса не найден",
        )
    return item


@router.post("/competition/contacts/", response_model=CompetitionContactResponse)
async def create_competition_contact(
    organization_name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionContactRepository(session)
    item = await repo.create(
        organization_name=organization_name,
        phone=phone,
        email=email,
    )
    return item


@router.put(
    "/competition/contacts/{item_id}/", response_model=CompetitionContactResponse
)
async def update_competition_contact(
    item_id: uuid.UUID,
    organization_name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        organization_name=organization_name,
        phone=phone,
        email=email,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт конкурса не найден",
        )

    return item


@router.delete(
    "/competition/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_competition_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = CompetitionContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт конкурса не найден",
        )
    return {"message": "Контакт конкурса успешно удален"}


# Journal News
@router.get("/journal/news/", response_model=list[JournalNewsResponse])
async def get_journal_news(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalNewsRepository(session)
    items = await repo.get_all()
    return items


@router.get("/journal/news/{item_id}/", response_model=JournalNewsResponse)
async def get_journal_news_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalNewsRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость журнала не найдена",
        )
    return item


@router.post("/journal/news/", response_model=JournalNewsResponse)
async def create_journal_news(
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

    repo = JournalNewsRepository(session)
    item = await repo.create(
        title=title,
        subtitle=subtitle,
        description=description,
        image_url=image_url,
    )
    return item


@router.put("/journal/news/{item_id}/", response_model=JournalNewsResponse)
async def update_journal_news(
    item_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    subtitle: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость журнала не найдена",
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


@router.delete("/journal/news/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_news(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalNewsRepository(session)
    current_item = await repo.get_by_id(item_id)

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость журнала не найдена",
        )

    # Удаляем изображение
    if current_item.image_url:
        await file_service.delete_file(current_item.image_url)

    # Удаляем запись о новости
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость журнала не найдена",
        )
    return {"message": "Новость журнала успешно удалена"}


# Journal Contacts
@router.get("/journal/contacts/", response_model=list[JournalContactResponse])
async def get_journal_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalContactRepository(session)
    items = await repo.get_all()
    return items


@router.get("/journal/contacts/{item_id}/", response_model=JournalContactResponse)
async def get_journal_contact_by_id(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalContactRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт журнала не найден",
        )
    return item


@router.post("/journal/contacts/", response_model=JournalContactResponse)
async def create_journal_contact(
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    address: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalContactRepository(session)
    item = await repo.create(
        phone=phone,
        email=email,
        address=address,
    )
    return item


@router.put("/journal/contacts/{item_id}/", response_model=JournalContactResponse)
async def update_journal_contact(
    item_id: uuid.UUID,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    address: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalContactRepository(session)
    item = await repo.update(
        obj_id=item_id,
        phone=phone,
        email=email,
        address=address,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт журнала не найден",
        )

    return item


@router.delete("/journal/contacts/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_contact(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    repo = JournalContactRepository(session)
    deleted = await repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт журнала не найден",
        )
    return {"message": "Контакт журнала успешно удален"}
