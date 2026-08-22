import pytest

from sandbox.stats import StatsError, mean, median


def test_mean_of_a_sample():
    assert mean([1, 2, 3, 4]) == 2.5


def test_mean_of_an_empty_sample_is_refused():
    with pytest.raises(StatsError):
        mean([])


def test_median_of_an_odd_sample_is_the_middle_value():
    assert median([3, 1, 2]) == 2


def test_median_of_an_even_sample_is_the_mean_of_the_two_middle_values():
    # Four values, sorted: 1, 2, 3, 4. The two middle ones are 2 and 3, so the median is 2.5.
    # There is no single middle element to return; returning 3 (or 2) is not the median of this
    # sample under any definition.
    assert median([4, 1, 3, 2]) == 2.5


def test_median_of_a_two_element_sample():
    assert median([10, 20]) == 15


def test_median_of_an_empty_sample_is_refused():
    with pytest.raises(StatsError):
        median([])
