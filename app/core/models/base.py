from enum import Enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from core.config import settings


# class SiteSection(str, Enum):
#     HOME: str = "home"
#     ABOUT: str = "about"
#     PARENTS: str = "parents"
#     ORGANIZATIONS: str = "organizations"
#     SOVIETS: str = "soviets"
#     CONTACTS: str = "contacts"
#     PARTNERS: str = "partners"

#     def get_title(self) -> str:
#         titles = {
#             self.HOME: "Главная",
#             self.ABOUT: "Об организации",
#             self.PARENTS: "Для родителей",
#             self.ORGANIZATIONS: "Образовательным организациям",
#             self.SOVIETS: "Управляющим советам",
#             self.CONTACTS: "Контакты",
#             self.PARTNERS: "Партнеры",
#         }
#         return titles[self]


# class ParentSubpage(str, Enum):
#     EDUCATIONAL_PROGRAMS: str = "educational_programs"
#     USEFUL_RESOURCES: str = "useful_resources"
#     THEMATIC_MEETINGS: str = "thematic_meetings"
#     ETIQUETTE_IN_EDUCATION: str = "etiquette_in_education"
#     PROFESSIONAL_LEARNING_TRAJECTORY_CHILD: str = (
#         "professional_learning_trajectory_child"
#     )

#     def get_title(self) -> str:
#         titles = {
#             self.EDUCATIONAL_PROGRAMS: "Образовательные программы",
#             self.USEFUL_RESOURCES: "Полезные ресурсы",
#             self.THEMATIC_MEETINGS: "Тематические встречи",
#             self.ETIQUETTE_IN_EDUCATION: "Проект «Этикет в образовании»",
#             self.PROFESSIONAL_LEARNING_TRAJECTORY_CHILD: "Проект «Профессиональная траектория обучения ребенка»",
#         }
#         return titles[self]


# class OrganizationSubpage(str, Enum):
#     SUPPORT_SOVIETS: str = "supports_soviets"
#     COMPETITION_SUCCESSFUL_YOUTH: str = "competition_successful_youth"
#     EDUCATIONAL_PROGRAMS: str = "educational_programs"
#     THEMATIC_MEETINGS: str = "thematic_meetings"
#     ETIQUETTE_IN_EDUCATION: str = "etiquette_in_education"
#     PROFESSIONAL_LEARNING_TRAJECTORY_CHILD: str = (
#         "professional_learning_trajectory_child"
#     )

#     def get_title(self) -> str:
#         titles = {
#             self.SUPPORT_SOVIETS: "Сопровождение Управляющих советов",
#             self.COMPETITION_SUCCESSFUL_YOUTH: "Конкурс «Успешная молодежь»",
#             self.EDUCATIONAL_PROGRAMS: "Образовательные программы",
#             self.THEMATIC_MEETINGS: "Тематические встречи",
#             self.ETIQUETTE_IN_EDUCATION: "Проект «Этикет в образовании»",
#             self.PROFESSIONAL_LEARNING_TRAJECTORY_CHILD: "Проект «Профессиональная траектория обучения ребенка»",
#         }
#         return titles[self]


# class SovietSubpage(str, Enum):
#     SUPPORT_SOVIETS: str = "supports_soviets"
#     LEARNING: str = "learning"
#     ONLINE_CONFERENCE_CALLS: str = "online_conference_calls"
#     PODCASTS_WITH_SOVIET_TEAMS: str = "podcasts_with_soviets_teams"
#     PROJECTS_BANK: str = "projects_bank"
#     COMPETITION: str = "competition"
#     SOVIET_JOURNAL: str = "soviet_journal"
#     MENTOR_JOURNAL: str = "mentor_journal"

#     def get_title(self) -> str:
#         titles = {
#             self.SUPPORT_SOVIETS: "Сопровождение Управляющих советов",
#             self.LEARNING: "Обучение",
#             self.ONLINE_CONFERENCE_CALLS: "Онлайн селекторные совещания",
#             self.PODCASTS_WITH_SOVIET_TEAMS: "Подкасты с командами УС",
#             self.PROJECTS_BANK: "Банк проектов",
#             self.COMPETITION: "Конкурс",
#             self.SOVIET_JOURNAL: "Журнал Управляющий совет",
#             self.MENTOR_JOURNAL: "Журнал Наставник",
#         }
#         return titles[self]


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
