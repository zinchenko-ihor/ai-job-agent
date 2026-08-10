from sqlalchemy import inspect

from app.db.session import engine


with engine.connect():
    inspector = inspect(engine)

    for table in ["skills", "user_skills", "job_skills"]:
        print(f"\n=== {table} ===")

        print("Columns:")

        for column in inspector.get_columns(table):
            print(
                f" - {column['name']} "
                f"({column['type']})"
            )

        print("Foreign Keys:")

        for fk in inspector.get_foreign_keys(table):
            print(
                f" - {fk['constrained_columns']} "
                f"-> {fk['referred_table']}."
                f"{fk['referred_columns']}"
            )

        print("Unique Constraints:")

        for constraint in inspector.get_unique_constraints(table):
            print(
                f" - {constraint['name']}: "
                f"{constraint['column_names']}"
            )
