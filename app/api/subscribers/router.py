import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.subscribers.repository import SubscriberRepository
from api.subscribers.schemas import (
    SubscriberCreate,
    SubscriberResponse,
    SubscriberUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[SubscriberResponse])
async def get_subscribers(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    subscriber_repo = SubscriberRepository(session)
    subscribers = await subscriber_repo.get_all()
    return subscribers


@router.get("/{subscriber_id}/", response_model=SubscriberResponse)
async def get_subscriber_by_id(
    subscriber_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    subscriber_repo = SubscriberRepository(session)
    subscriber = await subscriber_repo.get_by_id(subscriber_id)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписчик не найден",
        )
    return subscriber


@router.post("/", response_model=SubscriberResponse)
async def create_subscriber(
    email: Annotated[str, Form()],
    type_id: Annotated[uuid.UUID, Form()],
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    subscriber_repo = SubscriberRepository(session)
    subscriber = await subscriber_repo.create(
        email=email,
        type_id=type_id,
    )
    return subscriber


@router.put("/{subscriber_id}/", response_model=SubscriberResponse)
async def update_subscriber(
    subscriber_id: uuid.UUID,
    email: Annotated[str | None, Form()] = None,
    type_id: Annotated[uuid.UUID | None, Form()] = None,
    is_confirmed: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    subscriber_repo = SubscriberRepository(session)
    subscriber = await subscriber_repo.update(
        obj_id=subscriber_id,
        email=email,
        type_id=type_id,
        is_confirmed=is_confirmed,
    )

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписчик не найден",
        )

    return subscriber


@router.delete("/{subscriber_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscriber(
    subscriber_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    subscriber_repo = SubscriberRepository(session)
    deleted = await subscriber_repo.delete(subscriber_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписчик не найден",
        )
    return {"message": "Подписчик успешно удален"}
