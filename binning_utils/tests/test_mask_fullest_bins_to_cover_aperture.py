import numpy as np
import binning_utils as bu
import pytest


def test_len_zero():
    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[], bin_apertures=[], aperture=0.0
    )
    assert len(mask) == 0


def test_mask_fullest_bins_to_cover_aperture():
    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[1, 2, 3, 4], bin_apertures=[1, 1, 1, 1], aperture=2.0
    )
    np.testing.assert_array_equal(mask, [0, 0, 1, 1])

    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[4, 3, 2, 1], bin_apertures=[1, 1, 1, 1], aperture=2.0
    )
    np.testing.assert_array_equal(mask, [1, 1, 0, 0])

    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[1, 4, 3, 1], bin_apertures=[1, 1, 1, 1], aperture=2.0
    )
    np.testing.assert_array_equal(mask, [0, 1, 1, 0])


def test_round_to_ceiling():
    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[2, 1], bin_apertures=[1, 1], aperture=0.1
    )
    np.testing.assert_array_equal(mask, [1, 0])

    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[2, 1], bin_apertures=[1, 1], aperture=1.1
    )
    np.testing.assert_array_equal(mask, [1, 1])

    mask = bu.mask_fullest_bins_to_cover_aperture(
        bin_counts=[2, 1], bin_apertures=[1, 1], aperture=2.0
    )
    np.testing.assert_array_equal(mask, [1, 1])


def teast_bad_inputs():
    with pytest.raises(AssertionError) as e:
        mask = bu.mask_fullest_bins_to_cover_aperture(
            bin_counts=[], bin_apertures=[], aperture=1.0
        )

    with pytest.raises(AssertionError) as e:
        mask = bu.mask_fullest_bins_to_cover_aperture(
            bin_counts=[1], bin_apertures=[1], aperture=2.0
        )

    with pytest.raises(AssertionError) as e:
        mask = bu.mask_fullest_bins_to_cover_aperture(
            bin_counts=[1], bin_apertures=[1], aperture=-1
        )

    with pytest.raises(AssertionError) as e:
        mask = bu.mask_fullest_bins_to_cover_aperture(
            bin_counts=[1], bin_apertures=[0], aperture=-1
        )

    with pytest.raises(AssertionError) as e:
        mask = bu.mask_fullest_bins_to_cover_aperture(
            bin_counts=[-1], bin_apertures=[0], aperture=0
        )

    with pytest.raises(AssertionError) as e:
        mask = bu.mask_fullest_bins_to_cover_aperture(
            bin_counts=[1], bin_apertures=[-1], aperture=0
        )
