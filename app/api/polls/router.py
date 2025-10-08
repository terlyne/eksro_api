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
from api.polls import repository
from api.polls.schemas import (
    PollResponse,
    PollCreate,
    PollUpdate,
    AnswerCreate,
    AnswerResponse,
)


router = APIRouter()


@router.get("/", response_model=list[PollResponse])
async def get_polls(
    is_active: bool = Depends(verify_active_param_access),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    polls = await repository.get_polls(
        session=session,
        is_active=is_active,
    )
    return polls


@router.get("/{poll_id}/", response_model=PollResponse)
async def get_poll_by_id(
    poll_id: uuid.UUID,
    user: User | None = Depends(get_current_user_optional),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    poll = await repository.get_poll_by_id(session=session, poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    if not poll.is_active:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )


@router.get("/{poll_id}/answers/", response_model=list[AnswerResponse])
async def get_answers_by_poll_id(
    poll_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    current_poll = await repository.get_poll_by_id(
        session=session,
        poll_id=poll_id,
    )
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    answers = await repository.get_answers_by_poll(
        session=session,
        current_poll=current_poll,
    )

    return answers


@router.post("/{poll_id}/answers/")
async def answer_to_poll(
    poll_id: uuid.UUID,
    answer_in: AnswerCreate,
    user: User | None = Depends(get_current_user_optional),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> AnswerResponse:
    current_poll = await repository.get_poll_by_id(session=session, poll_id=poll_id)
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    if not current_poll.is_active:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

    answer = await repository.create_answer(
        session=session,
        current_poll=current_poll,
        answer_in=answer_in,
    )

    return answer


@router.post("/", response_model=PollResponse)
async def create_poll(
    poll_in: PollCreate,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    poll = await repository.create_poll(session=session, poll_in=poll_in)
    return poll


@router.patch("/{poll_id}/", response_model=PollResponse)
async def update_poll(
    poll_id: uuid.UUID,
    poll_in: PollUpdate,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    current_poll = await repository.get_poll_by_id(session=session, poll_id=poll_id)
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    poll = await repository.update_poll(
        session=session,
        current_poll=current_poll,
        poll_in=poll_in,
    )
    return poll


@router.delete("/{poll_id}/")
async def delete_poll(
    poll_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    current_poll = await repository.get_poll_by_id(session=session, poll_id=poll_id)
    if not current_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    await repository.delete_poll(session=session, current_poll=current_poll)

    return {"message": "success"}
