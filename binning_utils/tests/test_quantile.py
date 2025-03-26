import binning_utils as binu
import numpy as np
import pytest


def test_quantile_simple():
    x = binu.quantile(bin_edges=[-1, 1], bin_counts=[1], q=0.5)
    np.testing.assert_almost_equal(desired=0.0, actual=x)

    x = binu.quantile(bin_edges=[2, 3], bin_counts=[1], q=0.5)
    np.testing.assert_almost_equal(desired=2.5, actual=x)

    x = binu.quantile(bin_edges=[-5, -4], bin_counts=[1], q=0.5)
    np.testing.assert_almost_equal(desired=-4.5, actual=x)

    x = binu.quantile(bin_edges=[-5, -4], bin_counts=[1], q=0.0)
    np.testing.assert_almost_equal(desired=-5, actual=x)

    x = binu.quantile(bin_edges=[-5, -4], bin_counts=[1], q=1.0)
    np.testing.assert_almost_equal(desired=-4, actual=x)


def test_quantile_bad_shapes():
    with pytest.raises(AssertionError) as e:
        _ = binu.quantile(bin_edges=[0], bin_counts=[0], q=0)
    with pytest.raises(AssertionError) as e:
        _ = binu.quantile(bin_edges=[0, 1, 2], bin_counts=[0], q=0)
    with pytest.raises(AssertionError) as e:
        _ = binu.quantile(bin_edges=[0], bin_counts=[], q=0)


def test_quantile_bad_q():
    with pytest.raises(AssertionError) as e:
        _ = binu.quantile(bin_edges=[0, 1], bin_counts=[1], q=-1)
    with pytest.raises(AssertionError) as e:
        _ = binu.quantile(bin_edges=[0, 1], bin_counts=[1], q=1.1)


def test_quantile_bad_counts():
    with pytest.raises(AssertionError) as e:
        _ = binu.quantile(bin_edges=[0, 1], bin_counts=[-1], q=0.5)


def gauss(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * ((x - mu) / sigma) ** 2.0
    )


def test_quantile_bell():
    mu = 3.0
    sigma = 0.2

    x_bin = binu.Binning(bin_edges=np.linspace(2, 4, 1001))
    f = gauss(x=x_bin["centers"], mu=mu, sigma=sigma)

    x = binu.quantile(bin_edges=x_bin["edges"], bin_counts=f, q=0.5)
    np.testing.assert_almost_equal(desired=mu, actual=x)

    x = binu.quantile(bin_edges=x_bin["edges"], bin_counts=f, q=0.5 - 0.68 / 2)
    np.testing.assert_almost_equal(desired=mu - sigma, actual=x, decimal=3)

    x = binu.quantile(bin_edges=x_bin["edges"], bin_counts=f, q=0.5 + 0.68 / 2)
    np.testing.assert_almost_equal(desired=mu + sigma, actual=x, decimal=3)
