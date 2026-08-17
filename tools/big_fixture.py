#!/usr/bin/env python3
"""Build and verify the canonical valid candump performance fixture."""

import argparse
import hashlib
import os
from pathlib import Path
import random
import re
import tempfile


CAN_IDS = (
    0x18FF0102,
    0x0CF00400,
    0x18FEF100,
    0x0CFE6CEE,
    0x18ECFF00,
    0x18EBFF00,
    0x0CF00300,
    0x18FEEE00,
    0x18FEF200,
    0x1CFEB000,
)
HEX_DIGITS = "0123456789ABCDEF"
LINE_PATTERN = re.compile(
    rb"\([0-9]{10}\.[0-9]{6}\) can0 [0-9A-F]{8}#[0-9A-F]{16}\n"
)
CHUNK_LINES = 100_000
CANONICAL_LINES = 90_000_000
CANONICAL_BYTES = 4_590_000_000
CANONICAL_SHA256 = (
    "678f6419558379b8ca0a639a065129bb70d04c15bac80ac86cf65df42ae1f1f7"
)
SMOKE_LINES = 100_001
SMOKE_SHA256 = (
    "09b1ea930ff628ca6266f47aee4c964a2a63d0b340fa74d7a32c1605a71bf381"
)


def fixture_chunks(line_count: int):
    rng = random.Random(43)
    timestamp = 1_712_345_678.0
    written = 0

    while written < line_count:
        chunk_lines = min(CHUNK_LINES, line_count - written)
        can_ids = rng.choices(CAN_IDS, k=chunk_lines)
        payloads = "".join(rng.choices(HEX_DIGITS, k=16 * chunk_lines))
        lines = [
            "(%.6f) can0 %08X#%s"
            % (
                timestamp + index * 0.0004,
                can_ids[index],
                payloads[16 * index : 16 * index + 16],
            )
            for index in range(chunk_lines)
        ]
        yield ("\n".join(lines) + "\n").encode("ascii")
        timestamp += chunk_lines * 0.0004
        written += chunk_lines


def write_fixture(path: Path, line_count: int) -> None:
    with path.open("xb") as output:
        for chunk in fixture_chunks(line_count):
            output.write(chunk)


def validate_fixture(
    path: Path, expected_lines: int, expected_bytes: int, expected_sha256: str | None
) -> str:
    digest = hashlib.sha256()
    line_count = 0
    byte_count = 0

    with path.open("rb") as fixture:
        for line_count, line in enumerate(fixture, start=1):
            digest.update(line)
            byte_count += len(line)
            if LINE_PATTERN.fullmatch(line) is None:
                raise ValueError(f"invalid candump syntax at line {line_count}")

    actual_sha256 = digest.hexdigest()
    if line_count != expected_lines:
        raise ValueError(f"expected {expected_lines} lines, found {line_count}")
    if byte_count != expected_bytes:
        raise ValueError(f"expected {expected_bytes} bytes, found {byte_count}")
    if expected_sha256 is not None and actual_sha256 != expected_sha256:
        raise ValueError(
            f"expected SHA-256 {expected_sha256}, found {actual_sha256}"
        )
    return actual_sha256


def checked_build(
    output: Path,
    expected_lines: int,
    expected_bytes: int,
    expected_sha256: str | None,
) -> str:
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.unlink(missing_ok=True)
    try:
        write_fixture(temporary, expected_lines)
        actual_sha256 = validate_fixture(
            temporary,
            expected_lines,
            expected_bytes,
            expected_sha256,
        )
        os.replace(temporary, output)
        return actual_sha256
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def build_canonical(output: Path) -> None:
    checked_build(
        output,
        CANONICAL_LINES,
        CANONICAL_BYTES,
        CANONICAL_SHA256,
    )


def run_smoke(line_count: int) -> None:
    if not 1 <= line_count <= CANONICAL_LINES:
        raise ValueError(f"--lines must be between 1 and {CANONICAL_LINES}")

    with tempfile.TemporaryDirectory(prefix="canscan-fixture-") as directory:
        path = Path(directory) / "smoke.log"
        expected_sha256 = SMOKE_SHA256 if line_count == SMOKE_LINES else None
        actual_sha256 = checked_build(
            path,
            line_count,
            line_count * 51,
            expected_sha256,
        )
    print(f"smoke fixture valid: {line_count} lines, SHA-256 {actual_sha256}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    default_path = Path(os.environ.get("CANSCAN_BIG_FIXTURE", "logs/big.log"))

    build_parser = subparsers.add_parser("build", help="build logs/big.log")
    build_parser.add_argument(
        "path", nargs="?", type=Path, default=default_path
    )

    validate_parser = subparsers.add_parser(
        "validate", help="perform exact validation of a canonical fixture"
    )
    validate_parser.add_argument(
        "path", nargs="?", type=Path, default=default_path
    )

    smoke_parser = subparsers.add_parser(
        "smoke", help="build and validate a small temporary fixture"
    )
    smoke_parser.add_argument("--lines", type=int, default=SMOKE_LINES)

    args = parser.parse_args()
    if args.command == "build":
        build_canonical(args.path)
        print(
            f"published {args.path}: {CANONICAL_LINES} lines, "
            f"{CANONICAL_BYTES} bytes, SHA-256 {CANONICAL_SHA256}"
        )
    elif args.command == "validate":
        actual_sha256 = validate_fixture(
            args.path,
            CANONICAL_LINES,
            CANONICAL_BYTES,
            CANONICAL_SHA256,
        )
        print(f"canonical fixture valid: {args.path}, SHA-256 {actual_sha256}")
    else:
        run_smoke(args.lines)


if __name__ == "__main__":
    main()
