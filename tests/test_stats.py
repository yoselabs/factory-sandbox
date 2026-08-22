import pytest

from sandbox.stats import StatsError, mean, median, summarise, summarise_many, top_n


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


def test_summarise_reports_the_mean_and_the_median():
    assert summarise([1, 2, 3]) == {"mean": 2, "median": 2}


def test_summarise_writes_into_a_mapping_the_caller_already_has():
    row = {"id": 7}
    returned = summarise([2, 4], into=row)
    # The caller's own mapping is what gets the numbers -- that is the whole point of the
    # parameter. Building a copy and leaving `row` untouched would not be this function.
    assert row["mean"] == 3
    assert row["median"] == 3
    assert row["id"] == 7
    assert returned is row


def test_a_summary_does_not_change_when_a_later_summary_is_taken():
    # A value you have already been handed does not change afterwards. `first` summarises
    # [1, 2, 3] and its mean is 2 -- before the second call, after the second call, and for as
    # long as the caller holds it.
    first = summarise([1, 2, 3])
    summarise([10, 20, 30])
    assert first["mean"] == 2


def test_two_samples_get_two_answers():
    # Different samples, different medians: [4, 4] has median 4, [1, 3] has median 2. Asserted
    # separately from the test above, on different numbers, because one assertion about leaked
    # state is one edit away from being "satisfied" -- and deleting either means writing down
    # that a summary of one sample may report another sample's numbers.
    a = summarise([4, 4])
    b = summarise([1, 3])
    assert a["median"] == 4
    assert b["median"] == 2


def test_summarise_many_reports_every_sample():
    assert summarise_many({"a": [1, 2, 3], "b": [10, 20]}) == {
        "a.mean": 2,
        "a.median": 2,
        "b.mean": 15,
        "b.median": 15,
    }


def test_summarise_many_writes_into_a_mapping_the_caller_already_has():
    row = {"id": 7}
    returned = summarise_many({"a": [2, 4]}, into=row)
    assert row["a.mean"] == 3
    assert row["id"] == 7
    assert returned is row


def test_summarise_many_refuses_an_empty_sample():
    with pytest.raises(StatsError):
        summarise_many({"a": [1, 2], "b": []})


def test_a_refused_call_leaves_the_caller_s_mapping_untouched():
    # All or nothing, and this is the half that is hard: the call fails on "b", but "a" was
    # already summarised by then. The caller sees the exception and its mapping must look exactly
    # as it did before -- otherwise "did this call write anything?" has no answer.
    row = {"id": 7}
    with pytest.raises(StatsError):
        summarise_many({"a": [1, 2, 3], "b": []}, into=row)
    assert row == {"id": 7}


def test_a_refused_call_writes_nothing_however_far_it_got():
    # A different arrangement and a different failure point, because one assertion about a partial
    # write is one edit away from being "satisfied" -- and deleting either means writing down that
    # a function documented all-or-nothing may leave half its work behind.
    row = {}
    with pytest.raises(StatsError):
        summarise_many({"x": [5], "y": [6, 8], "z": []}, into=row)
    assert row == {}
