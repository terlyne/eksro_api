import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, PARTICIPANTS_IMAGES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.participants.repository import ParticipantRepository
from api.participants.schemas import (
    ParticipantCreate,
    ParticipantResponse,
    ParticipantUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[ParticipantResponse])
async def get_participants(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    participant_repo = ParticipantRepository(session)
    participants = await participant_repo.get_all()
    return participants


@router.get("/{participant_id}/", response_model=ParticipantResponse)
async def get_participant_by_id(
    participant_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    participant_repo = ParticipantRepository(session)
    participant = await participant_repo.get_by_id(participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник не найден",
        )
    return participant


@router.post("/", response_model=ParticipantResponse)
async def create_participant(
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    image: UploadFile | None = None,  # Файл изображения (опционально)
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=PARTICIPANTS_IMAGES_FOLDER,
        )

    participant_repo = ParticipantRepository(session)
    participant = await participant_repo.create(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )
    return participant


@router.put("/{participant_id}/", response_model=ParticipantResponse)
async def update_participant(
    participant_id: uuid.UUID,
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    participant_repo = ParticipantRepository(session)
    current_participant = await participant_repo.get_by_id(participant_id)

    if not current_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_participant.image_url:
            await file_service.delete_file(current_participant.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=PARTICIPANTS_IMAGES_FOLDER,
        )

    # Обновляем информацию об участнике
    participant = await participant_repo.update(
        obj_id=participant_id,
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
    )

    return participant


@router.delete("/{participant_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_participant(
    participant_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    participant_repo = ParticipantRepository(session)
    current_participant = await participant_repo.get_by_id(participant_id)

    if not current_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник не найден",
        )

    # Удаляем изображение
    if current_participant.image_url:
        await file_service.delete_file(current_participant.image_url)

    # Удаляем запись об участнике
    deleted = await participant_repo.delete(participant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник не найден",
        )
    return {"message": "Участник успешно удален"}
