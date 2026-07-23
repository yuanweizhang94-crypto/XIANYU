"""Public surface for the local Xianyu account boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from xianyu_system.worker.account.domain import (
    AccountBoundaryError,
    AccountPersistenceError,
    AccountReference,
    DuplicateAccountOwnership,
    InvalidAccountInput,
    InvalidLifecycleTransition,
    Profile,
    ProfileLifecycleStatus,
    ProfileNotFound,
    StaleProfileUpdate,
)

if TYPE_CHECKING:
    from xianyu_system.worker.account.service import AccountService

__all__ = [
    "AccountBoundaryError",
    "AccountPersistenceError",
    "AccountReference",
    "AccountService",
    "DuplicateAccountOwnership",
    "InvalidAccountInput",
    "InvalidLifecycleTransition",
    "Profile",
    "ProfileLifecycleStatus",
    "ProfileNotFound",
    "StaleProfileUpdate",
]


def __getattr__(name: str) -> object:
    if name == "AccountService":
        from xianyu_system.worker.account.service import AccountService

        globals()[name] = AccountService
        return AccountService

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
