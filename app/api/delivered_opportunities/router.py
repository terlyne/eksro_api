import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DELIVERED_OPPORTUNITIES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.delivered_opportunities.repository import DeliveredOpportunityRepository
from api.delivered_opportunities.schemas import (
    DeliveredOpportunityCreate,
    DeliveredOpportunityResponse,
    DeliveredOpportunityUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[DeliveredOpportunityResponse])
async def get_delivered_opportunities(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    del_op_repo = DeliveredOpportunityRepository(session)
    delivered_opportunities = await del_op_repo.get_all()
    return delivered_opportunities


@router.get("/{delivered_opportunity_id}/", response_model=DeliveredOpportunityResponse)
async def get_delivered_opportunity_by_id(
    delivered_opportunity_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    del_op_repo = DeliveredOpportunityRepository(session)
    delivered_opportunity = await del_op_repo.get_by_id(delivered_opportunity_id)
    if not delivered_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Доставляемая возможность не найдена",
        )
    return delivered_opportunity


@router.post("/", response_model=DeliveredOpportunityResponse)
async def create_delivered_opportunity(
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    target_group: Annotated[str, Form()],
    responsible_person: Annotated[str, Form()],
    image_file: UploadFile | None = None,  # Файл изображения (опционально)
    contact_phone: Annotated[str | None, Form()] = None,
    contact_email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image_file:
        image_url = await file_service.save_file(
            upload_file=image_file,
            subdirectory=DELIVERED_OPPORTUNITIES_FOLDER,
        )

    # Создаем запись о доставляемой возможности
    del_op_repo = DeliveredOpportunityRepository(session)
    delivered_opportunity = await del_op_repo.create(
        name=name,
        description=description,
        target_group=target_group,
        responsible_person=responsible_person,
        image_url=image_url,
        contact_phone=contact_phone,
        contact_email=contact_email,
    )
    return delivered_opportunity


@router.put("/{delivered_opportunity_id}/", response_model=DeliveredOpportunityResponse)
async def update_delivered_opportunity(
    delivered_opportunity_id: uuid.UUID,
    name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    target_group: Annotated[str | None, Form()] = None,
    responsible_person: Annotated[str | None, Form()] = None,
    image_file: UploadFile | None = None,  # Файл изображения (опционально)
    contact_phone: Annotated[str | None, Form()] = None,
    contact_email: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    del_op_repo = DeliveredOpportunityRepository(session)
    current_delivered_opportunity = await del_op_repo.get_by_id(
        delivered_opportunity_id
    )

    if not current_delivered_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Доставляемая возможность не найдена",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image_file:
        # Удаляем старое изображение
        if current_delivered_opportunity.image_url:
            await file_service.delete_file(current_delivered_opportunity.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image_file,
            subdirectory=DELIVERED_OPPORTUNITIES_FOLDER,
        )

    # Обновляем информацию о доставляемой возможности
    delivered_opportunity = await del_op_repo.update(
        obj_id=delivered_opportunity_id,
        name=name,
        description=description,
        target_group=target_group,
        responsible_person=responsible_person,
        image_url=image_url,
        contact_phone=contact_phone,
        contact_email=contact_email,
    )

    return delivered_opportunity


@router.delete("/{delivered_opportunity_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_delivered_opportunity(
    delivered_opportunity_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    del_op_repo = DeliveredOpportunityRepository(session)
    current_delivered_opportunity = await del_op_repo.get_by_id(
        delivered_opportunity_id
    )

    if not current_delivered_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Доставляемая возможность не найдена",
        )

    # Удаляем изображение
    if current_delivered_opportunity.image_url:
        await file_service.delete_file(current_delivered_opportunity.image_url)

    # Удаляем запись о доставляемой возможности
    deleted = await del_op_repo.delete(delivered_opportunity_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Доставляемая возможность не найдена",
        )
    return {"message": "Доставляемая возможность успешно удалена"}
