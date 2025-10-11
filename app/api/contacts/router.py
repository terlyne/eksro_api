import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.contacts.repository import ContactRepository
from api.contacts.schemas import (
    ContactCreate,
    ContactResponse,
    ContactUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    contact_repo = ContactRepository(session)
    contacts = await contact_repo.get_all()
    return contacts


@router.get("/{contact_id}/", response_model=ContactResponse)
async def get_contact_by_id(
    contact_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    contact_repo = ContactRepository(session)
    contact = await contact_repo.get_by_id(contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт не найден",
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str, Form()] = None,
    address: Annotated[str | None, Form()] = None,
    vk_group: Annotated[str | None, Form()] = None,
    tg_channel: Annotated[str | None, Form()] = None,
    discipline: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    work_hours: Annotated[str | None, Form()] = None,
    date_of_created: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY
    full_name: Annotated[str | None, Form()] = None,
    short_name: Annotated[str | None, Form()] = None,
    organization_founder: Annotated[str | None, Form()] = None,
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

    # Создаем запись о контакте
    contact_repo = ContactRepository(session)
    contact = await contact_repo.create(
        email=email,
        phone=phone,
        address=address,
        vk_group=vk_group,
        tg_channel=tg_channel,
        discipline=discipline,
        image_url=image_url,
        work_hours=work_hours,
        date_of_created=date_of_created,
        full_name=full_name,
        short_name=short_name,
        organization_founder=organization_founder,
    )
    return contact


@router.put("/{contact_id}/", response_model=ContactResponse)
async def update_contact(
    contact_id: uuid.UUID,
    email: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    address: Annotated[str | None, Form()] = None,
    vk_group: Annotated[str | None, Form()] = None,
    tg_channel: Annotated[str | None, Form()] = None,
    discipline: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    work_hours: Annotated[str | None, Form()] = None,
    date_of_created: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY
    full_name: Annotated[str | None, Form()] = None,
    short_name: Annotated[str | None, Form()] = None,
    organization_founder: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    contact_repo = ContactRepository(session)
    current_contact = await contact_repo.get_by_id(contact_id)

    if not current_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_contact.image_url:
            await file_service.delete_file(current_contact.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о контакте
    contact = await contact_repo.update(
        obj_id=contact_id,
        email=email,
        phone=phone,
        address=address,
        vk_group=vk_group,
        tg_channel=tg_channel,
        discipline=discipline,
        image_url=image_url,
        work_hours=work_hours,
        date_of_created=date_of_created,
        full_name=full_name,
        short_name=short_name,
        organization_founder=organization_founder,
    )

    return contact


@router.delete("/{contact_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    contact_repo = ContactRepository(session)
    current_contact = await contact_repo.get_by_id(contact_id)

    if not current_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт не найден",
        )

    # Удаляем изображение
    if current_contact.image_url:
        await file_service.delete_file(current_contact.image_url)

    # Удаляем запись о контакте
    deleted = await contact_repo.delete(contact_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Контакт не найден",
        )
    return {"message": "Контакт успешно удален"}
