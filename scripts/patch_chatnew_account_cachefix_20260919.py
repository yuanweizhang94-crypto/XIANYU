from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


BASE_SHA256 = "7d58515be1e86a9370b8fcce91a08943e4c9df253838477f0eba4e92e0294843"
FIXED_SHA256 = "5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b"

OLD_SNIPPET = (
    "if(t)T(b=>[...b,...y]);else{T(y);const b=D.current;"
)

NEW_SNIPPET = (
    "if(t)T(b=>{const F=[...b,...y];"
    "return Pe.current[e]={convs:F,hasMore:g.hasMore,cursor:g.nextCursor},F});"
    "else{Pe.current[e]={convs:y,hasMore:g.hasMore,cursor:g.nextCursor},"
    "T(y);const b=D.current;"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform_text(text: str) -> str:
    count = text.count(OLD_SNIPPET)
    if count != 1:
        raise ValueError(f"expected exactly one production preimage, found {count}")
    return text.replace(OLD_SNIPPET, NEW_SNIPPET, 1)


def patch_bytes(data: bytes) -> bytes:
    if sha256_bytes(data) != BASE_SHA256:
        raise ValueError("input chunk SHA256 does not match locked production preimage")
    text = data.decode("utf-8")
    fixed = transform_text(text).encode("utf-8")
    if sha256_bytes(fixed) != FIXED_SHA256:
        raise ValueError("patched chunk SHA256 does not match locked production output")
    return fixed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the 2026-09-19 XIANYU ChatNew account-cache truth hotfix."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    fixed = patch_bytes(args.input.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(fixed)
    print(f"BASE_SHA256={BASE_SHA256}")
    print(f"FIXED_SHA256={FIXED_SHA256}")
    print("CHATNEW_ACCOUNT_CACHEFIX=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
