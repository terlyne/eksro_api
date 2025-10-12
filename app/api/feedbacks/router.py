import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, FEEDBACKS_IMAGES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user, verify_active_param_access
from api.feedbacks.repository import FeedbackRepository
from api.feedbacks.schemas import (
    FeedbackCreate,
    FeedbackResponse,
    FeedbackUpdate,
    FeedbackAnswer,
)


router = APIRouter()


@router.get("/", response_model=list[FeedbackResponse])
async def get_feedbacks(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    feedback_repo = FeedbackRepository(session)
    feedbacks = await feedback_repo.get_all()
    return feedbacks[skip : skip + limit]


@router.get("/{feedback_id}/", response_model=FeedbackResponse)
async def get_feedback_by_id(
    feedback_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    feedback_repo = FeedbackRepository(session)
    feedback = await feedback_repo.get_by_id(feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обратная связь не найдена",
        )
    return feedback


@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    site_section: Annotated[str, Form()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    message: Annotated[str, Form()],
    subpage: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Сохраняем изображение (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=FEEDBACKS_IMAGES_FOLDER,
        )

    # Создаем запись об обратной связи
    feedback_repo = FeedbackRepository(session)
    feedback = await feedback_repo.create(
        site_section=site_section,
        subpage=subpage,
        name=name,
        email=email,
        message=message,
        phone=phone,
        image_url=image_url,
    )
    return feedback


@router.put("/{feedback_id}/", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: uuid.UUID,
    site_section: Annotated[str | None, Form()] = None,
    subpage: Annotated[str | None, Form()] = None,
    name: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    message: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    feedback_repo = FeedbackRepository(session)
    current_feedback = await feedback_repo.get_by_id(feedback_id)

    if not current_feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обратная связь не найдена",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_feedback.image_url:
            await file_service.delete_file(current_feedback.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=FEEDBACKS_IMAGES_FOLDER,
        )

    # Обновляем информацию об обратной связи
    feedback = await feedback_repo.update(
        obj_id=feedback_id,
        site_section=site_section,
        subpage=subpage,
        name=name,
        email=email,
        message=message,
        phone=phone,
        image_url=image_url,
    )

    return feedback


@router.delete("/{feedback_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(
    feedback_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    feedback_repo = FeedbackRepository(session)
    current_feedback = await feedback_repo.get_by_id(feedback_id)

    if not current_feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обратная связь не найдена",
        )

    # Удаляем изображение
    if current_feedback.image_url:
        await file_service.delete_file(current_feedback.image_url)

    # Удаляем запись об обратной связи
    deleted = await feedback_repo.delete(feedback_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обратная связь не найдена",
        )
    return {"message": "Обратная связь успешно удалена"}


@router.post("/{feedback_id}/answer/", response_model=FeedbackResponse)
async def answer_feedback(
    feedback_id: uuid.UUID,
    feedback_answer: FeedbackAnswer,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    feedback_repo = FeedbackRepository(session)
    current_feedback = await feedback_repo.get_by_id(feedback_id)

    if not current_feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обратная связь не найдена",
        )

    # Обновляем информацию об обратной связи с ответом
    feedback = await feedback_repo.update(
        obj_id=feedback_id,
        response=feedback_answer.response,
        is_answered=True,
    )

    return feedback
