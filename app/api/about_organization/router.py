import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.about_organization.repository import AboutOrganizationRepository
from api.about_organization.schemas import (
    AboutOrganizationCreate,
    AboutOrganizationResponse,
    AboutOrganizationUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[AboutOrganizationResponse])
async def get_about_organizations(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    about_org_repo = AboutOrganizationRepository(session)
    about_organizations = await about_org_repo.get_all()
    return about_organizations


@router.get("/{about_organization_id}/", response_model=AboutOrganizationResponse)
async def get_about_organization_by_id(
    about_organization_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    about_org_repo = AboutOrganizationRepository(session)
    about_organization = await about_org_repo.get_by_id(about_organization_id)
    if not about_organization:
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
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем документ
    document_url = await file_service.save_file(
        upload_file=document_file,
        subdirectory=DOCUMENTS_FOLDER,
    )

    # Создаем запись об организации
    about_org_repo = AboutOrganizationRepository(session)
    about_organization = await about_org_repo.create(
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
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    about_org_repo = AboutOrganizationRepository(session)
    current_about_organization = await about_org_repo.get_by_id(about_organization_id)

    if not current_about_organization:
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

    # Обновляем информацию об организации
    about_organization = await about_org_repo.update(
        obj_id=about_organization_id,
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

    return about_organization


@router.delete("/{about_organization_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_about_organization(
    about_organization_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    about_org_repo = AboutOrganizationRepository(session)
    current_about_organization = await about_org_repo.get_by_id(about_organization_id)

    if not current_about_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )

    # Удаляем документ
    await file_service.delete_file(current_about_organization.document_url)

    # Удаляем запись об организации
    deleted = await about_org_repo.delete(about_organization_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация об организации не найдена",
        )
    return {"message": "Информация об организации успешно удалена"}
