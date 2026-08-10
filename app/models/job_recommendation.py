from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.session import Base


class JobRecommendation(Base):

    __tablename__ = "job_recommendations"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )


    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "jobs.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )


    matched_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )


    missing_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


    job = relationship(
        "Job",
        lazy="joined",
    )
