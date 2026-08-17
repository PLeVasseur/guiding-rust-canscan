# canscan: Specification

## canscan v0.1: CAN log inspection CLI

`canscan` reads CAN bus capture logs in candump text format and produces
summaries for an integration engineer.

One line of candump format:

```text
(1712345678.123456) can0 18FF0102#DEADBEEF11223344
```

That's: `(timestamp) interface can_id#hex_payload`, where `can_id` is 3
hex digits (standard, 11-bit) or 8 hex digits (extended, 29-bit), and the
payload is 0 to 8 bytes of hex.

### Commands

```text
canscan summary <FILE>
    Frame count, capture duration, distinct IDs, overall frames/sec.

canscan top <FILE> --by count|bytes [--limit N]
    The top N IDs ranked by frame count or by payload bytes, with
    per-ID rates. Default limit: 10.

canscan filter <FILE> --id <ID> [--after TS] [--before TS]
    Print matching frames, preserving input format.
    If the input is rejected, filter must not have produced partial output.
```

### Requirements

1. Every command supports `--format text|json`. JSON output must be stable
   enough to consume from a script.
2. Exit code 0 on success, nonzero with a clear message on failure.
3. `summary` on the well-formed `logs/big.log` (4,590,000,000 bytes) must
   complete in under 60 seconds on the classroom machine.
4. The tool is the first of a family of internal utilities. Keep the
   parsing and analysis logic reusable.

### Fixtures

The starter repo ships pre-generated `logs/small.log` (1,000 lines) and
`logs/medium.log` (100,000 lines). Run `make fixtures` to build the
well-formed `logs/big.log`: exactly 90,000,000 valid candump lines and
4,590,000,000 bytes. The source archive doesn't include this file.
