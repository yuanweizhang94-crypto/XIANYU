from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch"
EXPECTED_PATCH_FILES = {
    "backend-web/app/api/routes/_exports.py",
    "backend-web/app/api/routes/cookies.py",
    "backend-web/app/api/routes/product_publish_capability.py",
    "tests/test_chg0028_selected_account_on_demand_capability.py",
}


def _patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def _git_apply_numstat() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "apply", "--numstat", "--unidiff-zero", str(PATCH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _numstat_paths(stdout: str) -> set[str]:
    paths = set()
    for line in stdout.splitlines():
        fields = line.split("\t")
        if len(fields) == 3:
            paths.add(fields[2])
    return paths


def _added_patch_text_for(path_fragment: str) -> str:
    in_file = False
    added_lines: list[str] = []
    for line in _patch_text().splitlines():
        if line.startswith("diff --git "):
            in_file = path_fragment in line
            continue
        if in_file and line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def _all_added_patch_text() -> str:
    return "\n".join(
        line[1:]
        for line in _patch_text().splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def test_chg0028_patch_is_parseable_and_scoped_to_existing_backend_owner() -> None:
    result = _git_apply_numstat()

    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert _numstat_paths(result.stdout) == EXPECTED_PATCH_FILES


def test_selected_account_route_uses_existing_capability_service_once() -> None:
    route_added = _added_patch_text_for("product_publish_capability.py")

    assert 'prefix="/product-publish/accounts"' in route_added
    assert 'router.get("/{account_id}/capability"' in route_added
    assert "detect_publish_account_capability" in route_added
    assert route_added.count("detect_publish_account_capability(") == 1
    assert "session_maintenance" not in route_added
    assert "consumers.publish" not in route_added


def test_account_list_contract_is_on_demand_not_persisted_ready() -> None:
    cookies_added = _added_patch_text_for("backend-web/app/api/routes/cookies.py")

    assert '"mode": "ON_DEMAND"' in cookies_added
    assert '"checked": False' in cookies_added
    assert 'state="NOT_CHECKED"' in cookies_added
    assert "PublishAccountCapabilityService" not in cookies_added
    assert "mtop.idle.pc.idleitem.preget" not in cookies_added
    assert "set_session_maintenance_state" not in cookies_added


def test_patch_does_not_create_global_readiness_writer_or_browser_gate() -> None:
    added = "\n".join(
        [
            _added_patch_text_for("backend-web/app/api/routes/_exports.py"),
            _added_patch_text_for("backend-web/app/api/routes/cookies.py"),
            _added_patch_text_for("backend-web/app/api/routes/product_publish_capability.py"),
        ]
    )
    forbidden = [
        "session_maintenance.consumers.publish",
        '"publish_auth_readiness"',
        "'publish_auth_readiness'",
        "set_session_maintenance_state",
        "mark_cookie_update_session_pending",
        "async_playwright",
        "launch_persistent_context",
        "page.goto",
        "browser",
        "scheduler",
        "COMPANY_LOCAL_EXECUTION_TOOL",
    ]

    assert [term for term in forbidden if term in added] == []


def test_patch_contains_upstream_native_mock_tests() -> None:
    tests_added = _added_patch_text_for("tests/test_chg0028_selected_account_on_demand_capability.py")

    assert "test_unchecked_account_list_publish_capability_is_on_demand_not_ready" in tests_added
    assert "test_account_list_does_not_call_publish_capability_producer" in tests_added
    assert "test_selected_account_capability_calls_existing_service_once" in tests_added
    assert "test_selected_account_success_uses_current_cookie_and_existing_service_once" in tests_added
    assert "test_transient_failure_is_retryable_not_session_invalid" in tests_added
    assert "test_account_invalid_and_fatal_semantics_are_preserved" in tests_added
    assert "AsyncMock" in tests_added
    assert "assert_awaited_once_with" in tests_added
    assert "cookie=\"current-cookie\"" in tests_added
    assert "session.commit.assert_not_awaited()" in tests_added
