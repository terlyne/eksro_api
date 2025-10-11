import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, BANNERS_IMAGES_FOLDER
from core.models import User, Banner
from core.db_helper import db_helper
from api.dependencies import get_current_active_user, verify_active_param_access
from api.banners.schemas import BannerResponse, BannerCreate, BannerUpdate
from api.banners.repository import BannerRepository


router = APIRouter()


@router.post("/", response_model=BannerResponse)
async def create_banner(
    image: UploadFile,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    count_order: Annotated[int, Form(gt=0)],
    is_active: Annotated[bool, Form()] = True,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Проверка уникальности позиции баннера (count_order)
    banner_repo = BannerRepository(session)
    existing_banners = await banner_repo.get_all()
    if any(b.count_order == count_order for b in existing_banners):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Баннер с такой позицией уже задан",
        )
    # Сохраняем изображение баннера
    image_url = await file_service.save_file(
        upload_file=image,
        subdirectory=BANNERS_IMAGES_FOLDER,
    )

    banner = await banner_repo.create(
        image_url=image_url,
        title=title,
        description=description,
        is_active=is_active,
        count_order=count_order,
    )

    return banner


@router.get("/", response_model=list[BannerResponse])
async def get_banners(
    is_active: bool = Depends(verify_active_param_access),
    skip: int = 0,
    limit: int = 6,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    banner_repo = BannerRepository(session)
    banners = await banner_repo.get_all()

    # Фильтруем по активности
    if is_active:
        banners = [b for b in banners if b.is_active]

    # Применяем пагинацию
    banners = banners[skip : skip + limit]

    return banners


@router.get("/{banner_id}/", response_model=BannerResponse)
async def get_banner_by_id(
    banner_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    banner_repo = BannerRepository(session)
    banner = await banner_repo.get_by_id(banner_id)
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found",
        )

    return banner


@router.patch("/{banner_id}/", response_model=BannerResponse)
async def update_banner(
    banner_id: uuid.UUID,
    image: UploadFile | None = None,
    title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    count_order: Annotated[int | None, Form(gt=0)] = None,
    is_active: Annotated[bool | None, Form()] = None,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    banner_repo = BannerRepository(session)
    current_banner = await banner_repo.get_by_id(banner_id)
    if not current_banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found",
        )

    image_url = None

    if image:
        await file_service.delete_file(current_banner.image_url)
        image_url = await file_service.save_file(image, BANNERS_IMAGES_FOLDER)

    banner = await banner_repo.update(
        obj_id=banner_id,
        image_url=image_url,
        title=title,
        description=description,
        count_order=count_order,
        is_active=is_active,
    )

    return banner


@router.delete("/{banner_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banner(
    banner_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    banner_repo = BannerRepository(session)
    current_banner = await banner_repo.get_by_id(banner_id)
    if not current_banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found",
        )

    await file_service.delete_file(current_banner.image_url)
    deleted = await banner_repo.delete(banner_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found",
        )
    return {"message": "success"}
