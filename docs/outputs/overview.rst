================
Output overview
================

Every file is written to the directory OptiX is run from. ``<material>`` is the Wannier90 file name
without its directory and without ``_tb.dat`` (e.g. ``GeS_wannier_04062024``). Existing files with
the same name are **overwritten** without warning.

Which files a run produces
==========================

.. list-table::
   :header-rows: 1
   :widths: 44 30 26

   * - File
     - Written when
     - Page
   * - ``bands_<material>.dat``
     - every run
     - :doc:`bands`
   * - ``ome_linear_sp_<material>.omesp``
     - ``OME_sp = linear``
     - :doc:`matrix_elements`
   * - ``ome_nonlinear_sp_<material>.omesp``
     - ``OME_sp = nonlinear``
     - :doc:`matrix_elements`
   * - ``ome_linear_ex_<material>.omeex``
     - ``OME_ex = linear``
     - :doc:`matrix_elements`
   * - ``ome_linear_ex_k_<material>.omeexk``
     - ``OME_ex = linear`` and ``Write_ex_kresolved = true``
     - :doc:`matrix_elements`
   * - ``ome_second_ex_<material>.omeex2``
     - ``OME_ex = nonlinear`` and ``Cache_ome_ex`` = ``write``/``readwrite``
     - :doc:`matrix_elements`
   * - ``sigma_first_sp_real_<material>.dat``, ``sigma_first_sp_imag_<material>.dat``
     - ``Response = absorbance``
     - :doc:`linear_conductivity`
   * - ``sigma_first_ex_real_<material>.dat``, ``sigma_first_ex_imag_<material>.dat``
     - ``Response = absorbance`` with Xatu
     - :doc:`linear_conductivity`
   * - ``shift_sp_lengthgauge_<material>.dat``
     - ``Response = shift_*``
     - :doc:`shift_conductivity`
   * - ``shift_vector.dat``
     - ``Response = shift_*``
     - :doc:`shift_conductivity`
   * - ``shift_ex_lengthgauge_<material>.dat``
     - ``Response = shift_*`` with Xatu
     - :doc:`shift_conductivity`
   * - ``shg_sp_lengthgauge_<material>.dat``, ``shg_ex_lengthgauge_<material>.dat``
     - ``Response = shg``
     - :doc:`second_order`
   * - ``second_<tag>_lengthgauge_<material>.dat``, ``second_ex_<tag>_lengthgauge_<material>.dat``
     - ``Response`` = ``electrooptic``, ``rectification`` or ``general`` (``<tag>`` is that name)
     - :doc:`second_order`

.. note::

   ``shift_vector.dat`` does **not** carry the material name. Runs of different materials in the same
   directory overwrite each other's copy.

General format of the spectra
=============================

All spectral files are plain text, whitespace separated, one row per frequency, with tensor components
in Cartesian order and the **last index fastest**. They fall into two groups:

* ``sigma_*`` and ``shift_*`` have **no header line** and hold **real** values. Column 1 is the photon
  energy :math:`\hbar\omega` in **eV**, on the grid defined by ``Energy_variables``
  (see :ref:`kw-energy`).
* ``shg_*`` and ``second_*`` (the second-order files, :doc:`second_order`) begin with a **header line
  starting with** ``#`` and hold **complex** values, real and imaginary part interleaved. The
  ``second_*`` files carry **two** frequency columns, :math:`\hbar\omega_p` and
  :math:`\hbar\omega_q`. ``numpy.loadtxt`` skips the header automatically.

They load directly with NumPy:

.. code-block:: python

   import numpy as np
   data = np.loadtxt("sigma_first_sp_real_GeS_wannier_04062024.dat")
   omega, sigma = data[:, 0], data[:, 1:].reshape(-1, 3, 3)   # sigma[iw, a, b]

or with gnuplot:

.. code-block:: text

   plot "sigma_first_sp_real_GeS_wannier_04062024.dat" u 1:2 w l t "Re sxx"

Terminal output
===============

The terminal log lists each stage as it starts (``1. Entering parser_input_file`` ... ``Opticx calculation
ended``). During the matrix-element step it prints one line per k-point, which can make the log long. To
keep it, redirect it to a file:

.. code-block:: bash

   opticx input.txt > opticx.log 2>&1
