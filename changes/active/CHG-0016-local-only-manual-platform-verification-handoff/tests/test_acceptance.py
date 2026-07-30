import json
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


def test_patch_artifact_parseability_repair_is_documented() -> None:
    tasks = read_doc("tasks.md")
    acceptance = read_doc("acceptance.md")

    for required in [
        "PATCH_ARTIFACT_CORRUPT",
        "RAW_WORKTREE_HASH_MISMATCH_0_OF_5",
        "WORKTREE_EOL_NORMALIZATION_ONLY",
        "PATCH_ARTIFACT_REPAIR_BLOCKED_BY_DIFF_CHECK",
        "deterministic Git-generated zero-context patch",
        "contains no context lines inside hunks",
        "contains no added payload with trailing spaces or tabs",
        "staged Git blob comparison 5/5",
    ]:
        assert required in tasks

    assert "git apply --numstat --unidiff-zero" in acceptance
    assert "git apply --check --unidiff-zero" in acceptance
    assert "--whitespace=error-all" in acceptance
    assert "--unified=0" in acceptance
    assert "Applied Git blobs match build Git blobs 5/5." in acceptance
    assert "Git-canonical content is identical for all five target files." in acceptance


def test_t11_repair_cycle_is_closed_and_t12_is_next() -> None:
    tasks = read_doc("tasks.md")

    assert "- [x] T11 Repair live manual verification defects" in tasks
    assert "- [ ] T12 Run controlled owner manual validation without sending messages." in tasks
    assert "Completed tasks: 11 / 13" in tasks
    assert "Next task: T12 Run controlled owner manual validation without sending messages." in tasks


def test_t11_exact_repair_evidence_is_recorded() -> None:
    docs = "\n\n".join([read_doc("tasks.md"), read_doc("acceptance.md")])

    for required in [
        "c0e78c341fd7a4d401396be6b9e71c2ff47ff4d7",
        "c7bf9a52e795ee7f472c68d426b7bd44c79a88ed",
        "92e14642beb4bbdfa513e305474a37ee08135dad",
        "c72c146f088b661bc9584364a9eecbddbfe27321",
        "84b1fdf376d3fa08199d85fac472cb502cbb0ea7",
        "bb023f67c860125c5ec6043192e372d7fd9d52c2",
        "08c0021c672a86cc10d80b30c62217c1fc27d691",
        "64db9f099d65341a9e118fbca07bfb5be6e5b89b",
        "174fac36b92f87b25d669a5a3ad80c59983a37d2",
        "E5791692B69D95157A2249EF6B4C04F71A65C8513412B1A87C70EFF03D117FFE",
        "WORKTREE_EOL_NORMALIZATION_ONLY",
    ]:
        assert required in docs


def test_generated_state_advances_only_to_t12() -> None:
    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    tasks = state["tasks"]

    assert state["active_change"]["id"] == CHANGE_ID
    assert state["active_change"]["status"] == "IMPLEMENTING"
    assert tasks["total"] == 13
    assert tasks["completed"] == 11
    assert tasks["next_task"] == "T12 Run controlled owner manual validation without sending messages."

    task_items = {task["text"].split(" ", 1)[0]: task for task in tasks["items"]}
    assert task_items["T12"]["completed"] is False
    assert task_items["T13"]["completed"] is False


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
