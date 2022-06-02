import binning_utils as binu
import numpy as np
import pytest


def test_power10_invalid_bin():
    with pytest.raises(AssertionError) as e:
        binu.power10.lower_bin_edge(decade=-1, bin=5, num_bins_per_decade=5)

    with pytest.raises(AssertionError) as e:
        binu.power10.lower_bin_edge(decade=-1, bin=-1, num_bins_per_decade=5)

    with pytest.raises(AssertionError) as e:
        binu.power10.lower_bin_edge(decade=0, bin=0, num_bins_per_decade=0)


def test_make_space_combis_invalid():
    with pytest.raises(AssertionError) as e:
        combis = binu.power10.make_decade_and_bin_combinations(
            start_decade=0,
            start_bin=0,
            stop_decade=1,
            stop_bin=0,
            num_bins_per_decade=0,
        )

    with pytest.raises(AssertionError) as e:
        combis = binu.power10.make_decade_and_bin_combinations(
            start_decade=0,
            start_bin=0,
            stop_decade=-1,
            stop_bin=0,
            num_bins_per_decade=5,
        )

def test_make_space_combis():
    combis = binu.power10.make_decade_and_bin_combinations(
        start_decade=0,
        start_bin=0,
        stop_decade=1,
        stop_bin=0,
        num_bins_per_decade=5,
    )
    assert len(combis) == 5
    assert combis[0] == (0, 0)
    assert combis[1] == (0, 1)
    assert combis[2] == (0, 2)
    assert combis[3] == (0, 3)
    assert combis[4] == (0, 4)


def test_make_space_combis_start_equal_stop():
    combis = binu.power10.make_decade_and_bin_combinations(
        start_decade=0,
        start_bin=1,
        stop_decade=0,
        stop_bin=1,
        num_bins_per_decade=5,
    )
    assert len(combis) == 0


def test_power10_space():
    space = binu.power10.space(
        start_decade=0,
        start_bin=0,
        stop_decade=3,
        stop_bin=0,
        num_bins_per_decade=5,
    )
    assert len(space) == 15

    actual_power_ratios = space[1:] / space[0:-1]
    desired_power_ratio = binu.power10.lower_bin_edge(
        decade=0, bin=1, num_bins_per_decade=5,
    )

    np.testing.assert_allclose(
        actual=actual_power_ratios, desired=desired_power_ratio,
    )



def test_find_upper_lower():
    x = 1.0
    d, b = binu.power10.find_upper_decade_and_bin(x=x, num_bins_per_decade=5)
    assert d == 0 and b == 1

    d, b = binu.power10.find_lower_decade_and_bin(x=x, num_bins_per_decade=5)
    assert d == 0 and b == 0


def test_find_upper_lower_exotic():
    d, b = binu.power10.find_upper_decade_and_bin(
        x=0.3e-9,
        num_bins_per_decade=5
    )
    assert d == -9, b == 2


def test_increase_decrease():
    p = (0, 0)
    for i in range(100):
        p = binu.power10.decade_bin_increase(p[0], p[1], num_bins_per_decade=5)
    assert p == (20, 0)
    for i in range(100):
        p = binu.power10.decade_bin_decrease(p[0], p[1], num_bins_per_decade=5)
    assert p == (0, 0)


def test_is_less():
    assert not binu.power10.decade_bin_is_less((0, 0), (-1, 0))
    assert not binu.power10.decade_bin_is_less((0, 0), (0, 0))
    assert binu.power10.decade_bin_is_less((0, 0), (0, 1))
    assert binu.power10.decade_bin_is_less((0, 0), (1, 0))
