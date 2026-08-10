from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile
from app.repositories.user_profile import UserProfileRepository


class UserProfileService:
    def __init__(self, session: Session):
        self.repository = UserProfileRepository(session)

    def get_by_telegram_chat_id(
        self,
        telegram_chat_id: str,
    ) -> UserProfile | None:
        return self.repository.get_by_telegram_chat_id(
            telegram_chat_id
        )

    def create_profile(
        self,
        name: str,
        telegram_chat_id: str,
        desired_position: str | None = None,
        location: str | None = None,
        cv_text: str | None = None,
    ) -> UserProfile:

        existing = self.get_by_telegram_chat_id(
            telegram_chat_id
        )

        if existing:
            return existing

        profile = UserProfile(
            name=name,
            telegram_chat_id=telegram_chat_id,
            desired_position=desired_position,
            location=location,
            cv_text=cv_text,
        )

        return self.repository.add(profile)
