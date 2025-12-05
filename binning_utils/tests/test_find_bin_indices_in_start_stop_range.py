import binning_utils as bu
import pytest


def test_invalid_bin_edges():
    with pytest.raises(AssertionError):
        bu.find_bin_indices_in_start_stop_range(
            bin_edges=[1], start=-1, stop=1
        )


def test_invalid_range():
    with pytest.raises(AssertionError):
        bu.find_bin_indices_in_start_stop_range(
            bin_edges=[1, 2], start=10, stop=1
        )


def test_invalid_edges_increase():
    with pytest.raises(AssertionError):
        bu.find_bin_indices_in_start_stop_range(
            bin_edges=[2, 1], start=1, stop=2
        )


def test_minimal():
    r, f = bu.find_bin_indices_in_start_stop_range(
        bin_edges=[1, 2],
        start=1,
        stop=2,
        return_if_bin_is_fully_contained=True,
    )
    assert len(r) == 1
    assert r[0] == 0

    assert len(f) == len(r)
    assert f[0] == True


def test_complex_none_fully_contained():
    r, f = bu.find_bin_indices_in_start_stop_range(
        bin_edges=[1, 2, 3],
        start=1.5,
        stop=2.5,
        return_if_bin_is_fully_contained=True,
    )
    assert len(r) == 2
    assert r[0] == 0
    assert r[1] == 1

    assert len(f) == 2
    assert f[0] == False
    assert f[1] == False


def test_complex_one_fully_contained():
    r, f = bu.find_bin_indices_in_start_stop_range(
        bin_edges=[1, 2, 3, 4],
        start=1.5,
        stop=3.5,
        return_if_bin_is_fully_contained=True,
    )
    assert len(r) == 3
    assert r[0] == 0
    assert r[1] == 1
    assert r[2] == 2

    assert len(f) == 3
    assert f[0] == False
    assert f[1] == True
    assert f[2] == False


def test_only_fully_contained():
    r, f = bu.find_bin_indices_in_start_stop_range(
        bin_edges=[1, 2, 3, 4, 5],
        start=2,
        stop=4,
        return_if_bin_is_fully_contained=True,
    )
    assert len(r) == 2
    assert r[0] == 1
    assert r[1] == 2

    assert len(f) == 2
    assert f[0] == True
    assert f[1] == True
