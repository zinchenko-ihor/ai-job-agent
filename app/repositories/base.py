from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model: type[ModelType]):
        self.session = session
        self.model = model

    def get_by_id(self, object_id: int) -> ModelType | None:
        return self.session.get(self.model, object_id)

    def get_all(self) -> list[ModelType]:
        statement = select(self.model)

        return list(
            self.session.scalars(statement).all()
        )

    def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.flush()

        return obj

    def delete(self, obj: ModelType) -> None:
        self.session.delete(obj)
