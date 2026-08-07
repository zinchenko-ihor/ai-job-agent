from sqlalchemy import inspect

from app.db.session import engine


with engine.connect():
    inspector = inspect(engine)

    print("Database tables:")

    for table in inspector.get_table_names():
        print(f" - {table}")
