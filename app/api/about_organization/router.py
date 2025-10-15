import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from api.dependencies import get_current_active_user
from api.delivered_opportunities.router import router as delivered_opportunities_router
from api.managers.router import router as managers_router
from api.documents.router import router as documents_router
from core.file.about_organization_service import about_organization_service
from api.about_organization.schemas import (
    AboutOrganizationResponse,
)


router = APIRouter()


router.include_router(
    delivered_opportunities_router,
    prefix="/delivered-opportunities",
)
router.include_router(
    managers_router,
    prefix="/managers",
)
router.include_router(
    documents_router,
    prefix="/documents",
)


@router.get("/", response_model=AboutOrganizationResponse)
async def get_about_organization():
    about_organization = await about_organization_service.get_about_organization()
    if not about_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )
    return about_organization


@router.get("/{about_organization_id}/", response_model=AboutOrganizationResponse)
async def get_about_organization_by_id(
    about_organization_id: uuid.UUID,
):
    about_organization = await about_organization_service.get_about_organization()
    if not about_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )
    # Проверяем, совпадает ли запрашиваемый ID с ID в данных
    if str(about_organization.id) != str(about_organization_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )
    return about_organization


@router.post("/", response_model=AboutOrganizationResponse)
async def create_about_organization(
    title: Annotated[str, Form()],
    full_name: Annotated[str, Form()],
    short_name: Annotated[str, Form()],
    creation_date: Annotated[str, Form()],  # Формат: dd.mm.YYYY
    founder: Annotated[str, Form()],
    location: Annotated[str, Form()],
    work_schedule: Annotated[str, Form()],
    contact_phone: Annotated[str, Form()],
    contact_email: Annotated[str, Form()],
    document_file: UploadFile,  # Файл документа
    user: User = Depends(get_current_active_user),
):
    # Проверяем, существует ли уже информация об организации
    existing_about_organization = (
        await about_organization_service.get_about_organization()
    )
    if existing_about_organization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Информация об организации уже существует. Используйте PUT для обновления.",
        )

    # Сохраняем документ
    document_url = await file_service.save_file(
        upload_file=document_file,
        subdirectory=DOCUMENTS_FOLDER,
    )

    # Создаем информацию об организации
    from api.about_organization.schemas import AboutOrganizationCreate

    about_organization_data = AboutOrganizationCreate(
        title=title,
        full_name=full_name,
        short_name=short_name,
        creation_date=creation_date,
        founder=founder,
        location=location,
        work_schedule=work_schedule,
        contact_phone=contact_phone,
        contact_email=contact_email,
        document_url=document_url,
    )

    about_organization = await about_organization_service.create_about_organization(
        about_organization_data
    )

    return about_organization


@router.put("/{about_organization_id}/", response_model=AboutOrganizationResponse)
async def update_about_organization(
    about_organization_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    full_name: Annotated[str | None, Form()] = None,
    short_name: Annotated[str | None, Form()] = None,
    creation_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY
    founder: Annotated[str | None, Form()] = None,
    location: Annotated[str | None, Form()] = None,
    work_schedule: Annotated[str | None, Form()] = None,
    contact_phone: Annotated[str | None, Form()] = None,
    contact_email: Annotated[str | None, Form()] = None,
    document_file: UploadFile | None = None,  # Файл документа (опционально)
    user: User = Depends(get_current_active_user),
):
    current_about_organization = (
        await about_organization_service.get_about_organization()
    )

    if not current_about_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )

    # Проверяем, совпадает ли запрашиваемый ID с ID в данных
    if str(current_about_organization.id) != str(about_organization_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )

    # Если загружен новый документ, удаляем старый и сохраняем новый
    document_url = None
    if document_file:
        # Удаляем старый документ
        await file_service.delete_file(current_about_organization.document_url)
        # Сохраняем новый документ
        document_url = await file_service.save_file(
            upload_file=document_file,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Подготовим данные для обновления
    from api.about_organization.schemas import AboutOrganizationUpdate

    update_data = {
        "title": title,
        "full_name": full_name,
        "short_name": short_name,
        "creation_date": creation_date,
        "founder": founder,
        "location": location,
        "work_schedule": work_schedule,
        "contact_phone": contact_phone,
        "contact_email": contact_email,
    }
    # Удаляем None значения
    update_data = {k: v for k, v in update_data.items() if v is not None}

    if document_url:
        update_data["document_url"] = document_url

    # Обновляем информацию об организации
    about_organization = await about_organization_service.update_about_organization(
        AboutOrganizationUpdate(**update_data)
    )

    if not about_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )

    return about_organization


@router.delete("/{about_organization_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_about_organization(
    about_organization_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
):
    current_about_organization = (
        await about_organization_service.get_about_organization()
    )

    if not current_about_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )

    # Проверяем, совпадает ли запрашиваемый ID с ID в данных
    if str(current_about_organization.id) != str(about_organization_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )

    # Удаляем документ
    await file_service.delete_file(current_about_organization.document_url)

    # Удаляем информацию об организации
    deleted = await about_organization_service.delete_about_organization()
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )
    return {"message": "Информация об организации успешно удалена"}
