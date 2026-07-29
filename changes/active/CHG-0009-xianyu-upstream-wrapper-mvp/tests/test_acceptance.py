from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHANGE = ROOT / "changes" / "active" / "CHG-0009-xianyu-upstream-wrapper-mvp"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def combined_change_text() -> str:
    return "\n".join(read(CHANGE / name) for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"])


def test_chg_0009_records_wrapper_scope_and_non_goals() -> None:
    text = combined_change_text()
    assert "CHG-0009 Xianyu upstream wrapper MVP" in text
    assert "XIANYU-WRAPPER-TEST-20260729-1544-R9X6" in text
    assert "XIANYU-WRAPPER-ACK-20260729-1544-R9X6" in text
    assert "No upstream source code is copied" in text
    assert "product publishing" in text
    assert "automatic delivery" in text


def test_chg_0009_tasks_are_ordered() -> None:
    lines = [line for line in read(CHANGE / "tasks.md").splitlines() if line.startswith("- [")]
    assert len(lines) == 9
    assert lines[0] == "- [x] T1 Record owner approval and executable wrapper scope"
    assert lines[5] == "- [x] T6 Add operator quickstart documentation"
    assert lines[6] == "- [x] T7 Run complete local verification"
    assert lines[7] == "- [x] T8 Execute supervised real Wrapper message loop"
    assert lines[-1] == "- [x] T9 Publish Draft PR and complete final administration"


def test_chg_0009_wrapper_boundaries_are_fail_closed() -> None:
    text = combined_change_text()
    assert "Loopback hosts only are allowed" in text
    assert "Live writes are disabled by default" in text
    assert "UNKNOWN" in text
    assert "must not be retried automatically" in text
    assert "docker compose --project-name xianyu_pilot" in text
    assert "must not operate mysql, redis, backend-web, frontend, sub2api" in text
    assert "PR #10" in text
