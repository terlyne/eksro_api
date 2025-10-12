import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.documents.repository import DocumentRepository
from api.documents.schemas import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[DocumentResponse])
async def get_documents(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    doc_repo = DocumentRepository(session)
    documents = await doc_repo.get_all()
    return documents


@router.get("/{document_id}/", response_model=DocumentResponse)
async def get_document_by_id(
    document_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    doc_repo = DocumentRepository(session)
    document = await doc_repo.get_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )
    return document


@router.post("/", response_model=DocumentResponse)
async def create_document(
    site_section: Annotated[str, Form()],
    title: Annotated[str, Form()],
    file: UploadFile,  # Файл документа
    subpage: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    # Сохраняем файл документа
    file_url = await file_service.save_file(
        upload_file=file,
        subdirectory=DOCUMENTS_FOLDER,
    )

    # Создаем запись о документе
    doc_repo = DocumentRepository(session)
    document = await doc_repo.create(
        site_section=site_section,
        subpage=subpage,
        title=title,
        file_url=file_url,
    )
    return document


@router.put("/{document_id}/", response_model=DocumentResponse)
async def update_document(
    document_id: uuid.UUID,
    site_section: Annotated[str | None, Form()] = None,
    subpage: Annotated[str | None, Form()] = None,
    title: Annotated[str | None, Form()] = None,
    file: UploadFile | None = None,  # Файл документа (опционально)
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    doc_repo = DocumentRepository(session)
    current_document = await doc_repo.get_by_id(document_id)

    if not current_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )

    # Если загружен новый файл, удаляем старый и сохраняем новый
    file_url = None
    if file:
        # Удаляем старый файл
        await file_service.delete_file(current_document.file_url)
        # Сохраняем новый файл
        file_url = await file_service.save_file(
            upload_file=file,
            subdirectory=DOCUMENTS_FOLDER,
        )

    # Обновляем информацию о документе
    document = await doc_repo.update(
        obj_id=document_id,
        site_section=site_section,
        subpage=subpage,
        title=title,
        file_url=file_url,
    )

    return document


@router.delete("/{document_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    doc_repo = DocumentRepository(session)
    current_document = await doc_repo.get_by_id(document_id)

    if not current_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )

    # Удаляем файл
    await file_service.delete_file(current_document.file_url)

    # Удаляем запись о документе
    deleted = await doc_repo.delete(document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )
    return {"message": "Документ успешно удален"}
