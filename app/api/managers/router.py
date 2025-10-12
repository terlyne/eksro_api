import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, MANAGERS_IMAGES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.managers.repository import ManagerRepository
from api.managers.schemas import (
    ManagerCreate,
    ManagerResponse,
    ManagerUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[ManagerResponse])
async def get_managers(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    manager_repo = ManagerRepository(session)
    managers = await manager_repo.get_all()
    return managers


@router.get("/{manager_id}/", response_model=ManagerResponse)
async def get_manager_by_id(
    manager_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    manager_repo = ManagerRepository(session)
    manager = await manager_repo.get_by_id(manager_id)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель не найден",
        )
    return manager


@router.post("/", response_model=ManagerResponse)
async def create_manager(
    site_section: Annotated[str, Form()],
    full_name: Annotated[str, Form()],
    position: Annotated[str, Form()],
    subpage: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Сохраняем изображение руководителя (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=MANAGERS_IMAGES_FOLDER,
        )

    # Создаем запись о руководителе
    manager_repo = ManagerRepository(session)
    manager = await manager_repo.create(
        site_section=site_section,
        subpage=subpage,
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
        image_url=image_url,
    )
    return manager


@router.put("/{manager_id}/", response_model=ManagerResponse)
async def update_manager(
    manager_id: uuid.UUID,
    site_section: Annotated[str | None, Form()] = None,
    subpage: Annotated[str | None, Form()] = None,
    full_name: Annotated[str | None, Form()] = None,
    position: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    manager_repo = ManagerRepository(session)
    current_manager = await manager_repo.get_by_id(manager_id)

    if not current_manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_manager.image_url:
            await file_service.delete_file(current_manager.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=MANAGERS_IMAGES_FOLDER,
        )

    # Обновляем информацию о руководителе
    manager = await manager_repo.update(
        obj_id=manager_id,
        site_section=site_section,
        subpage=subpage,
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
        image_url=image_url,
    )

    return manager


@router.delete("/{manager_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manager(
    manager_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    manager_repo = ManagerRepository(session)
    current_manager = await manager_repo.get_by_id(manager_id)

    if not current_manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель не найден",
        )

    # Удаляем изображение
    if current_manager.image_url:
        await file_service.delete_file(current_manager.image_url)

    # Удаляем запись о руководителе
    deleted = await manager_repo.delete(manager_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Руководитель не найден",
        )
    return {"message": "Руководитель успешно удален"}
