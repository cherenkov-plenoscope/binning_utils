Binning Utils
=============
|BlackStyle| |CiStatus|

A collection of tools to help with binning.

power10
-------
Create binning with power-space which is aligned to decades.

.. code:: python
   
   import binning_utils
   binning_utils.power10.space(start_decade=0, start_bin=0, stop_decade=2, stop_bin=1, num_bins_per_decade=3)                                             
   array([ 1., 2.15, 4.64, 10., 21.54, 46.41, 100.])


.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |CiStatus| image:: https://github.com/cherenkov-plenoscope/binning_utils/actions/workflows/ci.yml/badge.svg?branch=main&event=push
   :target: https://github.com/cherenkov-plenoscope/binning_utils/actions/workflows/ci.yml
