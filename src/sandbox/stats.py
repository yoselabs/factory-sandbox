"""Two summary statistics over a sequence of numbers.

Pure functions, no I/O, no dependencies. If something here is wrong, it is wrong for a reason
arithmetic can settle, not a reason taste can.
"""

from __future__ import annotations

from collections.abc import Sequence


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
    return ordered[len(ordered) // 2]
