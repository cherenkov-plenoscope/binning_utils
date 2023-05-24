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


def is_strictly_monotonic_increasing(x):
    assert len(x) >= 2
    for i in range(len(x) - 1):
        if x[i + 1] <= x[i]:
            return False
    return True


def merge_low_high_edges(low, high, max_relative_margin=1e-2):
    """
    Merge the low and high edges of bins into an array of bin edges.

    Parameters
    ----------
    low : array(N)
        The low edges of the bins. Must be strictly monotonic increasing.
    high : array(N)
        The high edges of the bins. Must be strictly monotonic increasing.
    max_relative_margin : float
        The relative deviation of the edges of two neigboring bins must not
        be further apart than this margin.

    Returns
    -------
    bin_edges : array(N + 1)
        The edges of the N bins, strictly monotonic increasing.
    """
    assert len(low) == len(high)
    assert is_strictly_monotonic_increasing(
        low
    ), "Expected low-edges to be strictly monotonic increasing."
    assert is_strictly_monotonic_increasing(
        high
    ), "Expected high-edges to be strictly monotonic increasing."

    N = len(low)
    bin_edges = np.zeros(N + 1)
    for n in range(N):
        bin_edges[n] = low[n]
    bin_edges[N] = high[N - 1]

    for n in range(N):
        assert (
            _relative_deviation(a=bin_edges[n + 1], b=high[n])
            < max_relative_margin
        ), "Expected bin-edges to have no gaps and no overlaps."

    return bin_edges


def max_lowest_edge(multiple_edges):
    """
    Returns the max. lower bin-edge from a list of multiple bin-edges.

    Parameters
    ----------
    multiple_edges : list of N arrays
    """
    lowest_edges = []
    for x in multiple_edges:
        assert is_strictly_monotonic_increasing(x)
        lowest_edges.append(x[0])
    return np.max(lowest_edges)


def min_highest_edge(multiple_edges):
    """
    Returns the min. highest bin-edge from a list of multiple bin-edges.

    Parameters
    ----------
    multiple_edges : list of N arrays
    """
    highest_edges = []
    for x in multiple_edges:
        assert is_strictly_monotonic_increasing(x)
        highest_edges.append(x[-1])
    return np.min(highest_edges)


def Binning(bin_edges, weight_lower_edge=0.5):
    """
    A handy dict with the most common properties of a binning.

    Parameters
    ----------
    bin_edges : array of (N + 1) floats
        The edges of the N bins, strictly_monotonic_increasing.
    weight_lower_edge : float
        Give weight to either prefer the lower, or the upper edge of the bin
        when computing 'centers'.

    Returns
    -------
    bins : dict
        num : int
            Number of bins (N).
        edges : array of (N + 1) floats
            Original bin-edges.
        centers : array of N floats
            Weighted centers of the bins.
        widths : array of N floats
            Width of the bins.
        start : float
            Lowest bin-edge
        stop : float
            Highest bin-edge
        limits : tuple(start, stop)
            Lowest and highest bin-edges.
    """
    assert is_strictly_monotonic_increasing(bin_edges)
    b = {}
    b["num"] = len(bin_edges) - 1
    b["edges"] = bin_edges
    b["centers"] = centers(
        bin_edges=bin_edges, weight_lower_edge=weight_lower_edge
    )
    b["widths"] = widths(bin_edges=bin_edges)
    b["start"] = bin_edges[0]
    b["stop"] = bin_edges[-1]
    b["limits"] = np.array([b["start"], b["stop"]])
    if np.all(bin_edges > 0.0):
        b["decade_start"] = 10 ** np.floor(np.log10(b["start"]))
        b["decade_stop"] = 10 ** np.ceil(np.log10(b["stop"]))
        b["decade_limits"] = [b["decade_start"], b["decade_stop"]]
    return b


def edges_from_width_and_num(bin_width, num_bins, first_bin_center):
    """
    Estimates the edges of bins based on the 'bin_width', their number and the
    center of the firs bin.
    """
    bin_edges = np.linspace(
        start=first_bin_center + bin_width * (-0.5),
        stop=first_bin_center + bin_width * (num_bins + 0.5),
        num=num_bins + 1,
    )
    return bin_edges
