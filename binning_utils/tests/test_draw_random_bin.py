import binning_utils as bu
import numpy as np


def test_draw_random_bin_size():
    prng = np.random.Generator(np.random.PCG64(132))

    r = bu.draw_random_bin(prng=prng, bin_apertures=[1, 2, 3])
    assert len(np.shape(r)) == 0

    r = bu.draw_random_bin(prng=prng, bin_apertures=[1, 2, 3], size=None)
    assert len(np.shape(r)) == 0

    r = bu.draw_random_bin(prng=prng, bin_apertures=[1, 2, 3], size=1)
    assert len(np.shape(r)) == 1
    assert r.shape[0] == 1

    r = bu.draw_random_bin(prng=prng, bin_apertures=[1, 2, 3], size=10)
    assert len(np.shape(r)) == 1
    assert r.shape[0] == 10


def test_draw_bin():
    prng = np.random.Generator(np.random.PCG64(132))
    bin_apertures = [2, 100, 1, 5, 1, 8]

    bins = bu.draw_random_bin(
        prng=prng, bin_apertures=bin_apertures, size=1000 * 1000
    )

    buni, bcounts = np.unique(bins, return_counts=True)

    bin_counts_normalized = bcounts / np.sum(bcounts)
    bin_apertures_normalized = bin_apertures / np.sum(bin_apertures)

    np.testing.assert_array_almost_equal(
        bin_counts_normalized,
        bin_apertures_normalized,
        decimal=3,
    )
