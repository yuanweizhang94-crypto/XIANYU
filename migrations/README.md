# XIANYU migrations

This directory contains the Alembic migration environment for the XIANYU Core database infrastructure.

Current revision: `0001_core_baseline`.

The current SQLAlchemy metadata is empty and there are no business tables. Applying the baseline records Alembic version state only. Application startup initializes SQLite infrastructure but does not automatically run migrations.

Programmatic migrations should share an existing SQLAlchemy `Connection` from the current project Engine through Alembic `Config.attributes`.

Standalone CLI migrations must pass an explicit temporary database path, for example:

```powershell
python -m alembic -c alembic.ini -x database_path=C:\temporary\xianyu.db upgrade head
```

Inspect migration heads and history with:

```powershell
python -m alembic -c alembic.ini heads
python -m alembic -c alembic.ini history
```

Do not test against real operational databases. Future schema changes must be introduced by a newly approved change and a new revision. Do not rewrite historical revisions once applied.
