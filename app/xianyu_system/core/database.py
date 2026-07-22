from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import URL, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


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


__all__ = [
    "Base",
    "DatabaseResources",
    "build_sqlite_url",
    "create_database_engine",
    "create_session_factory",
    "dispose_database",
    "initialize_database",
    "open_session",
    "resolve_database_path",
]
