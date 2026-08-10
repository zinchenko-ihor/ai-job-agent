import json
from pathlib import Path
from typing import Any


class ResumeProfileRepository:
    """
    Stores the analyzed resume profile for a Telegram user.

    MVP implementation:
    - one profile per user
    - stored as JSON
    - overwritten when a new CV is analyzed
    """

    BASE_DIR = Path("storage/profiles")

    def __init__(self):
        self.BASE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _profile_path(self, user_id: int) -> Path:
        user_dir = self.BASE_DIR / str(user_id)

        user_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return user_dir / "profile.json"

    def save(
        self,
        user_id: int,
        profile: dict[str, Any],
    ) -> Path:

        path = self._profile_path(user_id)

        path.write_text(
            json.dumps(
                profile,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def get(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:

        path = self._profile_path(user_id)

        if not path.exists():
            return None

        return json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )
