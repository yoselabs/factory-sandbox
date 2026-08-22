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
src/sandbox/stats.py  four pure functions
tests/test_stats.py   fifteen tests, two of which fail — one bug, asserted twice
```

## The failing test

`make check` fails on arrival, on purpose. **`summarise()` takes a mutable default argument**, so
every caller that does not supply one gets the *same* mapping — and a summary already handed out
changes when the next one is taken:

```python
first = summarise([1, 2, 3])    # -> {'mean': 2, 'median': 2}
summarise([10, 20, 30])         # a second, unrelated call
first                           # -> {'mean': 20.0, 'median': 20}, retroactively
```

Nothing about the arithmetic is wrong. `summarise([1, 2, 3])` computes 2 and 2, correctly, every
time. What is wrong is that the answer does not stay put: correctness here depends on the call
history rather than on the argument. The fix is the standard `None` sentinel and is one line.

There is one bug and two assertions on it, on different samples, because a lone assertion is one
edit away from being "satisfied" — and deleting either means writing down that a summary of one
sample may report another sample's numbers.

**Three bugs, three defect classes, on purpose.** This repository's job is to exercise an
unattended turn, and a second instance of a class already tested measures less than a new one:

| bug | fixed in | what was wrong |
|---|---|---|
| `median()` returned the upper of two middle values | `c3ed3da` | the **answer** |
| `top_n()` sorted the caller's list in place | `9fcf760` | the **effect** — the answer was right |
| `summarise()` shares one default mapping | open | the **duration** — the answer is right, then stops being right |

Each one leaves at least one test *passing* on the function that is broken, so an agent reading the
failure count alone gets the wrong idea about what to change. Here `summarise([1, 2, 3])` returning
the correct pair is asserted and passes; rewriting how the mean is computed fixes nothing and breaks
that.

A sandbox whose tests already pass has no job in it.

## Running it

```sh
make check
```
