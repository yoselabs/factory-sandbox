import pytest

from sandbox.stats import StatsError, mean, median, top_n


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


def test_top_n_returns_the_largest_values():
    assert top_n([4, 1, 3, 2], 2) == [4, 3]


def test_top_n_of_more_than_the_sample_holds_is_the_whole_sample():
    assert top_n([2, 1], 5) == [2, 1]


def test_top_n_refuses_a_negative_count():
    with pytest.raises(StatsError):
        top_n([1, 2, 3], -1)


def test_top_n_leaves_the_caller_s_list_in_the_order_it_was_given():
    # `stats.py` says, in its first line, that these are pure functions. A pure function does not
    # reorder its argument. The caller still owns this list and may be relying on its order --
    # reading it back, indexing into it, comparing it to another list. The return value being
    # right does not make the side effect acceptable.
    sample = [4, 1, 3, 2]
    top_n(sample, 2)
    assert sample == [4, 1, 3, 2]


def test_top_n_does_not_reorder_a_second_sample_either():
    # A different sample and a different `n`, because one assertion about a side effect is one
    # edit away from being "satisfied" -- and deleting either of these two means writing down that
    # a function documented as pure is allowed to rearrange its caller's data.
    sample = [7, 2, 9]
    assert top_n(sample, 1) == [9]
    assert sample == [7, 2, 9]
