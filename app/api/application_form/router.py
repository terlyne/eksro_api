import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.file.service import file_service, DOCUMENTS_FOLDER
from core.models import User
from core.db_helper import db_helper
from api.dependencies import get_current_active_user
from api.application_form.repository import ApplicationFormRepository
from api.application_form.schemas import (
    ApplicationFormCreate,
    ApplicationFormResponse,
    ApplicationFormUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[ApplicationFormResponse])
async def get_application_forms(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    app_form_repo = ApplicationFormRepository(session)
    application_forms = await app_form_repo.get_all()
    return application_forms


@router.get("/{application_form_id}/", response_model=ApplicationFormResponse)
async def get_application_form_by_id(
    application_form_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    app_form_repo = ApplicationFormRepository(session)
    application_form = await app_form_repo.get_by_id(application_form_id)
    if not application_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Форма заявки не найдена",
        )
    return application_form


@router.post("/", response_model=ApplicationFormResponse)
async def create_application_form(
    application_type: Annotated[
        str, Form()
    ],  # "Консультация", "Вступление в УС", "Другое"
    first_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    last_name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    text: Annotated[str | None, Form()] = None,
    is_processed: Annotated[bool, Form()] = False,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    app_form_repo = ApplicationFormRepository(session)
    application_form = await app_form_repo.create(
        application_type=application_type,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        text=text,
        is_processed=is_processed,
    )
    return application_form


@router.put("/{application_form_id}/", response_model=ApplicationFormResponse)
async def update_application_form(
    application_form_id: uuid.UUID,
    application_type: Annotated[
        str | None, Form()
    ] = None,  # "Консультация", "Вступление в УС", "Другое"
    first_name: Annotated[str | None, Form()] = None,
    last_name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    text: Annotated[str | None, Form()] = None,
    is_processed: Annotated[bool | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    app_form_repo = ApplicationFormRepository(session)
    application_form = await app_form_repo.update(
        obj_id=application_form_id,
        application_type=application_type,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        text=text,
        is_processed=is_processed,
    )

    if not application_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Форма заявки не найдена",
        )

    return application_form


@router.delete("/{application_form_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application_form(
    application_form_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_active_user),
):
    app_form_repo = ApplicationFormRepository(session)
    deleted = await app_form_repo.delete(application_form_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Форма заявки не найдена",
        )
    return {"message": "Форма заявки успешно удалена"}
