import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, SITE_IMAGES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.site_images.repository import SiteImageRepository
from api.site_images.schemas import (
    SiteImageCreate,
    SiteImageResponse,
    SiteImageUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[SiteImageResponse])
async def get_site_images(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    site_image_repo = SiteImageRepository(session)
    site_images = await site_image_repo.get_all()
    return site_images


@router.get("/{site_image_id}/", response_model=SiteImageResponse)
async def get_site_image_by_id(
    site_image_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    site_image_repo = SiteImageRepository(session)
    site_image = await site_image_repo.get_by_id(site_image_id)
    if not site_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение сайта не найдено",
        )
    return site_image


@router.post("/", response_model=SiteImageResponse)
async def create_site_image(
    name: Annotated[str, Form()],
    image: UploadFile,  # Файл изображения
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение сайта
    image_url = await file_service.save_file(
        upload_file=image,
        subdirectory=SITE_IMAGES_FOLDER,
    )

    # Создаем запись об изображении
    site_image_repo = SiteImageRepository(session)
    site_image = await site_image_repo.create(
        name=name,
        image_url=image_url,
    )
    return site_image


@router.put("/{site_image_id}/", response_model=SiteImageResponse)
async def update_site_image(
    site_image_id: uuid.UUID,
    name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    site_image_repo = SiteImageRepository(session)
    current_site_image = await site_image_repo.get_by_id(site_image_id)

    if not current_site_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение сайта не найдено",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        await file_service.delete_file(current_site_image.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=SITE_IMAGES_FOLDER,
        )

    # Обновляем информацию об изображении
    site_image = await site_image_repo.update(
        obj_id=site_image_id,
        name=name,
        image_url=image_url,
    )

    return site_image


@router.delete("/{site_image_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site_image(
    site_image_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    site_image_repo = SiteImageRepository(session)
    current_site_image = await site_image_repo.get_by_id(site_image_id)

    if not current_site_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение сайта не найдено",
        )

    # Удаляем изображение
    await file_service.delete_file(current_site_image.image_url)

    # Удаляем запись об изображении
    deleted = await site_image_repo.delete(site_image_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение сайта не найдено",
        )
    return {"message": "Изображение сайта успешно удалено"}
