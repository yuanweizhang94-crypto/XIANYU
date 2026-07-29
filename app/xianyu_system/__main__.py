"""CLI entry point for XIANYU local tools."""
from __future__ import annotations

import sys

from xianyu_system.worker.upstream_wrapper.cli import main as upstream_main


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        print("usage: python -m xianyu_system upstream <command> [options]")
        return 0
    command = args.pop(0)
    if command == "upstream":
        return upstream_main(args)
    print(f"unknown command: {command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
