.PHONY: check test bootstrap

# `make check` is the gate. The factory runs this exact target as a foreign workspace's
# `test_command` -- it must be the whole of what "passing" means here, and it must need nothing
# but uv and this repository.
check: test

bootstrap:
	@uv sync

test:
	@uv run pytest
