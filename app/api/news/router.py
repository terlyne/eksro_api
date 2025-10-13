import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, NEWS_IMAGES_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.news.repository import NewsRepository, NewsTypeRepository
from api.news.schemas import (
    NewsFullResponse,
    NewsPreviewResponse,
    NewsTypeCreate,
    NewsTypeResponse,
    NewsTypeUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[NewsFullResponse])
async def get_news(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_repo = NewsRepository(session)
    news = await news_repo.get_all()
    return news


@router.get("/preview/", response_model=list[NewsPreviewResponse])
async def get_news_preview(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_repo = NewsRepository(session)
    news = await news_repo.get_all()
    news_preview = []
    for news_item in news[skip : skip + limit]:
        news_preview.append(
            NewsPreviewResponse(
                id=news_item.id,
                image_url=news_item.image_url,
                min_text=news_item.min_text,
            )
        )

    return news_preview


@router.post("/", response_model=NewsFullResponse)
async def create_news(
    title: Annotated[str, Form()],
    news_url: Annotated[str, Form()],
    keywords: Annotated[list[str], Form()],
    image: UploadFile,
    min_text: Annotated[str, Form()],
    news_date: Annotated[str, Form()],  # Формат: dd.mm.YYYY
    type_id: Annotated[uuid.UUID, Form()],
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Сохраняем изображение новости
    image_url = await file_service.save_file(
        upload_file=image,
        subdirectory=NEWS_IMAGES_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
    )

    # Создаем запись о новости
    news_repo = NewsRepository(session)
    news = await news_repo.create(
        title=title,
        news_url=news_url,
        keywords=keywords,
        image_url=image_url,
        min_text=min_text,
        news_date=news_date,
        type_id=type_id,
    )

    return news


@router.patch("/{news_id}/", response_model=NewsFullResponse)
async def update_news(
    news_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    news_url: Annotated[str | None, Form()] = None,
    keywords: Annotated[list[str] | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    min_text: Annotated[str | None, Form()] = None,
    news_date: Annotated[str | None, Form()] = None,  # Формат: dd.mm.YYYY
    type_id: Annotated[uuid.UUID | None, Form()] = None,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_repo = NewsRepository(session)
    current_news = await news_repo.get_by_id(news_id)

    if not current_news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость не найдена",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        await file_service.delete_file(current_news.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=NEWS_IMAGES_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    # Обновляем информацию о новости
    news = await news_repo.update(
        obj_id=news_id,
        title=title,
        news_url=news_url,
        keywords=keywords,
        image_url=image_url,
        min_text=min_text,
        news_date=news_date,
        type_id=type_id,
    )

    return news


@router.delete("/{news_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
    news_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_repo = NewsRepository(session)
    current_news = await news_repo.get_by_id(news_id)

    if not current_news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость не найдена",
        )

    # Удаляем изображение
    await file_service.delete_file(current_news.image_url)

    # Удаляем запись о новости
    deleted = await news_repo.delete(news_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость не найдена",
        )
    return {"message": "Новость успешно удалена"}


# ====================
# ====================
# ====================
# ====================
# ====================
# ====================


@router.get("/types/", response_model=list[NewsTypeResponse])
async def get_news_types(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_type_repo = NewsTypeRepository(session)
    return await news_type_repo.get_all()


@router.get("/types/{type_id}/", response_model=NewsTypeResponse)
async def get_news_type_by_id(
    type_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_type_repo = NewsTypeRepository(session)
    news_type = await news_type_repo.get_by_id(type_id)
    if not news_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип новости не найден",
        )

    return news_type


@router.post("/types/", response_model=NewsTypeResponse)
async def create_news_type(
    type_in: NewsTypeCreate,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_type_repo = NewsTypeRepository(session)
    news_type = await news_type_repo.create(**type_in.model_dump())
    if not news_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тип новости уже существует",
        )
    return news_type


@router.patch("/types/{type_id}/", response_model=NewsTypeResponse)
async def update_news_type(
    type_id: uuid.UUID,
    type_in: NewsTypeUpdate,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_type_repo = NewsTypeRepository(session)
    news_type = await news_type_repo.update(
        type_id, **type_in.model_dump(exclude_unset=True)
    )
    if not news_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип новости не найден",
        )

    return news_type


@router.delete("/types/{type_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news_type(
    type_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    news_type_repo = NewsTypeRepository(session)
    current_news_type = await news_type_repo.get_by_id(type_id)

    if not current_news_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип новости не найден",
        )

    # Проверяем, есть ли новости с этим типом
    news_repo = NewsRepository(session)
    news_with_type = await news_repo.find_all(type_id=type_id)

    if news_with_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно удалить тип новости. Существуют новости с этим типом",
        )

    # Удаляем тип новости
    deleted = await news_type_repo.delete(type_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип новости не найден",
        )
    return {"message": "Тип новости успешно удален"}
