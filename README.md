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
src/sandbox/stats.py  three pure functions
tests/test_stats.py   eleven tests, two of which fail — one bug, asserted twice
```

## The failing test

`make check` fails on arrival, on purpose. **`top_n()` sorts its argument in place**, so it hands
back the right answer and leaves the caller's list rearranged behind it:

```python
sample = [4, 1, 3, 2]
top_n(sample, 2)     # -> [4, 3], which is correct
sample               # -> [4, 3, 2, 1], which is not what the caller passed in
```

The first line of `stats.py` says these are pure functions. A function that reorders its argument is
not one, and the caller still owns that list. The fix is one line; nothing about it is a matter of
taste.

There is one bug and two assertions on it, on different samples and different `n`, because a lone
assertion is one edit away from being "satisfied" — and deleting either of these means writing down
that a function documented as pure may rearrange its caller's data.

**Note what does *not* fail.** `test_top_n_returns_the_largest_values` passes with the bug in place,
because the return value was never wrong. That is deliberate: the first bug this repository carried
(`median()` returning the upper of two middle values, fixed in `c3ed3da`) was a wrong *answer*, and
a second bug of the same shape would test less than a different one. This one is a wrong *effect*.
An agent that only reads the failure count sees "two tests failing in `top_n`" and can still get it
backwards by rewriting the arithmetic that was already correct.

A sandbox whose tests already pass has no job in it.

## Running it

```sh
make check
```
