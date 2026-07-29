from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHANGE = ROOT / "changes" / "active" / "CHG-0008-xianyu-upstream-integration-foundation"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def combined_change_text() -> str:
    return "\n".join(read(CHANGE / name) for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"])


def test_chg_0008_records_direction_correction_without_adapter_runtime() -> None:
    text = combined_change_text()
    assert "Direction correction record" in text
    assert "stop manufacturing large adapter abstractions" in text
    assert "WAITING_FOR_OPERATOR_APPROVED_P1_LOGIN" in text
    assert not (ROOT / "app" / "xianyu_system" / "adapters" / "xianyu").exists()
    for forbidden in [
        "FakeXianyuSessionAdapter",
        "FakeXianyuMessageAdapter",
        "FakeXianyuPublishAdapter",
    ]:
        assert forbidden in text


def test_chg_0008_has_pinned_upstream_and_truthful_pilot_statuses() -> None:
    text = combined_change_text()
    assert "bda1a859df63fa5f24e51398fa80a23490bb6dfc" in text
    assert "AGPL-3.0" in text
    assert "5ce38ab2c4236f7eaa65983ce5c2da1f2fbd09af" in text
    assert "UNRESOLVED" in text
    assert "P0 system startup: PASSED" in text
    assert "P1 manual scan login: WAITING_FOR_OPERATOR_APPROVAL" in text
    assert "D:\\Administrator\\Documents\\DockerDesktopWSL" in text
    assert "Administrator default password: replaced" in text
    assert "Recommendation remains `INSUFFICIENT_EVIDENCE`" in text


def test_chg_0008_tasks_are_ordered_and_stop_before_supervised_account() -> None:
    lines = [line for line in read(CHANGE / "tasks.md").splitlines() if line.startswith("- [")]
    assert len(lines) == 9
    assert lines[:5] == [
        "- [x] T1 Obtain explicit project-owner approval for CHG-0008",
        "- [x] T2 Pivot CHG-0008 to upstream pilot and stop unnecessary offline adapter abstraction",
        "- [x] T3 Pin upstream projects and record license and safety audit facts",
        "- [x] T4 Define isolated deployment, test-account, credential, and live-operation boundaries",
        "- [x] T5 Record P0-P7 supervised pilot checklist and stop conditions",
    ]
    assert lines[5].startswith("- [x] T6 Execute local isolated P0 startup")
    assert lines[6].startswith("- [ ] T7 Execute supervised account P1-P3")
