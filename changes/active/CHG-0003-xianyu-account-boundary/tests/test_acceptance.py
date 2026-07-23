from __future__ import annotations

import ast
import json
from pathlib import Path
from uuid import UUID

import pytest
import yaml
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from xianyu_system.core.database import (
    dispose_database,
    get_current_revision,
    initialize_database,
    upgrade_database,
)

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"
CHG_0002 = ARCHIVE / "CHG-0002-core-application"
CHG_0003 = ACTIVE / "CHG-0003-xianyu-account-boundary"
CORE_IDS = {"CAP-CORE-CONFIG", "CAP-CORE-DATABASE", "CAP-HEALTH-MONITOR"}
ACCOUNT_REVISION = "0002_xianyu_account_boundary"
ACCOUNT_TABLE = "xianyu_account_profiles"
ACCOUNT_IMPLEMENTATION_PATHS = [
    "app/xianyu_system/worker/account/__init__.py",
    "app/xianyu_system/worker/account/domain.py",
    "app/xianyu_system/worker/account/service.py",
    "app/xianyu_system/worker/account/persistence.py",
    "migrations/versions/0002_xianyu_account_boundary.py",
]
ACCOUNT_TEST_PATHS = [
    "tests/unit/test_account_domain.py",
    "tests/unit/test_account_service.py",
    "tests/unit/test_import_safety.py",
    "tests/contract/test_account_persistence.py",
    "tests/contract/test_account_security.py",
    "tests/contract/test_migrations.py",
    "tests/contract/test_core_runtime.py",
    "tests/contract/test_capability_registry.py",
    "changes/active/CHG-0003-xianyu-account-boundary/tests/test_acceptance.py",
]


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(
        (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8")
    )
    return {item["id"]: item for item in registry["capabilities"]}


def test_chg_0002_is_archived_with_historical_tests_preserved() -> None:
    assert not (ACTIVE / "CHG-0002-core-application").exists()
    assert CHG_0002.is_dir()
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0002 / name) == "ARCHIVED"
    assert (CHG_0002 / "tests" / "test_acceptance.py").is_file()


def test_chg_0003_is_the_only_approved_active_change() -> None:
    active_dirs = [path.name for path in ACTIVE.iterdir() if path.is_dir()]
    assert active_dirs == ["CHG-0003-xianyu-account-boundary"]
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0003 / name) == "APPROVED"


