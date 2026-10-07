=========================================
second — SHG and general second order
=========================================

Written when ``Response`` is ``shg``, ``electrooptic``, ``rectification`` or ``general``.

.. code-block:: text

   shg_sp_lengthgauge_<material>.dat            # Response = shg, independent particles
   shg_ex_lengthgauge_<material>.dat            # Response = shg, with excitons
   second_<tag>_lengthgauge_<material>.dat      # tag = electrooptic | rectification | general, sp
   second_ex_<tag>_lengthgauge_<material>.dat   # the same, with excitons

Unlike the ``shift_*`` files, these carry a **header line beginning with** ``#`` naming the columns and
the units, and they hold **complex** values (real and imaginary part interleaved). ``numpy.loadtxt``
skips the header automatically.

See :doc:`../theory/second_order` for the expressions and :ref:`dc-limit` before reading anything on or
near :math:`\omega_2 = -\omega_1`. All these files use the normalisation and sign set out in
:ref:`second-order-normalisation`; files written before 2026-10-06 differ by a constant factor (see
:doc:`../changes`).

SHG files
=========

One row per frequency, **55 columns**: :math:`\hbar\omega`, then :math:`(\mathrm{Re},\mathrm{Im})` for
each of the 27 components, :math:`a` slowest and :math:`c` fastest.

.. important::

   Column 1 is :math:`\hbar\omega`, the **fundamental** (driving) photon energy — *not*
   :math:`2\hbar\omega`. A two-photon resonance of an excitation at energy :math:`E` therefore appears
   at :math:`\hbar\omega = E/2`, and a one-photon resonance at :math:`\hbar\omega = E`. This matches
   every other spectrum OptiX writes. The file states the convention in its own header line.

.. code-block:: python

   import numpy as np
   d = np.loadtxt("shg_ex_lengthgauge_hBN.dat")           # the "#" header is skipped
   omega = d[:, 0]
   z = d[:, 1:55].reshape(-1, 27, 2)
   sigma = (z[..., 0] + 1j*z[..., 1]).reshape(-1, 3, 3, 3)   # sigma[iw, a, b, c]

General / electro-optic / rectification files
=============================================

**56 columns**: :math:`\hbar\omega_p`, :math:`\hbar\omega_q`, then
:math:`(\mathrm{Re},\mathrm{Im})\times 27`. Both frequencies are written explicitly, so the file is
self-describing whether it came from a ratio scan or a 2D map.

For the rectification files (and a 1D ``general`` scan at ``Frequency_ratio = -1``) Re is :math:`b\leftrightarrow c`
symmetric and Im antisymmetric (the reality of the current). Re is the DC response to linearly polarised
light, Im the response to circular light, which holds the injection current (:ref:`dc-excitonic-injection`).
Both files use causal broadening; the shift current in the convention of the reference paper is the
separate ``shift_*`` file of ``Response = shift``. Until 2026-10-07 the excitonic rectification file held
the shift current with zero Im columns.

.. code-block:: python

   inj = 0.5*(sigma.imag - sigma.imag.transpose(0, 1, 3, 2))    # injection current, any rectification file

.. code-block:: python

   d = np.loadtxt("second_ex_general_lengthgauge_ReS2.dat")
   w1, w2 = d[:, 0], d[:, 1]
   z = d[:, 2:56].reshape(-1, 27, 2)
   sigma = (z[..., 0] + 1j*z[..., 1]).reshape(-1, 3, 3, 3)

Two-dimensional maps
====================

With ``Energy_variables_2``, the file has :math:`n_w\times n_{wb}` rows with :math:`\omega_1` as the **slow** index
and :math:`\omega_2` as the fast one, so it reshapes directly:

.. code-block:: python

   nw, nwb = 320, 480
   w1 = d[:, 0].reshape(nw, nwb)[:, 0]      # omega_1 axis
   w2 = d[:, 1].reshape(nw, nwb)[0, :]      # omega_2 axis
   sigma = sigma.reshape(nw, nwb, 3, 3, 3)
   plt.pcolormesh(w1, w2, np.abs(sigma[:, :, 2, 2, 2]).T)    # |sigma^zzz|

To pull a single line out of a large map without loading it, ``awk`` on the two frequency columns is
enough — for the SHG diagonal :math:`\omega_2=\omega_1`:

.. code-block:: bash

   awk '$1 == $2' second_ex_general_lengthgauge_ReS2.dat > shg_line.dat

.. warning::

   The anti-diagonal ``awk '$1 == -$2'`` is the rectification, **not** the shift current.
   See :ref:`dc-antidiagonal`.

Units and symmetrisation
========================

Values are in :math:`\mu\text{A nm/V}^2`, the same 2D-sheet unit as the shift conductivity, obtained with the same
atomic-unit conversion. No spin-degeneracy factor is applied.

All of these files are written **already symmetrised** over the two field indices (the intrinsic
permutation symmetry described in :doc:`../theory/second_order`) — unlike ``shift_sp_lengthgauge_*.dat``,
which is raw. Do not symmetrise them again.
