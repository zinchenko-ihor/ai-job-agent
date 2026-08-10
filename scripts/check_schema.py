from sqlalchemy import inspect

from app.db.session import engine


with engine.connect():
    inspector = inspect(engine)

    print("=== Tables ===")

    for table in inspector.get_table_names():
        print(f" - {table}")

    print("\n=== Jobs foreign keys ===")

    for fk in inspector.get_foreign_keys("jobs"):
        print(
            f" - {fk['constrained_columns']} "
            f"-> {fk['referred_table']}.{fk['referred_columns']}"
        )
