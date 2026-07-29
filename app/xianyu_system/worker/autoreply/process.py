"""Local background process management for autoreply."""
from __future__ import annotations

import os
import signal
import subprocess
import sys
from pathlib import Path

if os.name == "nt":
    import ctypes
    from ctypes import wintypes


class ProcessManager:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.pid_path = state_dir / "worker.pid"

    def read_pid(self) -> int | None:
        try:
            return int(self.pid_path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            return None

    @staticmethod
    def is_running(pid: int | None) -> bool:
        if not pid or pid <= 0:
            return False
        if os.name == "nt":
            process_query_limited_information = 0x1000
            still_active = 259
            handle = ctypes.windll.kernel32.OpenProcess(process_query_limited_information, False, pid)
            if not handle:
                return False
            try:
                exit_code = wintypes.DWORD()
                if not ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                    return False
                return exit_code.value == still_active
            finally:
                ctypes.windll.kernel32.CloseHandle(handle)
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    def start(self, *, config_path: Path) -> tuple[bool, int]:
        pid = self.read_pid()
        if self.is_running(pid):
            assert pid is not None
            return False, pid
        self.state_dir.mkdir(parents=True, exist_ok=True)
        args = [sys.executable, "-m", "xianyu_system", "autoreply", "run", "--config", str(config_path)]
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, creationflags=creationflags)
        self.pid_path.write_text(str(process.pid), encoding="utf-8", newline="\n")
        return True, process.pid

    def stop(self) -> tuple[bool, int | None]:
        pid = self.read_pid()
        if not self.is_running(pid):
            self.pid_path.unlink(missing_ok=True)
            return False, pid
        assert pid is not None
        os.kill(pid, signal.SIGTERM)
        self.pid_path.unlink(missing_ok=True)
        return True, pid
