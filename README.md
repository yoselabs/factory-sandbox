# factory-sandbox

**A throwaway proving ground for the factory's unattended loop. This is not a real project.**

Nothing here is meant to be useful. It exists so that an unattended turn has somewhere harmless to
land, and so that when a turn fails we can be confident the failure is the turn and not the
environment. **Nothing in this repository should ever become load-bearing.** If you find yourself
depending on it, you have made a mistake somewhere else.

## Why it is this small

The environment is the point. There is no linter, no type checker, no browser, no network access,
no system library, and no runtime dependency at all — the only thing `make check` needs is `uv` and
a copy of `pytest`. A workspace with a real toolchain costs gigabytes to materialise and gives a
failed run several plausible explanations. This one gives it exactly one.

## The shape

```
pyproject.toml        no runtime dependencies; pytest in the dev group
Makefile              `make check` is the gate, and it is the whole gate
src/sandbox/stats.py  two pure functions
tests/test_stats.py   six tests, two of which fail — one bug, asserted twice
```

## The failing test

`make check` fails on arrival, on purpose. `median()` returns the upper of the two middle values for
an even-sized sample instead of their mean, so `median([4, 1, 3, 2])` gives `3` where the median is
`2.5`. The tests asserting otherwise are right and the function is wrong; the fix is one line and
arithmetic decides it.

There is one bug and two assertions on it, on different samples, because a lone assertion is one
edit away from being "satisfied" — and editing it would mean writing down a claim about medians
that is simply false.

A sandbox whose tests already pass has no job in it.

## Running it

```sh
make check
```
