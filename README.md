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
src/sandbox/stats.py  five pure functions
tests/test_stats.py   twenty tests, two of which fail — one bug, asserted twice
```

## The failing test

`make check` fails on arrival, on purpose. **`summarise_many()` writes as it goes**, so a call that
refuses part-way through has already put half its work into the caller's mapping:

```python
row = {"id": 7}
summarise_many({"a": [1, 2, 3], "b": []}, into=row)   # raises StatsError on the empty "b"
row                                                   # -> {'id': 7, 'a.mean': 2, 'a.median': 2}
```

Its docstring says all or nothing. It means it: a caller that sees the exception cannot tell which
of the keys now in its mapping were already there and which this call added, so a half-written
report is worse than no report. The fix is to compute everything first and publish it at the end —
two lines, and no judgement call about what the right behaviour is.

There is one bug and two assertions on it, on different samples failing at different points, because
a lone assertion is one edit away from being "satisfied" — and deleting either means writing down
that a function documented all-or-nothing may leave half its work behind.

**Four bugs, four defect classes.** This repository's job is to exercise an unattended turn, and a
second instance of a class already tested measures less than a new one:

| bug | fixed in | what was wrong |
|---|---|---|
| `median()` returned the upper of two middle values | `c3ed3da` | the **answer** |
| `top_n()` sorted the caller's list in place | `9fcf760` | the **effect on success** — the answer was right |
| `summarise()` shared one default mapping | `a9be992` | the **duration** — right when handed over, then not |
| `summarise_many()` writes as it goes | open | the **effect on failure** — success is correct; refusal is not |

The fourth is the closest to an earlier one, and worth naming rather than pretending otherwise: it
and `top_n` are both "wrong effect". They are separated by *which path* — `top_n` corrupted the
caller on the path where it succeeded, and this one only misbehaves on the path where it refuses,
which no test of the happy path can reach. That is a real distinction and a narrower one than the
first three were from each other.

Each bug leaves at least one test *passing* on the function that is broken, so an agent reading the
failure count alone gets the wrong idea about what to change. Here all three happy-path tests for
`summarise_many` pass; the arithmetic and the `into` contract are already right.

A sandbox whose tests already pass has no job in it.

## Running it

```sh
make check
```
