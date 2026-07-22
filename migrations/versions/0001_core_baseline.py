"""Establish the empty XIANYU Core migration baseline."""

from __future__ import annotations

from collections.abc import Sequence

revision: str = "0001_core_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Establish the baseline without creating business schema."""
    pass


def downgrade() -> None:
    """Return to the pre-baseline state without dropping business schema."""
    pass
