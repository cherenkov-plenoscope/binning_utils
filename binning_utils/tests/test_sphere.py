import binning_utils as bu
import numpy as np


def test_fibonacci_space_basics():
    points = bu.sphere.fibonacci_space(size=1337)

    assert len(points) == 1337
    np.min(points[:, 2]) == -1.0
    np.max(points[:, 2]) == +1.0

    for point in points:
        assert np.abs(np.linalg.norm(point) - 1) < 1e-9


def test_fibonacci_space_distances_brute_force():
    size = 301
    points = bu.sphere.fibonacci_space(size=size)

    dd = np.zeros(shape=(size, size))

    for ia, a in enumerate(points):
        for ib, b in enumerate(points):
            dd[ia, ib] = np.linalg.norm(a - b)

    med_dd = [np.median(dd[i]) for i in range(size)]

    med_med_dd = np.median(med_dd)
    std_med_dd = np.std(med_dd)

    assert np.abs(med_med_dd - np.sqrt(2.0)) < 1e-2
    assert std_med_dd < 1e-2 * med_med_dd
