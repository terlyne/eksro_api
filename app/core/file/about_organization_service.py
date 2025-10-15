import json
import uuid
from pathlib import Path
from typing import Optional, Dict, Any

from api.about_organization.schemas import (
    AboutOrganizationResponse,
    AboutOrganizationCreate,
    AboutOrganizationUpdate,
)


class AboutOrganizationJSONService:
    """
    Сервис для хранения и управления информацией об организации в JSON-файле
    """

    def __init__(self, file_path: str = "data/about_organization.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_data(self) -> Optional[Dict[str, Any]]:
        """Чтение данных из JSON-файла"""
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _write_data(self, data: Dict[str, Any]) -> None:
        """Запись данных в JSON-файл"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def get_about_organization(self) -> Optional[AboutOrganizationResponse]:
        """Получить информацию об организации"""
        data = self._read_data()
        if data:
            # Генерируем фиктивный UUID для совместимости со схемой
            data.setdefault("id", str(uuid.uuid4()))
            # Убедимся, что document_url присутствует в данных
            if "document_url" not in data:
                data["document_url"] = None
            return AboutOrganizationResponse(**data)
        return None

    async def create_about_organization(
        self, about_org: AboutOrganizationCreate
    ) -> AboutOrganizationResponse:
        """Создать или обновить информацию об организации"""
        data = about_org.model_dump()
        # Генерируем UUID для совместимости со схемой
        data["id"] = str(uuid.uuid4())
        # Убедимся, что document_url присутствует в данных
        if "document_url" not in data:
            data["document_url"] = None
        self._write_data(data)
        return AboutOrganizationResponse(**data)

    async def update_about_organization(
        self, about_org_update: AboutOrganizationUpdate
    ) -> Optional[AboutOrganizationResponse]:
        """Обновить информацию об организации"""
        current_data = self._read_data()
        if not current_data:
            return None

        # Обновляем только те поля, которые были переданы
        update_data = about_org_update.model_dump(exclude_unset=True)
        current_data.update(update_data)

        # Убедимся, что document_url присутствует в данных
        if "document_url" not in current_data:
            current_data["document_url"] = None

        self._write_data(current_data)
        return AboutOrganizationResponse(**current_data)

    async def delete_about_organization(self) -> bool:
        """Удалить информацию об организации"""
        if self.file_path.exists():
            self.file_path.unlink()
            return True
        return False


# Глобальный экземпляр сервиса
about_organization_service = AboutOrganizationJSONService()
