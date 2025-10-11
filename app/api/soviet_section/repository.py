from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    SovietSupportDocument,
    SovietSupportEvent,
    SovietSupportApplication,
    SovietLeader,
    SovietNews,
    SovietQuestion,
    SovietContact,
    LearningDocument,
    LearningEvent,
    LearningApplication,
    LearningNews,
    LearningQuestion,
    LearningContact,
    OnlineConferenceRegulation,
    OnlineConferenceParticipant,
    OnlineConferenceNews,
    OnlineConferenceQuestion,
    OnlineConferenceContact,
    PodcastApplication,
    PodcastParticipant,
    PodcastNews,
    PodcastContact,
    ProjectNews,
    ProjectReport,
    CompetitionDocument,
    CompetitionContact,
    JournalNews,
    JournalContact,
)
from repository.base import BaseRepository


class SovietSupportDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietSupportDocument)


class SovietSupportEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietSupportEvent)


class SovietSupportApplicationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietSupportApplication)


class SovietLeaderRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietLeader)


class SovietNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietNews)


class SovietQuestionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietQuestion)


class SovietContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=SovietContact)


class LearningDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=LearningDocument)


class LearningEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=LearningEvent)


class LearningApplicationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=LearningApplication)


class LearningNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=LearningNews)


class LearningQuestionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=LearningQuestion)


class LearningContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=LearningContact)


class OnlineConferenceRegulationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=OnlineConferenceRegulation)


class OnlineConferenceParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=OnlineConferenceParticipant)


class OnlineConferenceNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=OnlineConferenceNews)


class OnlineConferenceQuestionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=OnlineConferenceQuestion)


class OnlineConferenceContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=OnlineConferenceContact)


class PodcastApplicationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=PodcastApplication)


class PodcastParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=PodcastParticipant)


class PodcastNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=PodcastNews)


class PodcastContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=PodcastContact)


class ProjectNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ProjectNews)


class ProjectReportRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ProjectReport)


class CompetitionDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=CompetitionDocument)


class CompetitionContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=CompetitionContact)


class JournalNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=JournalNews)


class JournalContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=JournalContact)
