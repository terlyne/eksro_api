import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, PARTNERS_LOGOS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.partners.repository import PartnerRepository
from api.partners.schemas import (
    PartnerCreate,
    PartnerResponse,
    PartnerUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[PartnerResponse])
async def get_partners(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    partner_repo = PartnerRepository(session)
    partners = await partner_repo.get_all()
    return partners


@router.get("/{partner_id}/", response_model=PartnerResponse)
async def get_partner_by_id(
    partner_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    partner_repo = PartnerRepository(session)
    partner = await partner_repo.get_by_id(partner_id)
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Партнер не найден",
        )
    return partner


@router.post("/", response_model=PartnerResponse)
async def create_partner(
    partner_name: Annotated[str, Form()],
    count_order: Annotated[int, Form(gt=0)],
    logo: UploadFile,  # Файл логотипа
    partner_url: Annotated[
        str | None, Form()
    ] = None,  # URL сайта партнера (опционально)
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Проверка уникальности позиции партнера (count_order)
    partner_repo = PartnerRepository(session)
    existing_partners = await partner_repo.get_all()
    if any(p.count_order == count_order for p in existing_partners):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Партнер с такой позицией уже задан",
        )
    # Сохраняем логотип партнера
    logo_url = await file_service.save_file(
        upload_file=logo,
        subdirectory=PARTNERS_LOGOS_FOLDER,
    )

    partner = await partner_repo.create(
        partner_name=partner_name,
        partner_url=partner_url,
        logo_url=logo_url,
        count_order=count_order,
    )

    return partner


@router.put("/{partner_id}/", response_model=PartnerResponse)
async def update_partner(
    partner_id: uuid.UUID,
    partner_name: Annotated[str | None, Form()] = None,
    count_order: Annotated[int | None, Form(gt=0)] = None,
    logo: UploadFile | None = None,  # Файл логотипа (опционально)
    partner_url: Annotated[
        str | None, Form()
    ] = None,  # URL сайта партнера (опционально)
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    partner_repo = PartnerRepository(session)
    current_partner = await partner_repo.get_by_id(partner_id)

    if not current_partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Партнер не найден",
        )

    # Проверка уникальности позиции партнера (count_order)
    if count_order:
        existing_partners = await partner_repo.get_all()
        if any(
            p.count_order == count_order and p.id != partner_id
            for p in existing_partners
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Партнер с такой позицией уже задан",
            )

    # Если загружен новый логотип, удаляем старый и сохраняем новый
    logo_url = None
    if logo:
        # Удаляем старый логотип
        await file_service.delete_file(current_partner.logo_url)
        # Сохраняем новый логотип
        logo_url = await file_service.save_file(
            upload_file=logo,
            subdirectory=PARTNERS_LOGOS_FOLDER,
        )

    # Обновляем информацию о партнере
    partner = await partner_repo.update(
        obj_id=partner_id,
        partner_name=partner_name,
        partner_url=partner_url,
        logo_url=logo_url,
        count_order=count_order,
    )

    return partner


@router.delete("/{partner_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_partner(
    partner_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    partner_repo = PartnerRepository(session)
    current_partner = await partner_repo.get_by_id(partner_id)

    if not current_partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Партнер не найден",
        )

    # Удаляем логотип
    await file_service.delete_file(current_partner.logo_url)

    # Удаляем запись о партнере
    deleted = await partner_repo.delete(partner_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Партнер не найден",
        )
    return {"message": "Партнер успешно удален"}
