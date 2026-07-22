"""${message}."""

from __future__ import annotations

from collections.abc import Sequence

revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """Apply this migration."""
    pass


def downgrade() -> None:
    """Revert this migration."""
    pass
