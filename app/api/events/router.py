import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, EVENTS_IMAGES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user, verify_active_param_access
from api.events.repository import EventRepository
from api.events.schemas import (
    EventCreate,
    EventResponse,
    EventUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[EventResponse])
async def get_events(
    is_active: bool = Depends(verify_active_param_access),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    event_repo = EventRepository(session)
    events = await event_repo.find_all(is_active=is_active)
    return events


@router.get("/{event_id}/", response_model=EventResponse)
async def get_event_by_id(
    event_id: uuid.UUID,
    is_active: bool = Depends(verify_active_param_access),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    event_repo = EventRepository(session)
    event = await event_repo.find_one(id=event_id, is_active=is_active)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие не найдено",
        )
    return event


@router.post("/", response_model=EventResponse)
async def create_event(
    site_section: Annotated[str, Form()],
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    subpage: Annotated[str | None, Form()] = None,
    event_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool, Form()] = True,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение мероприятия (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=EVENTS_IMAGES_FOLDER,
        )

    # Создаем запись о мероприятии
    event_repo = EventRepository(session)
    event = await event_repo.create(
        site_section=site_section,
        subpage=subpage,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )
    return event


@router.put("/{event_id}/", response_model=EventResponse)
async def update_event(
    event_id: uuid.UUID,
    site_section: Annotated[str | None, Form()] = None,
    subpage: Annotated[str | None, Form()] = None,
    title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    event_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY hh:mm
    location: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    is_active: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    event_repo = EventRepository(session)
    current_event = await event_repo.get_by_id(event_id)

    if not current_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие не найдено",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_event.image_url:
            await file_service.delete_file(current_event.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=EVENTS_IMAGES_FOLDER,
        )

    # Обновляем информацию о мероприятии
    event = await event_repo.update(
        obj_id=event_id,
        site_section=site_section,
        subpage=subpage,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image_url=image_url,
        is_active=is_active,
    )

    return event


@router.delete("/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    event_repo = EventRepository(session)
    current_event = await event_repo.get_by_id(event_id)

    if not current_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие не найдено",
        )

    # Удаляем изображение
    if current_event.image_url:
        await file_service.delete_file(current_event.image_url)

    # Удаляем запись о мероприятии
    deleted = await event_repo.delete(event_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие не найдено",
        )
    return {"message": "Мероприятие успешно удалено"}
