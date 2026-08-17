.PHONY: check fixtures validate-fixture fixture-smoke clean-fixtures

check:
	cargo fmt --all --check
	cargo clippy --all-targets -- -D warnings
	cargo test

# small.log and medium.log ship pre-generated. This target generates the
# one file too large to ship: the 4.59 GB big.log used by milestone M3.
# Publication is atomic and occurs only after syntax, size, line-count,
# and checksum validation succeeds. Campaigns may set CANSCAN_BIG_FIXTURE so
# the generated payload stays outside OpenCode's model-workspace scan.
fixtures:
	python3 tools/big_fixture.py build

validate-fixture:
	python3 tools/big_fixture.py validate

fixture-smoke:
	python3 tools/big_fixture.py smoke

clean-fixtures:
	rm -f logs/big.log logs/.big.log.tmp
