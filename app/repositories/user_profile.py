from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile
from app.repositories.base import BaseRepository


class UserProfileRepository(BaseRepository[UserProfile]):
    def __init__(self, session: Session):
        super().__init__(session, UserProfile)

    def get_by_telegram_chat_id(
        self,
        telegram_chat_id: str,
    ) -> UserProfile | None:

        statement = select(UserProfile).where(
            UserProfile.telegram_chat_id == telegram_chat_id
        )

        return self.session.scalar(statement)
