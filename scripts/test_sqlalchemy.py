from sqlalchemy import text

from app.db.session import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    version = result.scalar()

    print("✓ SQLAlchemy connection successful")
    print(version)
