from fastapi import APIRouter

from api.about_organization.router import router as about_organization_router
from api.delivered_opportunities.router import router as delivered_opportunities_router
from api.parent_section.router import router as parent_section_router
from api.soviet_section.router import router as soviet_section_router
from api.organization_section.router import router as organization_section_router
from api.application_form.router import router as application_form_router
from api.projects.router import router as projects_router
from api.banners.router import router as banners_router
from api.news.router import router as news_router
from api.feedbacks.router import router as feedbacks_router
from api.polls.router import router as polls_router
from api.partners.router import router as partners_router
from api.managers.router import router as managers_router
from api.participants.router import router as participants_router
from api.documents.router import router as documents_router
from api.events.router import router as events_router
from api.site_images.router import router as site_images_router
from api.contacts.router import router as contacts_router
from api.auth.router import router as auth_router
from api.users.router import router as users_router
from api.subscribers.router import router as subscribers_router
from api.email_templates.router import router as email_templates_router
from api.files.router import router as files_router
from api.search.router import router as search_router


router = APIRouter()

about_organization_router.include_router(
    delivered_opportunities_router,
    prefix="/delivered-opportunities",
)
about_organization_router.include_router(
    managers_router,
    prefix="/managers",
)
about_organization_router.include_router(
    documents_router,
    prefix="/documents",
)
# Подключаем маршруты
router.include_router(
    about_organization_router, prefix="/about-organization", tags=["Об организации"]
)

router.include_router(
    parent_section_router, prefix="/parent-section", tags=["Родителям"]
)
soviet_section_router.include_router(
    application_form_router,
    prefix="/application-form",
)
router.include_router(
    soviet_section_router, prefix="/soviet-section", tags=["Управляющим советам"]
)
router.include_router(
    organization_section_router,
    prefix="/organization-section",
    tags=["Образовательным организациям"],
)

router.include_router(partners_router, prefix="/partners", tags=["Партнеры"])


router.include_router(
    projects_router, prefix="/projects", tags=["Проекты (Главная страница)"]
)
router.include_router(
    banners_router, prefix="/banners", tags=["Баннеры (Главная страница)"]
)
router.include_router(news_router, prefix="/news", tags=["Новости (Главная страница)"])
router.include_router(
    feedbacks_router, prefix="/feedbacks", tags=["Вопросы (Главная страница)"]
)
router.include_router(polls_router, prefix="/polls", tags=["Опросы (Главная страница)"])

router.include_router(
    contacts_router, prefix="/contacts", tags=["Контакты (Главная страница)"]
)
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])


router.include_router(site_images_router, prefix="/site-images", tags=["site-images"])
router.include_router(subscribers_router, prefix="/subscribers", tags=["subscribers"])
router.include_router(
    email_templates_router, prefix="/email-templates", tags=["email-templates"]
)
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(search_router, prefix="/search", tags=["search"])
