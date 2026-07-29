"""CLI for deterministic local automatic reply."""
from __future__ import annotations

import argparse
import os
import time
from collections.abc import Sequence
from pathlib import Path

from xianyu_system.worker.autoreply.config import AutoreplyConfig, AutoreplyConfigError
from xianyu_system.worker.autoreply.process import ProcessManager
from xianyu_system.worker.autoreply.service import AutoreplyService
from xianyu_system.worker.upstream_wrapper.config import UpstreamWrapperConfigError
from xianyu_system.worker.upstream_wrapper.client import UpstreamWrapperError

DEFAULT_CONFIG = Path(".local/autoreply.yaml")


def _load_local_env(path: Path = Path(".local/xianyu-upstream.env")) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value)


def _config(path: Path) -> AutoreplyConfig:
    _load_local_env()
    return AutoreplyConfig.from_file(path)


def _service(path: Path) -> AutoreplyService:
    return AutoreplyService(_config(path))


def _print_status(service: AutoreplyService, running: bool = False, pid: int | None = None) -> None:
    status = service.doctor()
    print(f"running={running}")
    if pid:
        print(f"pid={pid}")
    print(f"config_enabled={status.config_enabled}")
    print(f"blocked_reason={status.blocked_reason or 'none'}")
    print(f"listener_status={status.listener_status}")
    print(f"backend_healthy={status.backend_healthy}")
    print(f"listener_connected={status.listener_connected}")
    print(f"account_logged_in={status.account_logged_in}")
    print(f"success_count={status.success_count}")
    print(f"skipped_count={status.skipped_count}")
    print(f"failed_count={status.failed_count}")
    print(f"unknown_count={status.unknown_count}")
    print("secret_values_displayed=false")


def _cmd_doctor(args: argparse.Namespace) -> int:
    service = _service(args.config)
    _print_status(service)
    return 0 if service.doctor().blocked_reason in {None, "DISABLED"} else 1


def _cmd_status(args: argparse.Namespace) -> int:
    config = _config(args.config)
    manager = ProcessManager(config.state_dir)
    pid = manager.read_pid()
    running = manager.is_running(pid)
    service = AutoreplyService(config)
    _print_status(service, running=running, pid=pid if running else None)
    return 0


def _cmd_start(args: argparse.Namespace) -> int:
    config = _config(args.config)
    manager = ProcessManager(config.state_dir)
    started, pid = manager.start(config_path=args.config)
    print(f"started={started}")
    print("running=true")
    print(f"pid={pid}")
    print("secret_values_displayed=false")
    return 0


def _cmd_stop(args: argparse.Namespace) -> int:
    config = _config(args.config)
    manager = ProcessManager(config.state_dir)
    stopped, pid = manager.stop()
    service = AutoreplyService(config)
    service.stop_owned_listener()
    service.write_status(running=False, pid=None)
    print(f"stopped={stopped}")
    if pid:
        print(f"pid={pid}")
    print("running=false")
    print("secret_values_displayed=false")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    service = _service(args.config)
    service.ensure_started()
    service.write_status(running=True, pid=os.getpid())
    try:
        if args.once:
            outcomes = service.poll_once()
            for outcome in outcomes:
                print(f"result={outcome.result}")
            return 0
        while True:
            service.poll_once()
            service.write_status(running=True, pid=os.getpid())
            time.sleep(service.config.poll_seconds)
    except KeyboardInterrupt:
        service.write_status(running=False, pid=None)
        return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m xianyu_system autoreply")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["doctor", "status", "start", "stop", "run"]:
        child = sub.add_parser(name)
        child.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
        if name == "run":
            child.add_argument("--once", action="store_true")
        child.set_defaults(func=globals()[f"_cmd_{name}"])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except (AutoreplyConfigError, UpstreamWrapperConfigError, UpstreamWrapperError) as exc:
        print(f"error={exc}")
        print("secret_values_displayed=false")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
