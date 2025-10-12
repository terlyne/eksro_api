import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, status, UploadFile

from core.config import settings

# Папки для изображений
IMAGES_FOLDER = "images"
BANNERS_IMAGES_FOLDER = "images/banners"
EVENTS_IMAGES_FOLDER = "images/events"
NEWS_IMAGES_FOLDER = "images/news"
PARTNERS_IMAGES_FOLDER = "images/partners"
PARTNERS_LOGOS_FOLDER = "images/partners/logos"
PROJECTS_IMAGES_FOLDER = "images/projects"
SITE_IMAGES_FOLDER = "images/site"
MANAGERS_IMAGES_FOLDER = "images/managers"
PARTICIPANTS_IMAGES_FOLDER = "images/participants"
FEEDBACKS_IMAGES_FOLDER = "images/feedbacks"

# Папки для документов
DOCUMENTS_FOLDER = "documents"

# Подпапки для конкретных разделов
ABOUT_ORGANIZATION_FOLDER = "about_organization"
DELIVERED_OPPORTUNITIES_FOLDER = "delivered_opportunities"
PARENT_SECTION_FOLDER = "parent_section"
SOVIET_SECTION_FOLDER = "soviet_section"
ORGANIZATION_SECTION_FOLDER = "organization_section"
APPLICATION_FORM_FOLDER = "application_form"


class FileService:
    def __init__(self):
        self.uploads_dir: Path = settings.file.uploads_dir
        self.allowed_image_types: set = settings.file.allowed_image_types
        self.allowed_document_types: set = settings.file.allowed_document_types
        self.max_file_size: int = settings.file.max_file_size

    async def save_file(
        self,
        upload_file: UploadFile,
        subdirectory: str,
    ) -> str:
        # Валидация файла в зависимости от типа
        if subdirectory.startswith(IMAGES_FOLDER):
            await self._validate_image_file(upload_file)
        elif subdirectory.startswith(DOCUMENTS_FOLDER):
            await self._validate_document_file(upload_file)

        # Генерация уникального имени файла
        file_extension = os.path.splitext(upload_file.filename)[1]
        filename = f"{uuid.uuid4().hex}{file_extension}"

        # Создание пути для сохранения файла
        save_path = self.uploads_dir / subdirectory / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Сохранение файла
        async with aiofiles.open(save_path, "wb") as f:
            content = await upload_file.read()
            await f.write(content)

        # Возвращаем относительный путь к файлу
        relative_path = str(Path(subdirectory) / filename)
        return relative_path.replace("\\", "/")

    async def _validate_image_file(
        self,
        upload_file: UploadFile,
    ):
        """Валидация изображения"""
        content = await upload_file.read()
        if len(content) > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл слишком большой",
            )

        if upload_file.content_type not in self.allowed_image_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недопустимый тип файла",
            )

        await upload_file.seek(0)

    async def _validate_document_file(
        self,
        upload_file: UploadFile,
    ):
        """Валидация документа"""
        content = await upload_file.read()
        if len(content) > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл слишком большой",
            )

        if upload_file.content_type not in self.allowed_document_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недопустимый тип файла",
            )

        await upload_file.seek(0)

    async def delete_file(
        self,
        file_path: str,
    ):
        """Удаление файла"""
        absolute_path = self.uploads_dir / file_path
        try:
            if absolute_path.exists():
                absolute_path.unlink()
        except OSError:
            pass


# Создаем экземпляр сервиса
file_service = FileService()
