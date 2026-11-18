"""Safety checks and schema inspection shared by persistence tests."""

from sqlalchemy import inspect
from sqlalchemy.engine import make_url


def validate_test_url(value: str, development_url: str | None = None):
    url = make_url(value)
    if url.drivername != "postgresql+psycopg":
        raise ValueError("TEST_DATABASE_URL must use postgresql+psycopg")
    if not url.database or not url.database.endswith("_test"):
        raise ValueError("Test database name must end in _test")
    if development_url and url.database == make_url(development_url).database:
        raise ValueError("Test and development databases must have different names")
    return url


def schema_signature(connection, schema):
    inspector = inspect(connection)
    signature = {}
    for table in sorted(inspector.get_table_names(schema=schema)):
        columns = [
            (
                column["name"],
                str(column["type"]),
                column["nullable"],
                column.get("default"),
                column.get("identity"),
            )
            for column in inspector.get_columns(table, schema=schema)
        ]
        foreign_keys = [
            (
                fk["name"],
                fk["constrained_columns"],
                fk["referred_table"],
                fk["referred_columns"],
                fk["options"],
            )
            for fk in inspector.get_foreign_keys(table, schema=schema)
        ]
        signature[table] = {
            "columns": columns,
            "pk": inspector.get_pk_constraint(table, schema=schema),
            "fk": foreign_keys,
            "checks": sorted(
                (check["name"], check["sqltext"])
                for check in inspector.get_check_constraints(table, schema=schema)
            ),
            "indexes": inspector.get_indexes(table, schema=schema),
        }
    return signature
