import uuid

from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Poll, PollAnswer
from api.polls.schemas import PollCreate, PollUpdate, AnswerCreate


async def get_polls(
    session: AsyncSession,
    is_active: bool = True,
) -> list[Poll]:
    if is_active:
        stmt = (
            select(Poll).where(Poll.is_active == True).order_by(desc(Poll.created_at))
        )
    else:
        stmt = select(Poll).order_by(desc(Poll.created_at))

    result = await session.scalars(stmt)
    return list(result.unique().all())


async def get_answers_by_poll(
    session: AsyncSession,
    current_poll: Poll,
) -> list[PollAnswer]:
    stmt = select(PollAnswer).where(PollAnswer.poll_id == current_poll.id)
    result = await session.scalars(stmt)

    return list(result.all())


async def get_poll_by_id(
    session: AsyncSession,
    poll_id: uuid.UUID,
) -> Poll | None:
    stmt = select(Poll).where(Poll.id == poll_id).options(selectinload(Poll.answers))
    poll = await session.scalar(stmt)
    return poll


async def update_poll(
    session: AsyncSession,
    current_poll: Poll,
    poll_in: PollUpdate,
) -> Poll:
    update_data = poll_in.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(current_poll, field, value)

    await session.commit()

    return current_poll


async def create_poll(
    session: AsyncSession,
    poll_in: PollCreate,
) -> Poll:
    poll = Poll(**poll_in.model_dump())
    session.add(poll)

    await session.commit()
    stmt = select(Poll).where(Poll.id == poll.id).options(selectinload(Poll.answers))
    poll_with_answers = await session.scalar(stmt)

    return poll_with_answers


async def create_answer(
    session: AsyncSession,
    current_poll: Poll,
    answer_in: AnswerCreate,
) -> PollAnswer:
    answer = PollAnswer(**answer_in.model_dump(), poll_id=current_poll.id)
    session.add(answer)
    await session.commit()
    await session.refresh(answer)

    return answer


async def delete_poll(
    session: AsyncSession,
    current_poll: Poll,
):
    await session.delete(current_poll)
    await session.commit()
