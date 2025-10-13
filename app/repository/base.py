from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from core.models.mixins.id import IdMixin


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession, model: DeclarativeMeta):
        self.session = session
        self.model = model

    async def get_all(self) -> list:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, obj_id: str) -> object:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> object:
        obj = self.model(**kwargs)
        self.session.add(obj)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: str, **kwargs) -> object:
        obj = await self.get_by_id(obj_id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key) and value is not None:
                    setattr(obj, key, value)

            await self.session.commit()
            await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        obj = await self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def find_one(self, **args):
        stmt = select(self.model)
        for key, value in args.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self, **args) -> list:
        stmt = select(self.model)
        for key, value in args.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_active(self) -> list:
        if hasattr(self.model, "is_active"):
            stmt = select(self.model).where(self.model.is_active.is_(True))
        else:
            stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search(self, query: str, search_fields: list[str]) -> list:
        """
        Поиск по указанным полям модели

        :param query: Поисковый запрос
        :param search_fields: Список полей для поиска
        :return: Список найденных объектов
        """
        if not query or not search_fields:
            return []

        # Создаем условие поиска по всем указанным полям
        conditions = []
        for field_name in search_fields:
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                # Для текстовых полей используем ilike (регистронезависимый поиск)
                if hasattr(field, "ilike"):
                    conditions.append(field.ilike(f"%{query}%"))

        if not conditions:
            return []

        # Объединяем условия через OR
        stmt = select(self.model).where(or_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def filter_by(self, **filters) -> list:
        """
        Фильтрация по указанным полям модели

        :param filters: Поля и значения для фильтрации
        :return: Список отфильтрованных объектов
        """
        stmt = select(self.model)

        # Применяем фильтры
        for field_name, value in filters.items():
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                stmt = stmt.where(field == value)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def paginate(self, page: int = 1, size: int = 10) -> tuple[list, int]:
        """
        Пагинация результатов

        :param page: Номер страницы (начиная с 1)
        :param size: Размер страницы
        :return: Кортеж из списка объектов и общего количества объектов
        """
        # Получаем общее количество объектов
        count_stmt = select(func.count()).select_from(self.model)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        # Получаем объекты для текущей страницы
        offset = (page - 1) * size
        stmt = select(self.model).offset(offset).limit(size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def search_with_pagination(
        self, query: str, search_fields: list[str], page: int = 1, size: int = 10
    ) -> tuple[list, int]:
        """
        Поиск с пагинацией по указанным полям модели

        :param query: Поисковый запрос
        :param search_fields: Список полей для поиска
        :param page: Номер страницы (начиная с 1)
        :param size: Размер страницы
        :return: Кортеж из списка объектов и общего количества объектов
        """
        if not query or not search_fields:
            # Если нет запроса или полей для поиска, возвращаем все объекты с пагинацией
            return await self.paginate(page, size)

        # Создаем условие поиска по всем указанным полям
        conditions = []
        for field_name in search_fields:
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                # Для текстовых полей используем ilike (регистронезависимый поиск)
                if hasattr(field, "ilike"):
                    conditions.append(field.ilike(f"%{query}%"))

        if not conditions:
            # Если нет условий поиска, возвращаем все объекты с пагинацией
            return await self.paginate(page, size)

        # Объединяем условия через OR
        stmt = select(self.model).where(or_(*conditions))

        # Получаем общее количество объектов
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        # Получаем объекты для текущей страницы
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def filter_with_pagination(
        self, page: int = 1, size: int = 10, **filters
    ) -> tuple[list, int]:
        """
        Фильтрация с пагинацией по указанным полям модели

        :param page: Номер страницы (начиная с 1)
        :param size: Размер страницы
        :param filters: Поля и значения для фильтрации
        :return: Кортеж из списка объектов и общего количества объектов
        """
        stmt = select(self.model)

        # Применяем фильтры
        for field_name, value in filters.items():
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                stmt = stmt.where(field == value)

        # Получаем общее количество объектов
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        # Получаем объекты для текущей страницы
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total
