import binning_utils as binu
import numpy as np
import pytest


def test_centers_too_few_edges():
    with pytest.raises(AssertionError) as e:
        centers = binu.centers(bin_edges=[0])


def test_centers_simple():
    centers = binu.centers(bin_edges=[0, 1])
    assert len(centers) == 1
    assert centers[0] == 0.5


def test_widths_too_few_edges():
    with pytest.raises(AssertionError) as e:
        centers = binu.widths(bin_edges=[0])


def test_widths_simple():
    centers = binu.widths(bin_edges=[0, 1])
    assert len(centers) == 1
    assert centers[0] == 1.0


def test_power10_lower_bin_edge_decade():
    edge = binu.power10.lower_bin_edge(decade=-1, bin=0, num_bins_per_decade=5)
    assert edge == 0.1

    edge = binu.power10.lower_bin_edge(decade=0, bin=0, num_bins_per_decade=5)
    assert edge == 1.0

    edge = binu.power10.lower_bin_edge(decade=1, bin=0, num_bins_per_decade=5)
    assert edge == 10.0


def test_merge_strictly_monotonic_input():
    strictly_monotonic_increasing = np.linspace(0, 1, 5)
    strictly_monotonic_decreasing = np.linspace(0, 1, 5)
    constant = np.ones(5)

    with pytest.raises(AssertionError) as e:
        binu.merge_low_high_edges(
            low=constant, high=strictly_monotonic_increasing
        )

    with pytest.raises(AssertionError) as e:
        binu.merge_low_high_edges(
            low=strictly_monotonic_increasing, high=constant
        )

    with pytest.raises(AssertionError) as e:
        binu.merge_low_high_edges(
            low=strictly_monotonic_increasing,
            high=strictly_monotonic_decreasing,
        )

    with pytest.raises(AssertionError) as e:
        binu.merge_low_high_edges(
            low=strictly_monotonic_decreasing,
            high=strictly_monotonic_increasing,
        )

    with pytest.raises(AssertionError) as e:
        binu.merge_low_high_edges(
            low=strictly_monotonic_decreasing,
            high=strictly_monotonic_decreasing,
        )


def test_merge_margin():
    low = np.linspace(1, 10, 10)
    high = np.linspace(2, 11, 10)

    edges = binu.merge_low_high_edges(low=low, high=high)
    assert len(edges) == 11

    for i, edge in enumerate(edges):
        assert edge == i + 1

    with pytest.raises(AssertionError) as e:
        edges = binu.merge_low_high_edges(
            low=low, high=high + 0.1, max_relative_margin=1e-2
        )


def test_strict():
    assert binu.is_strictly_monotonic_increasing([0, 1, 2])
    assert not binu.is_strictly_monotonic_increasing([0, 0])
    assert not binu.is_strictly_monotonic_increasing([0, -1])
    assert not binu.is_strictly_monotonic_increasing([0, 1, 2, 2, 3])
