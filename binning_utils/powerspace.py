import numpy as np


def powerspace(start, stop, power_slope, size):
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
