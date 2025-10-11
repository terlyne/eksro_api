from sqlalchemy import select


class BaseRepository:

    model = None

    async def find_one(cls, **args):
        stmt = select(cls.model)