def test_chg_0003_t7_completion_advances_only_to_t8() -> None:
    task_lines = [
        line
        for line in (CHG_0003 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]

    assert len(task_lines) == 9
    assert all(line.startswith("- [x]") for line in task_lines[:7])
    assert all(line.startswith("- [ ]") for line in task_lines[7:])

    state = json.loads(
        (ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8")
    )

    assert state["active_change"]["id"] == "CHG-0003-xianyu-account-boundary"
    assert state["active_change"]["status"] == "APPROVED"
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 7
    assert all(
        state["tasks"]["items"][index]["completed"] is True for index in range(7)
    )
    assert state["tasks"]["items"][7]["completed"] is False
    assert state["tasks"]["next_task"] == (
        "T8 Update capability evidence and run complete verification"
    )


def test_account_boundary_is_implemented_locally_but_not_externally(
    tmp_path: Path,
) -> None:
    from xianyu_system.worker.account import (
        AccountReference,
        AccountService,
        DuplicateAccountOwnership,
        InvalidAccountInput,
        InvalidLifecycleTransition,
        Profile,
        ProfileLifecycleStatus,
        ProfileNotFound,
        StaleProfileUpdate,
    )
    from xianyu_system.worker.account.persistence import AccountProfileRepository

    registry = registry_by_id()
    account = registry["CAP-XY-ACCOUNT"]
    assert account["status"] == "implementing"
    assert account["owner_module"] == "worker.account"
    assert account["active_change"] == "CHG-0003-xianyu-account-boundary"
    assert account["implementation_paths"] == ACCOUNT_IMPLEMENTATION_PATHS
    assert account["test_paths"] == ACCOUNT_TEST_PATHS
    assert account["last_verified_commit"] is None

    worker_root = ROOT / "app" / "xianyu_system" / "worker"
    account_root = worker_root / "account"
    assert (worker_root / "__init__.py").is_file()
    assert (account_root / "__init__.py").is_file()
    assert (account_root / "domain.py").is_file()
    assert (account_root / "persistence.py").is_file()
    assert (account_root / "service.py").is_file()
    assert (ROOT / "migrations" / "versions" / "0002_xianyu_account_boundary.py").is_file()
    account_init_path = account_root / "__init__.py"
    account_init_bytes = account_init_path.read_bytes()

    assert not account_init_bytes.startswith(b"\xef\xbb\xbf")
    assert account_init_bytes.startswith(
        b'"""Public surface for the local Xianyu account boundary.'
    )

    account_init_source = account_init_bytes.decode("utf-8")
    account_init_tree = ast.parse(account_init_source)
    assert "TYPE_CHECKING" in account_init_source
    assert "def __getattr__" in account_init_source
    assert '"AccountService"' in account_init_source
    assert "xianyu_system.worker.account.persistence" not in account_init_source
    assert "sqlalchemy" not in account_init_source.lower()
    for node in account_init_tree.body:
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module != "xianyu_system.worker.account.persistence"
            assert node.module != "xianyu_system.worker.account.service"

    import_safety_source = (
        ROOT / "tests" / "unit" / "test_import_safety.py"
    ).read_text(encoding="utf-8")
    assert '"xianyu_system.worker.account"' in import_safety_source
    assert '"xianyu_system.worker.account.domain"' in import_safety_source
    assert '"xianyu_system.worker.account.service"' not in import_safety_source.split(
        "IMPORT_MODULES", 1
    )[1].split("]", 1)[0]
    assert "account_service_loaded" in import_safety_source
    assert "account_persistence_loaded" in import_safety_source
    assert 'assert report["after"]["metadata_tables"] == []' in import_safety_source
    permanent_tests = {
        ROOT / "tests" / "unit" / "test_account_domain.py": 10,
        ROOT / "tests" / "unit" / "test_account_service.py": 7,
        ROOT / "tests" / "contract" / "test_account_persistence.py": 7,
        ROOT / "tests" / "contract" / "test_account_security.py": 4,
    }
    total_t7_tests = 0
    for test_path, expected_count in permanent_tests.items():
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
        tests = [
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        ]
        assert len(tests) == expected_count
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for decorator in node.decorator_list:
                    assert "parametrize" not in ast.unparse(decorator)
        total_t7_tests += len(tests)
    assert total_t7_tests == 28
    persistence_contract_source = (
        ROOT / "tests" / "contract" / "test_account_persistence.py"
    ).read_text(encoding="utf-8")
    security_contract_source = (
        ROOT / "tests" / "contract" / "test_account_security.py"
    ).read_text(encoding="utf-8")
    for forbidden_cleanup in [
        "install_account_package_collection_proxy",
        "install_core_metadata_empty_view",
        "types.ModuleType",
        "sys.modules[",
        "sys.modules.pop",
        "package.__getattr__",
        "tables_type.__eq__",
        "_xianyu_account_empty_view",
        "account_aware_eq",
        "Base.metadata.remove",
        "clear_mappers",
        "importlib.reload",
        "cleanup_account_metadata_after_module",
    ]:
        assert forbidden_cleanup not in persistence_contract_source
        assert forbidden_cleanup not in security_contract_source
    forbidden_contract_import_roots = {
        "xianyu_system",
        "sqlalchemy",
        "alembic",
        "types",
        "importlib",
    }
    for contract_path in [
        ROOT / "tests" / "contract" / "test_account_persistence.py",
        ROOT / "tests" / "contract" / "test_account_security.py",
    ]:
        tree = ast.parse(contract_path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.Import):
                roots = {alias.name.split(".", 1)[0] for alias in node.names}
                assert roots.isdisjoint(forbidden_contract_import_roots)
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                assert (
                    node.module.split(".", 1)[0]
                    not in forbidden_contract_import_roots
                )
        contract_source = contract_path.read_text(encoding="utf-8")
        assert "run_isolated_account_python" in contract_source
        assert "subprocess.run" in contract_source
        assert "sys.executable" in contract_source

    import runpy
    import sys

    from xianyu_system.core.database import Base

    before_account_modules = {
        name for name in sys.modules if name.startswith("xianyu_system.worker.account")
    }
    before_tables = tuple(Base.metadata.tables)
    before_eq = type(Base.metadata.tables).__eq__
    for contract_path in [
        ROOT / "tests" / "contract" / "test_account_persistence.py",
        ROOT / "tests" / "contract" / "test_account_security.py",
    ]:
        runpy.run_path(str(contract_path))
    after_account_modules = {
        name for name in sys.modules if name.startswith("xianyu_system.worker.account")
    }
    after_tables = tuple(Base.metadata.tables)
    after_eq = type(Base.metadata.tables).__eq__
    assert after_account_modules == before_account_modules
    assert after_tables == before_tables
    assert after_eq is before_eq
    assert (
        "def test_account_operations_make_no_network_browser_or_credential_store_calls"
        in security_contract_source
    )
    for operation_name in [
        "create_profile",
        "get_profile",
        "list_profiles",
        "rename_profile",
        "set_external_account_identifier",
        "set_credential_reference",
        "set_lifecycle_status",
    ]:
        assert operation_name in security_contract_source
    assert "socket.create_connection" in security_contract_source
    assert "socket.socket" in security_contract_source
    assert "subprocess.run" in security_contract_source
    assert "subprocess.Popen" in security_contract_source
    assert "Path.home" in security_contract_source
    assert (
        '"external_account_identifier": "   "' in persistence_contract_source
    )
    assert '"credential_reference": "   "' in persistence_contract_source
    assert "synthetic-profile-whitespace-external" in persistence_contract_source
    assert "synthetic-profile-whitespace-credential" in persistence_contract_source

    for capability_id in CORE_IDS:
        capability = registry[capability_id]
        assert capability["status"] == "verified"
        assert (
            "changes/archive/CHG-0002-core-application/tests/test_acceptance.py"
            in capability["test_paths"]
        )

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for forbidden in ["Cookie=", "Token=", "Secret=", "Password="]:
        assert forbidden not in env_example

    proposal = (CHG_0003 / "proposal.md").read_text(encoding="utf-8")
    design = (CHG_0003 / "design.md").read_text(encoding="utf-8")
    acceptance = (CHG_0003 / "acceptance.md").read_text(encoding="utf-8")
    assert "T1 through T7 are complete." in proposal
    assert "T8 is the next executable task" in proposal
    assert "T1 through T7 are complete." in acceptance
    assert "PR #3 remains Draft" in acceptance
    assert "## Current implementation" in design
    assert "xianyu_system.worker.account is implemented" in design

    resources = initialize_database(tmp_path / "account-boundary.db")
    try:
        upgrade_database(resources)
        assert get_current_revision(resources) == ACCOUNT_REVISION
        assert set(inspect(resources.engine).get_table_names()) == {
            "alembic_version",
            ACCOUNT_TABLE,
        }

        service = AccountService(resources.session_factory)
        first = service.create_profile(
            account_alias="synthetic-profile-one",
            external_account_identifier="synthetic-external-reference-001",
        )
        second = service.create_profile(account_alias="synthetic-profile-two")

        assert UUID(first.profile_id).version == 4
        assert first.profile_id == first.profile_id.lower()
        assert first.lifecycle_status is ProfileLifecycleStatus.PENDING
        assert first.row_version == 1
        assert second.profile_id != first.profile_id
        assert isinstance(first.account_reference, AccountReference)
        assert first.account_reference.profile_id == first.profile_id
        assert first.account_reference.account_alias == first.account_alias
        assert (
            first.account_reference.external_account_identifier
            == first.external_account_identifier
        )
        assert first.account_reference.credential_reference == first.credential_reference

        assert service.get_profile(first.profile_id) == first
        assert [profile.profile_id for profile in service.list_profiles()] == sorted(
            [first.profile_id, second.profile_id]
        )

        renamed = service.rename_profile(
            first.profile_id,
            account_alias=" synthetic-profile-renamed ",
            expected_version=first.row_version,
        )
        assert renamed.account_alias == "synthetic-profile-renamed"
        assert renamed.account_reference is not first.account_reference
        assert renamed.account_reference.profile_id == renamed.profile_id
        assert renamed.row_version == 2

        with_external = service.set_external_account_identifier(
            renamed.profile_id,
            external_account_identifier=" synthetic-external-reference-002 ",
            expected_version=renamed.row_version,
        )
        assert (
            with_external.account_reference.external_account_identifier
            == "synthetic-external-reference-002"
        )
        cleared_external = service.set_external_account_identifier(
            renamed.profile_id,
            external_account_identifier=None,
            expected_version=with_external.row_version,
        )
        assert cleared_external.external_account_identifier is None

        with_credential = service.set_credential_reference(
            renamed.profile_id,
            credential_reference=" synthetic-credential-reference-001 ",
            expected_version=cleared_external.row_version,
        )
        assert (
            with_credential.account_reference.credential_reference
            == "synthetic-credential-reference-001"
        )
        cleared_credential = service.set_credential_reference(
            renamed.profile_id,
            credential_reference=None,
            expected_version=with_credential.row_version,
        )
        assert cleared_credential.credential_reference is None

        enabled = service.set_lifecycle_status(
            renamed.profile_id,
            lifecycle_status=ProfileLifecycleStatus.ENABLED,
            expected_version=cleared_credential.row_version,
        )
        disabled = service.set_lifecycle_status(
            renamed.profile_id,
            lifecycle_status=ProfileLifecycleStatus.DISABLED,
            expected_version=enabled.row_version,
        )
        reenabled = service.set_lifecycle_status(
            renamed.profile_id,
            lifecycle_status="ENABLED",
            expected_version=disabled.row_version,
        )
        assert reenabled.lifecycle_status is ProfileLifecycleStatus.ENABLED

        detached_reference = first.account_reference.with_account_alias(
            "synthetic-detached-alias"
        )
        assert detached_reference is not first.account_reference
        assert detached_reference.profile_id == first.profile_id
        assert detached_reference.account_alias == "synthetic-detached-alias"
        with pytest.raises(InvalidAccountInput):
            Profile(
                profile_id="22222222-2222-4222-8222-222222222222",
                account_reference=first.account_reference,
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                row_version=1,
            )

        with pytest.raises(InvalidLifecycleTransition):
            service.set_lifecycle_status(
                renamed.profile_id,
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                expected_version=reenabled.row_version,
            )

        with pytest.raises(StaleProfileUpdate):
            service.rename_profile(
                renamed.profile_id,
                account_alias="synthetic-stale-alias",
                expected_version=1,
            )

        service.set_external_account_identifier(
            second.profile_id,
            external_account_identifier="synthetic-external-reference-003",
            expected_version=second.row_version,
        )
        with pytest.raises(DuplicateAccountOwnership):
            service.set_external_account_identifier(
                reenabled.profile_id,
                external_account_identifier="synthetic-external-reference-003",
                expected_version=reenabled.row_version,
            )

        second_after_external = service.get_profile(second.profile_id)
        service.set_credential_reference(
            second.profile_id,
            credential_reference="synthetic-credential-reference-002",
            expected_version=second_after_external.row_version,
        )
        with pytest.raises(DuplicateAccountOwnership) as duplicate_error:
            service.set_credential_reference(
                reenabled.profile_id,
                credential_reference="synthetic-credential-reference-002",
                expected_version=reenabled.row_version,
            )
        assert "synthetic-credential-reference-002" not in str(duplicate_error.value)

        manual = Profile.create(
            profile_id="11111111-1111-4111-8111-111111111111",
            account_alias="synthetic-uncommitted-profile",
        )
        session = resources.session_factory()
        try:
            AccountProfileRepository(session).add(manual)
        finally:
            session.close()
        with pytest.raises(ProfileNotFound):
            service.get_profile(manual.profile_id)

        invalid_rows = [
            {
                "profile_id": "22222222-2222-4222-8222-222222222222",
                "account_alias": "   ",
                "external_account_identifier": None,
                "credential_reference": None,
            },
            {
                "profile_id": "33333333-3333-4333-8333-333333333333",
                "account_alias": " padded-alias ",
                "external_account_identifier": None,
                "credential_reference": None,
            },
            {
                "profile_id": "44444444-4444-4444-8444-444444444444",
                "account_alias": "valid-alias",
                "external_account_identifier": " padded-external ",
                "credential_reference": None,
            },
            {
                "profile_id": "55555555-5555-4555-8555-555555555555",
                "account_alias": "valid-alias",
                "external_account_identifier": None,
                "credential_reference": " padded-credential ",
            },
        ]
        insert_statement = text(
            """
            INSERT INTO xianyu_account_profiles (
                profile_id,
                account_alias,
                external_account_identifier,
                credential_reference,
                lifecycle_status,
                row_version
            )
            VALUES (
                :profile_id,
                :account_alias,
                :external_account_identifier,
                :credential_reference,
                'PENDING',
                1
            )
            """
        )
        for invalid_row in invalid_rows:
            with pytest.raises(IntegrityError), resources.engine.begin() as connection:
                connection.execute(insert_statement, invalid_row)
    finally:
        dispose_database(resources)

    domain_source = (account_root / "domain.py").read_text(encoding="utf-8").lower()
    for forbidden in ["sqlalchemy", "fastapi", "alembic", "httpx", "requests", "browser"]:
        assert forbidden not in domain_source

    service_source = (account_root / "service.py").read_text(encoding="utf-8")
    for forbidden in ["FastAPI", "Router", "requests.", "httpx.", "Provider"]:
        assert forbidden not in service_source

    persistence_source = (account_root / "persistence.py").read_text(encoding="utf-8")
    for forbidden in ["create_engine", "sessionmaker", ".commit("]:
        assert forbidden not in persistence_source
    assert "__tablename__" not in persistence_source
    assert "mapped_column" not in persistence_source

    public_source = (account_root / "__init__.py").read_text(encoding="utf-8")
    for forbidden in ["_AccountProfileRecord", "Table", "Repository", "Session"]:
        assert forbidden not in public_source

    migration_source = (
        ROOT / "migrations" / "versions" / "0002_xianyu_account_boundary.py"
    ).read_text(encoding="utf-8").lower()
    for forbidden in ["insert", "bulk_insert", "network", "browser", "cookie", "token"]:
        assert forbidden not in migration_source
