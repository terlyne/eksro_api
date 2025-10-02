from fastapi import APIRouter

from api.auth.router import router as auth_router
from api.users.router import router as users_router
from api.banners.router import router as banners_router
from api.events.router import router as events_router
from api.feedbacks.router import router as feedbacks_router
from api.news.router import router as news_router
from api.email_templates.router import router as email_templates_router
from api.partners.router import router as partners_router
from api.polls.router import router as polls_router
from api.projects.router import router as projects_router
from api.subscribers.router import router as subscribers_router
from api.contacts.router import router as contacts_router
from api.documents.router import router as documents_router
from api.site_images.router import router as site_images_router
from api.files.router import router as files_router
from api.search.router import router as search_router


router = APIRouter()
router.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
router.include_router(router=users_router, prefix="/users", tags=["Users"])
router.include_router(router=banners_router, prefix="/banners", tags=["Banners"])
router.include_router(router=events_router, prefix="/events", tags=["Events"])
router.include_router(router=feedbacks_router, prefix="/feedbacks", tags=["Feedbacks"])
router.include_router(router=news_router, prefix="/news", tags=["News"])
router.include_router(
    router=email_templates_router,
    prefix="/email-templates",
    tags=["Email Templates"],
)
router.include_router(router=partners_router, prefix="/partners", tags=["Partners"])
router.include_router(router=polls_router, prefix="/polls", tags=["Polls"])
router.include_router(router=projects_router, prefix="/projects", tags=["Projects"])
router.include_router(
    router=subscribers_router,
    prefix="/subscribers",
    tags=["Subscribers"],
)
router.include_router(router=documents_router, prefix="/documents", tags=["Documents"])
router.include_router(
    router=site_images_router, prefix="/site-images", tags=["Site Images"]
)
router.include_router(router=contacts_router, prefix="/contacts", tags=["Contacts"])
router.include_router(router=files_router, prefix="/files", tags=["Files"])
router.include_router(router=search_router, prefix="/search", tags=["Search"])
