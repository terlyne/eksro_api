import uuid
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, UploadFile, Form, Depends

from core.models.user import User
from core.db_helper import db_helper
from core.file.service import file_service, SITE_IMAGES_FOLDER
from api.dependencies import get_current_active_user
from api.site_images.schemas import SiteImageResponse
from api.site_images import repository


router = APIRouter()


@router.post("/", response_model=SiteImageResponse)
async def create_site_image(
    name: Annotated[str, Form()],
    image: UploadFile,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    image_url = await file_service.save_file(image, SITE_IMAGES_FOLDER)
    site_image = await repository.create_site_image(
        session=session, name=name, image_url=image_url
    )
    return site_image


@router.get("/", response_model=list[SiteImageResponse])
async def get_site_images(
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    site_images = await repository.get_site_images(session=session)
    return site_images


@router.delete("/{site_image_id}/")
async def delete_site_image(
    site_image_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    current_site_image = await repository.get_site_image_by_id(
        session=session,
        site_image_id=site_image_id,
    )
    if not current_site_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site image not found",
        )

    return {"message": "success"}
