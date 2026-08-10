from app.db.session import SessionLocal
from app.services.matching import MatchingService


db = SessionLocal()


service = MatchingService(db)


match = service.calculate_match(
    user_profile_id=1,
    job_id=1
)


print(
    "Score:",
    match.match_score
)

print(
    "Recommended:",
    match.is_recommended
)


db.close()
