from sqlalchemy import inspect

from app.db.session import engine


with engine.connect():
    inspector = inspect(engine)

    print("=== Job Matches Foreign Keys ===")

    for fk in inspector.get_foreign_keys("job_matches"):
        print(
            f" - {fk['constrained_columns']} "
            f"-> {fk['referred_table']}.{fk['referred_columns']}"
        )

    print("\n=== Unique Constraints ===")

    for constraint in inspector.get_unique_constraints("job_matches"):
        print(
            f" - {constraint['name']}: "
            f"{constraint['column_names']}"
        )
