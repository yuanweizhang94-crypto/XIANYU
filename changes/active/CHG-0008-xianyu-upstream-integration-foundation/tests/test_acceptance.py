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
    assert "P2_P6_PASSED_WITH_OPERATOR_DELISTED_CLEANUP" in text
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
    assert "P1 manual scan login: PASSED" in text
    assert "P2 online state: PASSED" in text
    assert "P3 read-only message verification: PASSED" in text
    assert "P4 manually confirmed reply: PASSED" in text
    assert "P5 manually confirmed test listing: PASSED" in text
    assert "P6 test listing cleanup: PASSED as operator-delisted cleanup, not deletion" in text
    assert "P7 one-time schedule: NOT_EXECUTED" in text
    assert "D:\\Administrator\\Documents\\DockerDesktopWSL" in text
    assert "Administrator default password: replaced" in text
    assert "Final recommendation: `WRAP`" in text


def test_chg_0008_tasks_are_ordered_and_complete_after_supervised_pilot() -> None:
    lines = [line for line in read(CHANGE / "tasks.md").splitlines() if line.startswith("- [")]
    assert len(lines) == 9
    assert lines == [
        "- [x] T1 Obtain explicit project-owner approval for CHG-0008",
        "- [x] T2 Pivot CHG-0008 to upstream pilot and stop unnecessary offline adapter abstraction",
        "- [x] T3 Pin upstream projects and record license and safety audit facts",
        "- [x] T4 Define isolated deployment, test-account, credential, and live-operation boundaries",
        "- [x] T5 Record P0-P7 supervised pilot checklist and stop conditions",
        "- [x] T6 Execute local isolated P0 startup only after operator approves upstream runtime setup",
        "- [x] T7 Execute supervised account P1-P3 only with a dedicated test account",
        "- [x] T8 Execute supervised manual operation P4-P7 only after P1-P3 pass",
        "- [x] T9 Record pilot conclusion and final PR administration",
    ]
    text = combined_change_text()
    assert "Completed tasks: 9 / 9" in text
    assert "Next task: null" in text
    assert "PR #9 remains Draft, open, and unmerged" in text
    assert "No Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, CHG-0009" in text
