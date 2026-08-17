# canscan-starter (Project A)

Starter repository for Project A (`canscan`) from the Guiding Rust course.

- [Student course book](https://petelevasseur.com/guiding-rust/)
- [Training resources](https://petelevasseur.com/training/)
- Workshop snapshot: `workshop-2026-08-19`

Use this repository as a GitHub template for your pair, or clone it directly.
The root CI is intentionally red at first because there is no root crate.
Creating the crate and a compiling participant-owned skeleton is milestone M0.

## Contents

- `SPEC.md`: the specification as handed out during the course.
- `logs/small.log` and `logs/medium.log`: fixtures, pre-generated. Run
  `make fixtures` once to generate the well-formed `logs/big.log` used by
  milestone M3. It's exactly 90,000,000 lines and 4,590,000,000 bytes,
  so start the disk-intensive build early. The build publishes the file
  only after exact validation succeeds; `big.log` isn't shipped in the
  starter archive.
- `REVIEW-LOG.md`: the pair's running log, with a template inside.
- `.github/workflows/ci.yml`: fmt, `clippy -D warnings`, test.
- `exercises/smell-sample/`: the module for the Day 1 morning smell
  exercise. It compiles without warnings and its test passes.
- `exercises/two-skeletons/`: pre-generated results for the "One Task,
  Two Skeletons" exercise, with tests that show the defects.

Rust 1.89.0 is pinned in `rust-toolchain.toml`; rustup installs it
automatically on the first cargo command.

`make fixture-smoke` exercises generation and validation with a small
temporary file. `make validate-fixture` performs exact syntax, line-count,
byte-count, and SHA-256 validation of an existing canonical `logs/big.log`.
Its expected SHA-256 is
`678f6419558379b8ca0a639a065129bb70d04c15bac80ac86cf65df42ae1f1f7`.

## Note: there's no crate at the root

Milestone M0 is to create one: decide the shape, write the skeleton by
hand with `todo!()` bodies, and only then
generate. CI fails until a crate exists, which matches the intended order
of work.
