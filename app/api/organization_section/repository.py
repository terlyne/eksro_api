from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    OrganizationSupportDocument,
    OrganizationSupportEvent,
    OrganizationSupportApplication,
    OrganizationLeader,
    OrganizationNews,
    OrganizationQuestion,
    OrganizationContact,
    OrganizationEducationalProgramDocument,
    OrganizationEducationalProgramContact,
    OrganizationThematicMeetingParticipant,
    OrganizationThematicMeetingEvent,
    OrganizationThematicMeetingContact,
    OrganizationEtiquetteInEducationDocument,
    OrganizationEtiquetteInEducationEvent,
    OrganizationEtiquetteInEducationContact,
    OrganizationProfessionalLearningTrajectoryDocument,
    OrganizationProfessionalLearningTrajectoryParticipant,
    OrganizationProfessionalLearningTrajectoryEvent,
    OrganizationProfessionalLearningTrajectoryContact,
)
from repository.base import BaseRepository


class OrganizationSupportDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationSupportDocument,
        )


class OrganizationSupportEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationSupportEvent,
        )


class OrganizationSupportApplicationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationSupportApplication,
        )


class OrganizationLeaderRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationLeader,
        )


class OrganizationNewsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationNews,
        )


class OrganizationQuestionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationQuestion,
        )


class OrganizationContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationContact,
        )


class OrganizationEducationalProgramDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationEducationalProgramDocument,
        )


class OrganizationEducationalProgramContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationEducationalProgramContact,
        )


class OrganizationThematicMeetingParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationThematicMeetingParticipant,
        )


class OrganizationThematicMeetingEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationThematicMeetingEvent,
        )


class OrganizationThematicMeetingContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationThematicMeetingContact,
        )


class OrganizationEtiquetteInEducationDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationEtiquetteInEducationDocument,
        )


class OrganizationEtiquetteInEducationEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationEtiquetteInEducationEvent,
        )


class OrganizationEtiquetteInEducationContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationEtiquetteInEducationContact,
        )


class OrganizationProfessionalLearningTrajectoryDocumentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationProfessionalLearningTrajectoryDocument,
        )


class OrganizationProfessionalLearningTrajectoryParticipantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationProfessionalLearningTrajectoryParticipant,
        )


class OrganizationProfessionalLearningTrajectoryEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationProfessionalLearningTrajectoryEvent,
        )


class OrganizationProfessionalLearningTrajectoryContactRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=OrganizationProfessionalLearningTrajectoryContact,
        )
