from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHANGE = ROOT / "changes" / "active" / "CHG-0010-xianyu-automatic-reply-mvp"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def combined_change_text() -> str:
    return "\n".join(read(CHANGE / name) for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"])


def test_chg_0010_records_automatic_reply_direction() -> None:
    text = combined_change_text()
    assert "CHG-0010 Xianyu automatic reply MVP" in text
    assert "automatic reply MVP" in text
    assert "No operator workflow" in text
    assert "per-message selection" in text
    assert "XIANYU-AUTOREPLY-TEST-20260729-A7P3" in text
    assert "XIANYU-AUTOREPLY-ACK-20260729-A7P3" in text


def test_chg_0010_tasks_are_ordered() -> None:
    lines = [line for line in read(CHANGE / "tasks.md").splitlines() if line.startswith("- [")]
    assert len(lines) == 8
    assert lines[0] == "- [x] T1 Record owner direction correction and automatic-reply scope"
    assert lines[1] == "- [x] T2 Define deterministic autoreply configuration and safety gates"
    assert lines[-1] == "- [ ] T8 Publish PR and complete final administration"


def test_chg_0010_safety_boundaries_are_fail_closed() -> None:
    text = combined_change_text()
    assert "Automatic reply is disabled by default" in text
    assert "UNKNOWN is never retried automatically" in text
    assert "Startup watermark prevents replying to historical messages" in text
    assert "Conversation cooldown" in text
    assert "full message text" in text
    assert "No upstream tracked source" in text
    assert "docs/XIANYU_AUTOREPLY_QUICKSTART.md" in text
