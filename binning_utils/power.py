import numpy as np


def space(start, stop, power_slope, size):
    """
    Parameters
    ----------
    start : float
        Lower limit of the space.
    stop : float
        Upper limit of the space.
    power_slope : float
        Slope of the power law.
    size : int
        The number of samples.

    Returns
    -------
    x : array_like
        Values between 'start' and 'stop' spaced to histogram a power law
        with slope 'power_slope' in equal amounts in each bin.
    """
    # Adopted from CORSIKA
    rd = np.linspace(0.0, 1.0, size)
    if power_slope != -1.0:
        ll = start ** (power_slope + 1.0)
        ul = stop ** (power_slope + 1.0)
        slex = 1.0 / (power_slope + 1.0)
        return (rd * ul + (1.0 - rd) * ll) ** slex
    else:
        ll = stop / start
        return start * ll**rd


def spacing(start, stop, x, power_slope):
    """
    Parameters
    ----------
    start : float
        Start of the bin
    stop : float
        Stop of the bin
    x : float
        Value
    power_slope : float
        Slope of the power law.

    Returns
    -------
    pos : float
        The position where x has to be put in the linear interval from start to
        stop.
    """
    if power_slope != -1.0:
        inv_slex = power_slope + 1.0
        p_x = x**inv_slex
        p_start = start**inv_slex
        p_stop = stop**inv_slex
        return (p_x - p_start) / (p_stop - p_start)
    else:
        return np.log(x / start) / np.log(stop / start)
