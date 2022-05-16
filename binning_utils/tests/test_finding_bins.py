import binning_utils as binu
import numpy as np
import pytest


assert_close = np.testing.assert_almost_equal


def test_finding_bin_index_in_edges():
    VALUE = 0
    UNDERFLOW = 1
    BIN_IDX = 2
    OVERFLOW = 3
    bin_edges = np.linspace(0, 1, 5)
    scenarios = [
        (-0.1, True, 0, False),
        (0.0, False, 0, False),
        (0.1, False, 0, False),
        (0.23, False, 0, False),
        (0.26, False, 1, False),
        (0.49, False, 1, False),
        (0.51, False, 2, False),
        (0.74, False, 2, False),
        (0.76, False, 3, False),
        (0.99, False, 3, False),
        (1.0, False, 4, True),
        (1.1, False, 4, True),
    ]

    for scenario in scenarios:
        print(scenario)
        underflow, bin_idx, overflow = binu.find_bin_in_edges(
            bin_edges=bin_edges, value=scenario[VALUE]
        )

        assert scenario[UNDERFLOW] == underflow
        assert scenario[BIN_IDX] == bin_idx
        assert scenario[OVERFLOW] == overflow


def test_finding_bin_index_in_centers():
    VALUE = 0
    UNDERFLOW = 1
    LOWER_IDX = 2
    OVERFLOW = 3
    UPPER_IDX = 4
    LOWER_WEIGHT = 5
    bin_centers = np.linspace(0, 1, 6)
    # 0    1     2    3     4    5
    # .0,  .2,  .4,   .6,   .8   1.
    scenarios = [
        (-0.1, True, 0, False, 1, 0.0),
        (0.0, False, 0, False, 1, 1.0),
        (0.1, False, 0, False, 1, 0.5),
        (0.19, False, 0, False, 1, 0.05),
        (0.3, False, 1, False, 2, 0.5),
        (0.41, False, 2, False, 3, 0.95),
        (0.5, False, 2, False, 3, 0.5),
        (0.75, False, 3, False, 4, 0.25),
        (0.8, False, 4, False, 5, 1.0),
        (0.95, False, 4, False, 5, 0.25),
        (1.0, False, 5, True, 6, 1.0),
        (1.1, False, 5, True, 6, 1.0),
    ]

    for scenario in scenarios:
        print(scenario)
        match = binu.find_bins_in_centers(
            bin_centers=bin_centers, value=scenario[VALUE]
        )

        assert scenario[UNDERFLOW] == match["underflow"]
        assert scenario[OVERFLOW] == match["overflow"]
        assert scenario[LOWER_IDX] == match["lower_bin"]
        assert scenario[UPPER_IDX] == match["upper_bin"]
        assert_close(scenario[LOWER_WEIGHT], match["lower_weight"])
        assert_close(match["lower_weight"] + match["upper_weight"], 1.0)


def test_finding_bin_index_in_circular():
    VALUE = 0
    UNDERFLOW = 1
    LOWER_IDX = 2
    OVERFLOW = 3
    UPPER_IDX = 4
    LOWER_WEIGHT = 5
    bin_centers = np.linspace(0, 1, 3)
    # 0., .5, 1.
    scenarios = [
        (0.0, False, 0, False, 1, 1.0),
        (-1e-6, True, 0, False, 1, 0.0),
        (1 - 1e-6, False, 1, False, 2, 2e-6),
        (1, False, 2, True, 3, 1.0),
    ]

    for scenario in scenarios:
        print(scenario)
        match = binu.find_bins_in_centers(
            bin_centers=bin_centers, value=scenario[VALUE]
        )

        assert scenario[UNDERFLOW] == match["underflow"]
        assert scenario[OVERFLOW] == match["overflow"]
        assert scenario[LOWER_IDX] == match["lower_bin"]
        assert scenario[UPPER_IDX] == match["upper_bin"]
        assert_close(scenario[LOWER_WEIGHT], match["lower_weight"])
        assert_close(match["lower_weight"] + match["upper_weight"], 1.0)
