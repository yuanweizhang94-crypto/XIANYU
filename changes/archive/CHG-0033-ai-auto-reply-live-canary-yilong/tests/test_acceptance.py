from pathlib import Path


CHANGE_ID = "CHG-0033-ai-auto-reply-live-canary-yilong"
ROOT = Path(__file__).resolve().parents[4]
CHANGE_DIR = ROOT / "changes" / "archive" / CHANGE_ID


def test_chg0033_zero_action_gates_are_recorded() -> None:
    acceptance = (CHANGE_DIR / "acceptance.md").read_text(encoding="utf-8")

    assert "`COMMANDER_GO_FOR_AI_LIVE_CANARY=false`" in acceptance
    assert "`AI_ENABLEMENT_INVOCATIONS=0`" in acceptance
    assert "`AI_PROVIDER_INVOCATIONS=1`" in acceptance
    assert "`SENDER_FREE_PROVIDER_INVOCATIONS=1`" in acceptance
    assert "`AI_REPLY_SEND_INVOCATIONS=0`" in acceptance
    assert "`PLATFORM_SEND_INVOCATIONS=0`" in acceptance
    assert "`PRODUCTION_MUTATION_COUNT=0`" in acceptance


def test_chg0033_identity_and_credential_limits_are_recorded() -> None:
    proposal = (CHANGE_DIR / "proposal.md").read_text(encoding="utf-8")
    evidence = (CHANGE_DIR / "evidence" / "20260825-change-creation.md").read_text(
        encoding="utf-8"
    )

    assert "APPROVED_ACCOUNT_MASKED=280***247" in proposal
    assert "APPROVED_ACCOUNT_MASKED=280***247" in evidence
    assert "PARENT_AI_CREDENTIAL_USED=false" in proposal
    assert "PARENT_AI_CREDENTIAL_PRINTED=false" in proposal
    assert "PARENT_AI_CREDENTIAL_PERSISTED=false" in proposal
    assert "screenshot was used only as external project-owner identity binding" in evidence


def test_chg0033_no_counterpart_rule_is_fail_closed() -> None:
    acceptance = (CHANGE_DIR / "acceptance.md").read_text(encoding="utf-8")

    assert "HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART" in acceptance
    assert "regardless of provider readiness" in acceptance


def test_chg0033_final_no_go_closure_is_recorded() -> None:
    acceptance = (CHANGE_DIR / "acceptance.md").read_text(encoding="utf-8")
    closure = (CHANGE_DIR / "evidence" / "20260825-final-no-go-closure.md").read_text(
        encoding="utf-8"
    )

    for marker in (
        "AI_AUTO_REPLY_LIVE_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART_AND_PROVIDER_READINESS",
        "PRIMARY_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART",
        "ADDITIONAL_BLOCKER_PROVIDER=PROVIDER_CREDENTIAL_HTTP_4XX",
        "ADDITIONAL_BLOCKER_BACKLOG=UNREAD_ZERO_NOT_PROVEN",
        "AI_REMAINED_DISABLED=true",
        "AI_PROVIDER_INVOCATIONS=1",
        "AI_REPLY_SEND_INVOCATIONS=0",
        "PLATFORM_SEND_INVOCATIONS=0",
        "UNRELATED_CONVERSATIONS_ENUMERATED=0",
    ):
        assert marker in acceptance
        assert marker in closure
