from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE_ID = "CHG-0016-local-only-manual-platform-verification-handoff"
CHANGE_DIR = ROOT / "changes" / "active" / CHANGE_ID
CHANGE_FILES = ["proposal.md", "design.md", "tasks.md", "acceptance.md"]


def read_doc(name: str) -> str:
    return (CHANGE_DIR / name).read_text(encoding="utf-8")


def test_change_documents_are_implementing() -> None:
    for name in CHANGE_FILES:
        text = read_doc(name)
        assert f"Change ID: {CHANGE_ID}" in text
        assert "Status: IMPLEMENTING" in text


def test_reuse_decision_is_patch_upstream() -> None:
    text = "\n\n".join(read_doc(name) for name in CHANGE_FILES)
    assert "Decision: PATCH_UPSTREAM" in text
    assert "CHG-0009 remains" in text
    assert "Decision: BUILD_LOCAL_EXCEPTION" not in text


def test_implementation_forbids_unsafe_runtime_paths() -> None:
    acceptance = read_doc("acceptance.md")
    for required in [
        "No second IM, Token, WebSocket, sender, or automatic reply executor is created.",
        "No automated page interaction or remote solver is added.",
        "Default replies remain disabled pending owner decision after ignored backup.",
        "No websocket, scheduler, or CHG-0010 worker is started.",
        "No message is sent.",
    ]:
        assert required in acceptance


def test_manual_handoff_boundaries_are_documented() -> None:
    design = read_doc("design.md")
    for required in [
        "Do not assume a Docker container can directly open a Windows desktop browser.",
        "Any unknown state is `FAIL_CLOSED`.",
        "memory-only",
        "TTL maximum five minutes",
        "Forbidden program behavior",
        "Use upstream account service.",
        "The handoff must not generate an IM Token.",
    ]:
        assert required in design


def test_evidence_and_threat_model_exist() -> None:
    assert (CHANGE_DIR / "evidence" / "upstream-audit.md").is_file()
    assert (CHANGE_DIR / "threat-model.md").is_file()


def test_patch_artifact_is_recorded_by_change() -> None:
    assert (
        ROOT
        / "vendor"
        / "patches"
        / "xianyu-auto-reply"
        / "bda1a85-manual-only-verification.patch"
    ).is_file()


def test_change_file_set_is_explicit() -> None:
    changed_files = [
        path.relative_to(CHANGE_DIR).as_posix()
        for path in CHANGE_DIR.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]
    assert sorted(changed_files) == [
        "acceptance.md",
        "design.md",
        "evidence/upstream-audit.md",
        "proposal.md",
        "tasks.md",
        "tests/test_acceptance.py",
        "threat-model.md",
    ]
