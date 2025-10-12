import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from core.models import User
from core.db_helper import db_helper
from api.dependencies import (
    get_current_active_user,
    verify_active_param_access,
    get_current_user_optional,
)
from api.polls.repository import PollRepository, PollAnswerRepository
from api.polls.schemas import (
    PollResponse,
    PollCreate,
    PollUpdate,
    PollAnswerCreate as AnswerCreate,
    PollAnswerResponse as AnswerResponse,
)


router = APIRouter()


@router.get("/", response_model=list[PollResponse])
async def get_polls(
    is_active: bool = Depends(verify_active_param_access),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = PollRepository(session=session)
    polls = await repo.find_all(
        is_active=is_active,
    )
    return polls


@router.get("/{poll_id}/", response_model=PollResponse)
async def get_poll_by_id(
    poll_id: uuid.UUID,
    is_active: bool = Depends(verify_active_param_access),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = PollRepository(session=session)
    poll = await repo.find_one(id=poll_id, is_active=is_active)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    return poll


@router.get("/{poll_id}/answers/", response_model=list[AnswerResponse])
async def get_answers_by_poll_id(
    poll_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    poll_repo = PollRepository(session=session)
    current_poll = await poll_repo.get_by_id(
        obj_id=poll_id,
    )
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    answers_repo = PollAnswerRepository(session=session)
    answers = await answers_repo.find_all(
        poll_id=poll_id,
    )

    return answers


@router.post("/{poll_id}/answers/")
async def answer_to_poll(
    poll_id: uuid.UUID,
    answer_in: AnswerCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    is_active: bool = Depends(verify_active_param_access),
) -> AnswerResponse:

    poll_repo = PollRepository(session=session)
    current_poll = await poll_repo.find_one(id=poll_id, is_active=is_active)
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )
    answers_repo = PollAnswerRepository(session=session)
    answer = await answers_repo.create(
        poll_id=poll_id,
        **answer_in.model_dump(),
    )

    return answer


@router.post("/", response_model=PollResponse)
async def create_poll(
    poll_in: PollCreate,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = PollRepository(session=session)
    poll = await repo.create(**poll_in.model_dump())
    return poll


@router.patch("/{poll_id}/", response_model=PollResponse)
async def update_poll(
    poll_id: uuid.UUID,
    poll_in: PollUpdate,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = PollRepository(session=session)
    current_poll = await repo.get_by_id(obj_id=poll_id)
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    poll = await repo.update(
        obj_id=current_poll.id,
        **poll_in.model_dump(),
    )
    return poll


@router.delete("/{poll_id}/")
async def delete_poll(
    poll_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    repo = PollRepository(session=session)
    current_poll = await repo.get_by_id(obj_id=poll_id)
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    await repo.delete(obj_id=current_poll.id)

    return {"message": "success"}
