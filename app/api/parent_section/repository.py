from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    ParentDocument,
    ParentContact,
    ThematicMeetingParticipant,
    ThematicMeetingEvent,
    ThematicMeetingContact,
    EtiquetteInEducationDocument,
    EtiquetteInEducationEvent,
    EtiquetteInEducationContact,
    ProfessionalLearningTrajectoryDocument,
    ProfessionalLearningTrajectoryParticipant,
    ProfessionalLearningTrajectoryEvent,
    ProfessionalLearningTrajectoryContact,
)
from repository.base import BaseRepository


class ParentDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ParentDocument)


class ParentContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ParentContact)


class ThematicMeetingParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ThematicMeetingParticipant)


class ThematicMeetingEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ThematicMeetingEvent)


class ThematicMeetingContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ThematicMeetingContact)


class EtiquetteInEducationDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=EtiquetteInEducationDocument)


class EtiquetteInEducationEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=EtiquetteInEducationEvent)


class EtiquetteInEducationContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=EtiquetteInEducationContact)


class ProfessionalLearningTrajectoryDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ProfessionalLearningTrajectoryDocument)


class ProfessionalLearningTrajectoryParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session, model=ProfessionalLearningTrajectoryParticipant
        )


class ProfessionalLearningTrajectoryEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ProfessionalLearningTrajectoryEvent)


class ProfessionalLearningTrajectoryContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ProfessionalLearningTrajectoryContact)
