from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import URL, create_engine, event
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ALEMBIC_CONFIG_PATH = REPOSITORY_ROOT / "alembic.ini"
MIGRATIONS_PATH = REPOSITORY_ROOT / "migrations"
BASELINE_REVISION = "0001_core_baseline"


class Base(DeclarativeBase):
    """Declarative metadata boundary for future approved Core models."""


@dataclass(frozen=True, slots=True)
class DatabaseResources:
    """Database resources owned by one XIANYU application instance."""

    path: Path
    engine: Engine
    session_factory: sessionmaker[Session]


def resolve_database_path(database_path: Path) -> Path:
    """Resolve a SQLite path without creating files or directories."""
    return database_path.expanduser().resolve(strict=False)


def build_sqlite_url(database_path: Path) -> URL:
    """Build a SQLAlchemy SQLite URL without string-concatenating paths."""
    resolved_path = resolve_database_path(database_path)
    return URL.create(
        drivername="sqlite+pysqlite",
        database=str(resolved_path),
    )


def configure_sqlite_pragmas(engine: Engine) -> None:
    """Register SQLite PRAGMA setup for connections from one Engine."""

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection: Any, _connection_record: Any) -> None:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA busy_timeout=5000")
        finally:
            cursor.close()


def create_database_engine(database_path: Path) -> Engine:
    """Create a synchronous SQLAlchemy Engine without opening a connection."""
    engine = create_engine(
        build_sqlite_url(database_path),
        connect_args={"check_same_thread": False},
        echo=False,
        pool_pre_ping=True,
    )
    configure_sqlite_pragmas(engine)
    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create the unified synchronous Session factory."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def initialize_database(database_path: Path) -> DatabaseResources:
    """Initialize SQLite infrastructure and verify WAL connectivity."""
    resolved_path = resolve_database_path(database_path)
    if resolved_path.exists() and resolved_path.is_dir():
        raise ValueError(f"Database path points to an existing directory: {resolved_path}")

    engine: Engine | None = None
    try:
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_database_engine(resolved_path)
        session_factory = create_session_factory(engine)
        with engine.connect() as connection:
            journal_mode = str(connection.exec_driver_sql("PRAGMA journal_mode").scalar_one())
            if journal_mode.lower() != "wal":
                raise RuntimeError(f"SQLite WAL mode was not enabled: {journal_mode}")
            if connection.exec_driver_sql("SELECT 1").scalar_one() != 1:
                raise RuntimeError("SQLite connectivity validation failed")
        return DatabaseResources(
            path=resolved_path,
            engine=engine,
            session_factory=session_factory,
        )
    except Exception:
        if engine is not None:
            engine.dispose()
        raise


@contextmanager
def open_session(resources: DatabaseResources) -> Iterator[Session]:
    """Open a Session and always close it without auto-commit."""
    session = resources.session_factory()
    try:
        yield session
    finally:
        session.close()


def dispose_database(resources: DatabaseResources) -> None:
    """Dispose the Engine owned by the provided resources."""
    resources.engine.dispose()


def build_alembic_config(
    *,
    connection: Connection | None = None,
) -> Config:
    """Build an Alembic Config without opening a database connection."""
    config = Config(str(ALEMBIC_CONFIG_PATH))
    config.set_main_option("script_location", str(MIGRATIONS_PATH))
    if connection is not None:
        config.attributes["connection"] = connection
    return config


def upgrade_database(
    resources: DatabaseResources,
    revision: str = "head",
) -> None:
    """Upgrade the provided database resources using a shared Connection."""
    with resources.engine.begin() as connection:
        config = build_alembic_config(connection=connection)
        command.upgrade(config, revision)


def downgrade_database(
    resources: DatabaseResources,
    revision: str = "base",
) -> None:
    """Downgrade the provided database resources using a shared Connection."""
    with resources.engine.begin() as connection:
        config = build_alembic_config(connection=connection)
        command.downgrade(config, revision)


def get_current_revision(
    resources: DatabaseResources,
) -> str | None:
    """Return the current Alembic revision without mutating the database."""
    with resources.engine.connect() as connection:
        migration_context = MigrationContext.configure(connection)
        return migration_context.get_current_revision()


__all__ = [
    "ALEMBIC_CONFIG_PATH",
    "BASELINE_REVISION",
    "MIGRATIONS_PATH",
    "Base",
    "DatabaseResources",
    "build_alembic_config",
    "build_sqlite_url",
    "create_database_engine",
    "create_session_factory",
    "dispose_database",
    "downgrade_database",
    "get_current_revision",
    "initialize_database",
    "open_session",
    "resolve_database_path",
    "upgrade_database",
]
