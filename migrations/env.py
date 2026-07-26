from __future__ import annotations

from pathlib import Path
from typing import Any

from alembic import context
from sqlalchemy.engine import Connection

from xianyu_system.worker.account.persistence import account_profiles_table
from xianyu_system.worker.message.persistence import (
    conversation_table,
    delivery_attempt_table,
    message_table,
)

from xianyu_system.core.database import (
    Base,
    build_sqlite_url,
    dispose_database,
    initialize_database,
)

config = context.config
target_metadata = Base.metadata
assert account_profiles_table.metadata is Base.metadata
assert conversation_table.metadata is Base.metadata
assert message_table.metadata is Base.metadata
assert delivery_attempt_table.metadata is Base.metadata


def get_explicit_database_path() -> Path:
    """Return the required explicit Alembic CLI database path."""
    arguments: dict[str, Any] = context.get_x_argument(as_dictionary=True)
    raw_path = arguments.get("database_path")
    if not raw_path:
        raise RuntimeError(
            "Alembic requires a shared connection or an explicit "
            "-x database_path=<path> argument."
        )
    return Path(str(raw_path))


def run_migrations_offline() -> None:
    """Run migrations without opening a database connection."""
    url = build_sqlite_url(get_explicit_database_path())
    context.configure(
        url=str(url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_with_connection(connection: Connection) -> None:
    """Run migrations using an existing SQLAlchemy Connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a shared Connection or explicit project database path."""
    connection = config.attributes.get("connection")
    if isinstance(connection, Connection):
        run_with_connection(connection)
        return

    resources = initialize_database(get_explicit_database_path())
    try:
        with resources.engine.begin() as managed_connection:
            run_with_connection(managed_connection)
    finally:
        dispose_database(resources)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
