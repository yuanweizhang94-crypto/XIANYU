from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import cast

import yaml

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"

CHG_0002 = ARCHIVE / "CHG-0002-core-application"
CHG_0003 = ARCHIVE / "CHG-0003-xianyu-account-boundary"
CHG_0004 = ARCHIVE / "CHG-0004-xianyu-message-boundary"
CHG_0005 = ACTIVE / "CHG-0005-xianyu-reply-boundary"

MESSAGE_CAPABILITY = "CAP-XY-MESSAGE"
REPLY_CAPABILITY = "CAP-XY-REPLY"

MESSAGE_VERIFIED_CANDIDATE_SHA = "49498e6f30944883c1a0a5a504932bbd02fc86de"
REPLY_EVIDENCE_CANDIDATE_SHA = "5724d164619c64e93295595b3acdd1429d24e3e0"

MESSAGE_ARCHIVED_ACCEPTANCE = (
    "changes/archive/CHG-0004-xianyu-message-boundary/tests/test_acceptance.py"
)

MESSAGE_ACTIVE_ACCEPTANCE = (
    "changes/active/CHG-0004-xianyu-message-boundary/tests/test_acceptance.py"
)


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(
        (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8")
    )
    return {str(item["id"]): item for item in registry["capabilities"]}


def assert_candidate_commit_is_valid_offline(commit_sha: str) -> None:
    assert re.fullmatch(r"[0-9a-f]{40}", commit_sha)
    candidate_ref = f"{commit_sha}^{{commit}}"
    candidate_exists = subprocess.run(
        ["git", "cat-file", "-e", candidate_ref],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if candidate_exists.returncode == 0:
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit_sha, "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        assert ancestor.returncode == 0, ancestor.stderr or ancestor.stdout
        return

    shallow = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert shallow.stdout.strip() == "true", (
        "reply evidence candidate commit is missing from a complete local repository"
    )


def test_completed_changes_are_archived_with_history_preserved() -> None:
    for change in [CHG_0002, CHG_0003, CHG_0004]:
        assert change.is_dir()
        assert not (ACTIVE / change.name).exists()
        for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
            assert status_of(change / name) == "ARCHIVED"
        assert (change / "tests" / "test_acceptance.py").is_file()

    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        text = (CHG_0004 / name).read_text(encoding="utf-8")
        assert "Merge and archive record" in text
        assert "bab7a1a86239cb4dba9b2f7dc8db0ff33bc80dc6" in text
        assert "0cfd719dff5d472e9e5ac26bf720afc7efb74e9f" in text
        assert "CHG-0005 is a DRAFT preparation only" in text


def test_chg_0005_is_the_only_verifying_active_change() -> None:
    active_dirs = sorted(path.name for path in ACTIVE.iterdir() if path.is_dir())
    assert active_dirs == ["CHG-0005-xianyu-reply-boundary"]
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0005 / name) == "VERIFYING"


def test_chg_0005_t9_completion_has_no_next_task() -> None:
    task_lines = [
        line
        for line in (CHG_0005 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]
    assert len(task_lines) == 9
    completed_count = sum(line.startswith("- [x]") for line in task_lines)
    assert completed_count == 9
    assert all(line.startswith("- [x]") for line in task_lines)
    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] == {
        "id": "CHG-0005-xianyu-reply-boundary",
        "status": "VERIFYING",
        "path": "changes/active/CHG-0005-xianyu-reply-boundary",
    }
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == completed_count
    assert state["tasks"]["next_task"] is None
    assert all(item["completed"] is True for item in state["tasks"]["items"])
    assert state["capabilities"]["by_status"] == {"planned": 4, "verified": 6}


def test_reply_capability_remains_planned_and_unimplemented() -> None:
    registry = registry_by_id()
    message = registry[MESSAGE_CAPABILITY]
    reply = registry[REPLY_CAPABILITY]

    assert message["status"] == "verified"
    assert message["active_change"] is None
    assert message["last_verified_commit"] == MESSAGE_VERIFIED_CANDIDATE_SHA
    message_implementation_paths = cast(list[str], message["implementation_paths"])
    message_test_paths = cast(list[str], message["test_paths"])
    assert len(message_implementation_paths) == 7
    assert len(message_test_paths) == 10
    assert MESSAGE_ARCHIVED_ACCEPTANCE in message_test_paths
    assert MESSAGE_ACTIVE_ACCEPTANCE not in message_test_paths

    assert reply["status"] == "verified"
    assert reply["active_change"] is None
    assert reply["last_verified_commit"] == REPLY_EVIDENCE_CANDIDATE_SHA
    assert_candidate_commit_is_valid_offline(REPLY_EVIDENCE_CANDIDATE_SHA)
    assert reply["owner_module"] == "app.reply"
    assert reply["specification"] == "specs/capabilities/CAP-XY-REPLY.md"
    reply_implementation_paths = cast(list[str], reply["implementation_paths"])
    reply_test_paths = cast(list[str], reply["test_paths"])
    assert len(reply_implementation_paths) == 8
    assert len(reply_test_paths) == 12

    assert (ROOT / "app" / "xianyu_system" / "reply").is_dir()
    assert (ROOT / "migrations" / "versions" / "0004_xianyu_reply_boundary.py").is_file()
    assert not (ROOT / "app" / "xianyu_system" / "reply.py").exists()
    assert not (ROOT / "app" / "xianyu_system" / "worker" / "reply.py").exists()
    assert not (ROOT / "app" / "xianyu_system" / "worker" / "reply").exists()
    expected_unit_tests = {
        "test_reply_domain.py",
        "test_reply_evaluator.py",
        "test_reply_renderer.py",
        "test_reply_mapper.py",
        "test_reply_service.py",
    }
    expected_contract_tests = {
        "test_reply_persistence.py",
        "test_reply_security.py",
    }
    assert expected_unit_tests <= {path.name for path in (ROOT / "tests" / "unit").glob("*reply*")}
    assert expected_contract_tests <= {
        path.name for path in (ROOT / "tests" / "contract").glob("*reply*")
    }

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for forbidden in [
        "Cookie=",
        "Token=",
        "Secret=",
        "Password=",
        "Session=",
        "Customer=",
        "Reply_API=",
        "AI_API=",
        "WECOM=",
    ]:
        assert forbidden not in env_example

    documents = [
        (CHG_0005 / "proposal.md").read_text(encoding="utf-8"),
        (CHG_0005 / "design.md").read_text(encoding="utf-8"),
        (CHG_0005 / "acceptance.md").read_text(encoding="utf-8"),
    ]
    joined = "\n".join(documents)
    for required in [
        "APPROVED",
        "No real Xianyu message sending",
        "No WeCom integration",
        "No AI Provider",
        "Synthetic Fixtures",
        "Fail closed",
        "T1-T5 design and architecture are approved",
        "Runtime implementation is not started",
        "T6 requires a separate explicit owner authorization",
        "ReplyRule identity is `(rule_id, version)`",
        "`rule_id`, `rule_version`",
        "ReplyAuditEvent",
        "`lifecycle_state == ENABLED` is the only",
        "`ARCHIVED`",
        "ReplyAuditRepository",
        "ReplyEvaluationResult",
        "ReplyDecisionService owns",
        "Migration created in Phase 1: no",
        "T6 implementation record",
        "CAP-XY-REPLY intentionally remains `planned`",
        "T7 permanent evidence record",
        "T9 Ready candidate",
        "PR #5 remains Draft until the Ready Candidate passes final CI",
        "T9 final acceptance criteria",
        "T9 Ready Candidate SHA is `365cce3ef6574974c1cee1bb676fe8c1ad8ad4e3`",
        "PR #5 is Ready for review",
        "open, and unmerged",
        "Merge requires separate explicit authorization",
    ]:
        assert required in joined

    design_text = (CHG_0005 / "design.md").read_text(encoding="utf-8")
    spec_text = (ROOT / "specs" / "capabilities" / "CAP-XY-REPLY.md").read_text(encoding="utf-8")
    combined = "\n".join([design_text, spec_text])
    for forbidden in [
        "No Runtime design is approved.",
        "No term is final until a later approved task records the decision.",
        "All terminology, matching, authorization, risk, content safety, precedence, fallback, escalation, ownership, persistence, lifecycle, and failure decisions still require approval in later tasks.",
        "This candidate description is not approved Runtime design.",
        "| `enabled` | Boolean",
    ]:
        assert forbidden not in combined
