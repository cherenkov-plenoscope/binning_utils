import numpy as np
from . import power10


def centers(bin_edges, weight_lower_edge=0.5):
    """
    Parameters
    ----------
    bin_edges : array of floats
        The edges of the bins.
    weight_lower_edge : float
        Give weight to either prefer the lower, or the upper edge of the bin.

    Returns
    -------
    width : array of floats
        The centers of the bins.
    """

    bin_edges = np.array(bin_edges)
    assert len(bin_edges) >= 2, "Need at least two edges to compute a center."
    assert weight_lower_edge >= 0.0 and weight_lower_edge <= 1.0
    weight_upper_edge = 1.0 - weight_lower_edge
    return (
        weight_lower_edge * bin_edges[:-1] + weight_upper_edge * bin_edges[1:]
    )


def widths(bin_edges):
    """
    Parameters
    ----------
    bin_edges : array of floats
        The edges of the bins.

    Returns
    -------
    width : array of floats
        The widths of the bins.
    """

    bin_edges = np.array(bin_edges)
    assert len(bin_edges) >= 2, "Need at least two edges to compute a width."
    return bin_edges[1:] - bin_edges[:-1]


def find_bin_in_edges(bin_edges, value):
    """
    A wrapper around numpy.digitize with over/under-flow indication.

    Parameters
    ----------
    bin_edges : array of floats
        The edges of the bins.
    value : float
        The value to be assigned to a bin.

    Returns
    -------
    underflow-flag, bin-index, overflow-flag
    """
    upper_bin_edge = int(np.digitize([value], bin_edges)[0])
    if upper_bin_edge == 0:
        return True, 0, False
    if upper_bin_edge == bin_edges.shape[0]:
        return False, upper_bin_edge - 1, True
    return False, upper_bin_edge - 1, False


def find_bins_in_centers(bin_centers, value):
    """
    Compute the weighted distance to the supports of the bins.
    """
    underflow, lower_bin, overflow = find_bin_in_edges(
        bin_edges=bin_centers, value=value
    )

    upper_bin = lower_bin + 1
    if underflow:
        lower_weight = 0.0
    elif overflow:
        lower_weight = 1.0
    else:
        dist_to_lower = value - bin_centers[lower_bin]
        bin_range = bin_centers[upper_bin] - bin_centers[lower_bin]
        lower_weight = 1 - dist_to_lower / bin_range

    return {
        "underflow": underflow,
        "overflow": overflow,
        "lower_bin": lower_bin,
        "upper_bin": lower_bin + 1,
        "lower_weight": lower_weight,
        "upper_weight": 1.0 - lower_weight,
    }


def _relative_deviation(a, b):
    if np.abs(a + b) == 0.0:
        return 0
    return np.abs(a - b) / np.abs(0.5 * (a + b))


def merge_low_high_edges(low_edges, high_edges, max_relative_margin=1e-2):
    """
    Merge the low and high edges of bins into an array of bin edges.

    Parameters
    ----------
    low_edges : array(N)
        The low edges of the bins. Must be strictly monotonic increasing.
    high_edges : array(N)
        The high edges of the bins. Must be strictly monotonic increasing.
    max_relative_margin : float
        The relative deviation of the edges of two neigboring bins must not
        be further apart than this margin.

    Returns
    -------
    bin_edges : array(N + 1)
        The edges of the N bins, strictly monotonic increasing.
    """
    assert len(low_edges) == len(high_edges)
    assert np.all(
        np.gradient(low_edges) > 0
    ), "Expected low_edges to be strictly monotonic increasing."
    assert np.all(
        np.gradient(high_edges) > 0
    ), "Expected high_edges to be strictly monotonic increasing."

    N = len(low_edges)
    bin_edges = np.zeros(N + 1)
    for n in range(N):
        bin_edges[n] = low_edges[n]
    bin_edges[N] = high_edges[N - 1]

    for n in range(N):
        assert (
            _relative_deviation(a=bin_edges[n + 1], b=high_edges[n])
            < max_relative_margin
        ), "Expected bin-edges to have no gaps and no overlaps."

    return bin_edges
