"""Minimal CLI for the localhost-only upstream Pilot wrapper."""
from __future__ import annotations

import argparse
from collections.abc import Sequence

from xianyu_system.worker.upstream_wrapper.client import UpstreamWrapper, UpstreamWrapperError
from xianyu_system.worker.upstream_wrapper.config import UpstreamWrapperConfig, UpstreamWrapperConfigError
from xianyu_system.worker.upstream_wrapper.models import ConfirmedReplyRequest


def _mask(value: str) -> str:
    if len(value) <= 6:
        return "***"
    return f"{value[:3]}...{value[-3:]}"


def _wrapper() -> UpstreamWrapper:
    return UpstreamWrapper(UpstreamWrapperConfig.from_env())


def _cmd_doctor(_: argparse.Namespace) -> int:
    wrapper = _wrapper()
    health = wrapper.health()
    listener = wrapper.listener_status()
    try:
        account = wrapper.account_status()
        account_state = "logged_in" if account.logged_in else "not_logged_in"
    except UpstreamWrapperError:
        account_state = "unknown"
    print(f"backend_health={health.backend_ok}")
    print(f"listener_api_health={health.listener_api_ok}")
    print(f"listener_connected={health.listener_connected}")
    print(f"listener_status={listener}")
    print(f"account_status={account_state}")
    return 0 if health.backend_ok and health.listener_api_ok else 1


def _cmd_account(_: argparse.Namespace) -> int:
    account = _wrapper().account_status()
    print(f"account_ref={_mask(account.account_ref)}")
    print(f"logged_in={account.logged_in}")
    print(f"listener_state={account.listener_state}")
    return 0


def _cmd_listener(args: argparse.Namespace) -> int:
    wrapper = _wrapper()
    if args.listener_command == "status":
        print(f"listener_status={wrapper.listener_status()}")
        return 0
    if args.listener_command == "start":
        result = wrapper.start_listener()
    elif args.listener_command == "stop":
        result = wrapper.stop_listener()
    else:
        raise UpstreamWrapperError("unknown listener command")
    print(f"state={result.state.value}")
    print(f"operation_id={result.operation_id}")
    return 0 if result.state.value == "SUCCESS" else 1


def _cmd_messages(args: argparse.Namespace) -> int:
    events = _wrapper().list_recent_inbound_events(limit=args.limit, match_text=args.match_text)
    for event in events:
        marker = "matched" if args.match_text and event.text == args.match_text else "redacted"
        print(
            " ".join(
                [
                    f"internal_message_id={event.internal_message_id}",
                    f"account_ref={_mask(event.account_ref)}",
                    f"conversation_ref={_mask(event.conversation_ref)}",
                    f"direction={event.direction}",
                    f"source={event.source}",
                    f"text={marker}",
                ]
            )
        )
    print(f"count={len(events)}")
    return 0


def _cmd_reply(args: argparse.Namespace) -> int:
    request = ConfirmedReplyRequest(
        internal_message_id=args.message_id,
        text=args.text,
        confirm=bool(args.confirm),
    )
    result = _wrapper().send_confirmed_reply(request)
    print(f"state={result.state.value}")
    print(f"operation_id={result.operation_id}")
    if result.detail:
        print(f"detail={result.detail}")
    return 0 if result.state.value == "SUCCESS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m xianyu_system upstream")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor").set_defaults(func=_cmd_doctor)
    sub.add_parser("account").set_defaults(func=_cmd_account)

    listener = sub.add_parser("listener")
    listener_sub = listener.add_subparsers(dest="listener_command", required=True)
    for command in ["status", "start", "stop"]:
        listener_sub.add_parser(command).set_defaults(func=_cmd_listener)

    messages = sub.add_parser("messages")
    messages.add_argument("--limit", type=int, default=20)
    messages.add_argument("--match-text")
    messages.set_defaults(func=_cmd_messages)

    reply = sub.add_parser("reply")
    reply.add_argument("--message-id", required=True)
    reply.add_argument("--text", required=True)
    reply.add_argument("--confirm", action="store_true")
    reply.set_defaults(func=_cmd_reply)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except (UpstreamWrapperConfigError, UpstreamWrapperError) as exc:
        print(f"error={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
