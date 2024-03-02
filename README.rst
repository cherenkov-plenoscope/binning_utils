#############
Binning Utils
#############
|TestStatus| |PyPiStatus| |BlackStyle| |BlackPackStyle| |MITLicenseBadge|

A collection of tools to help with binning.

*******
power10
*******

Create binning in geomspace which is aligned to decades.

.. code:: python

    import binning_utils
    binning_utils.power10.space(
        start_decade=0,
        start_bin=0,
        stop_decade=2,
        stop_bin=1,
        num_bins_per_decade=3,
    )
    array([ 1., 2.15, 4.64, 10., 21.54, 46.41, 100.])


**********
powerspace
**********

To make bin edges for distributions occuring in power laws.
For example to histogram the energies of cosmic rays which occur in a
power law with slope ``-2.7``

.. code:: python

    import binning_utils
    binning_utils.powerspace(
        start=1,
        stop=10,
        power_slope=-2.7,
        size=10,
    )
    array([ 1.        ,  1.07017144,  1.15544801,  1.26196439,  1.39995703,
        1.58808152,  1.86493297,  2.32807878,  3.33799855, 10.        ])



.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |BlackPackStyle| image:: https://img.shields.io/badge/pack%20style-black-000000.svg
    :target: https://github.com/cherenkov-plenoscope/black_pack

.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/binning_utils/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/binning_utils/actions/workflows/test.yml

.. |MITLicenseBadge| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://opensource.org/licenses/MIT

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/binning_utils_sebastian-achim-mueller
    :target: https://pypi.org/project/binning_utils_sebastian-achim-mueller
