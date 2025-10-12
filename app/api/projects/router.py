import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user, verify_active_param_access
from api.projects.repository import ProjectRepository
from api.projects.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[ProjectResponse])
async def get_projects(
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    project_repo = ProjectRepository(session)
    projects = await project_repo.find_all(is_active=is_active)
    return projects


@router.get("/{project_id}/", response_model=ProjectResponse)
async def get_project_by_id(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
):
    project_repo = ProjectRepository(session)
    project = await project_repo.find_one(id=project_id, is_active=is_active)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден",
        )
    return project


@router.post("/", response_model=ProjectResponse)
async def create_project(
    title: Annotated[str, Form()],
    project_url: Annotated[str, Form()],
    keywords: Annotated[list[str], Form()],
    min_text: Annotated[str, Form()],
    theme: Annotated[str, Form()],
    category: Annotated[str, Form()],
    is_active: Annotated[bool, Form()] = True,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем изображение проекта (если загружено)
    image_url = None
    if image:
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    # Создаем запись о проекте
    project_repo = ProjectRepository(session)
    project = await project_repo.create(
        title=title,
        project_url=project_url,
        keywords=keywords,
        min_text=min_text,
        image_url=image_url,
        theme=theme,
        category=category,
        is_active=is_active,
    )
    return project


@router.put("/{project_id}/", response_model=ProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    title: Annotated[str | None, Form()] = None,
    project_url: Annotated[str | None, Form()] = None,
    keywords: Annotated[list[str] | None, Form()] = None,
    min_text: Annotated[str | None, Form()] = None,
    theme: Annotated[str | None, Form()] = None,
    category: Annotated[str | None, Form()] = None,
    is_active: Annotated[bool | None, Form()] = None,
    image: UploadFile | None = None,  # Файл изображения (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    project_repo = ProjectRepository(session)
    current_project = await project_repo.get_by_id(project_id)

    if not current_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден",
        )

    # Если загружено новое изображение, удаляем старое и сохраняем новое
    image_url = None
    if image:
        # Удаляем старое изображение
        if current_project.image_url:
            await file_service.delete_file(current_project.image_url)
        # Сохраняем новое изображение
        image_url = await file_service.save_file(
            upload_file=image,
            subdirectory=DOCUMENTS_FOLDER,  # Используем DOCUMENTS_FOLDER для изображений тоже
        )

    # Обновляем информацию о проекте
    project = await project_repo.update(
        obj_id=project_id,
        title=title,
        project_url=project_url,
        keywords=keywords,
        min_text=min_text,
        image_url=image_url,
        theme=theme,
        category=category,
        is_active=is_active,
    )

    return project


@router.delete("/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    project_repo = ProjectRepository(session)
    current_project = await project_repo.get_by_id(project_id)

    if not current_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден",
        )

    # Удаляем изображение
    if current_project.image_url:
        await file_service.delete_file(current_project.image_url)

    # Удаляем запись о проекте
    deleted = await project_repo.delete(project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден",
        )
    return {"message": "Проект успешно удален"}
