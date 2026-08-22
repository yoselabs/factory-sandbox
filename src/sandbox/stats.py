"""Two summary statistics over a sequence of numbers.

Pure functions, no I/O, no dependencies. If something here is wrong, it is wrong for a reason
arithmetic can settle, not a reason taste can.
"""

from __future__ import annotations

from collections.abc import MutableMapping, Sequence


class StatsError(ValueError):
    """The input cannot be summarised. An empty sample has no mean and no median."""


def mean(values: Sequence[float]) -> float:
    """The arithmetic mean."""
    if not values:
        raise StatsError("mean of an empty sequence is undefined")
    return sum(values) / len(values)


def median(values: Sequence[float]) -> float:
    """The middle value of the sample, sorted.

    For an odd-sized sample that is the single middle element. For an even-sized sample the
    median is the mean of the two middle elements -- there is no single middle one to return.
    """
    if not values:
        raise StatsError("median of an empty sequence is undefined")
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def top_n(values: Sequence[float], n: int) -> list[float]:
    """The `n` largest values, largest first.

    Fewer than `n` values in the sample means all of them, in order. `n == 0` is an empty list,
    not an error -- "give me nothing" is a question with an answer. A negative `n` is refused,
    because there is no sample it could describe.
    """
    if n < 0:
        raise StatsError("cannot take a negative number of values")
    ordered = sorted(values, reverse=True)
    return ordered[:n]


def summarise(
    values: Sequence[float], into: MutableMapping[str, float] | None = None
) -> MutableMapping[str, float]:
    """Mean and median of `values`, written into `into` and returned.

    `into` exists so a caller that already has a mapping can have the numbers written straight
    into it -- a report being assembled, a row being built -- rather than getting a new mapping
    back and merging it by hand. Called without one, you get a mapping of your own.
    """
    if into is None:
        into = {}
    into["mean"] = mean(values)
    into["median"] = median(values)
    return into
