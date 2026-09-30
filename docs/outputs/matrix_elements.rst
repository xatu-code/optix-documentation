=============================================
Optical matrix element files (.omesp, .omeex)
=============================================

These files are intermediate results. OptiX writes them so that later runs can skip the expensive
matrix-element step (see :doc:`../workflows`). You rarely need to read them yourself, but their formats
are documented here for post-processing and debugging.

All quantities in these files are in **atomic units** (energies in Hartree, k in :math:`\text{bohr}^{-1}`, velocities in
atomic units of velocity, positions in bohr). Only the *band window* is stored, i.e. the bands in
``Bandlist`` (or in the Xatu band list), numbered :math:`1\dots N_b` in the order the list gives
them. Valence bands come first.

ome_linear_sp_<material>.omesp
==============================

Written by ``OME_sp = linear``. Plain text. It holds band energies and velocity matrix elements
:math:`v^a_{ij}(\mathbf{k}) = \langle i\mathbf{k}|\hat v^a|j\mathbf{k}\rangle`.

.. code-block:: text

   1                                              # order flag (1 = linear)
   kx ky kz  E_1 E_2 ... E_Nb                     # k-point 1: energies
   kx ky kz  Re vx_11 Im vx_11 Re vy_11 Im vy_11 Re vz_11 Im vz_11
   kx ky kz  Re vx_12 Im vx_12 ...                # (i, j) with j fastest, Nb*Nb lines
   ...
   kx ky kz  E_1 ... E_Nb                         # k-point 2
   ...

The file contains no header with its dimensions. It can only be read back with the same k-mesh and
band window that produced it.

ome_nonlinear_sp_<material>.omesp
=================================

Written by ``OME_sp = nonlinear``. **Unformatted binary stream** (native endianness, 8-byte reals).
Besides energies and velocities, it contains the Berry connections, the shift vectors
:math:`R^{a,b}_{ij}`, the sum-rule generalised derivatives :math:`(r^b_{ij})_{;k^a}` and the
k-derivatives of :math:`|v^b_{ij}|`. In order:

.. code-block:: text

   int32   order flag (2)
   int32   Nk, Nb
   real64  kx(Nk), ky(Nk), kz(Nk)
   for each k-point:
       real64     E(Nb)
       complex128 v(3, Nb, Nb)
       complex128 Berry connection A(3, Nb, Nb)
       real64     shift vector R(3, 3, Nb, Nb)
       complex128 generalised derivative (3, 3, Nb, Nb)
   real64  d|v|/dk (Nk, 3, 3, Nb, Nb)          # appended after all k-points

Arrays are in Fortran (column-major) order. OptiX checks ``Nk`` and ``Nb`` when reading, and stops if
they do not match the current input.

ome_linear_ex_<material>.omeex
==============================

Written by ``OME_ex = linear``. Plain text. It holds the ground-state-to-exciton velocity matrix elements
:math:`P^a_N = \langle N|\hat v^a|0\rangle` for each exciton :math:`N = 1\dots` ``Exciton_cutoff``:

.. code-block:: text

   1
   1  Re Px Im Px  Re Py Im Py  Re Pz Im Pz
   2  ...

These are the *bare* velocity matrix elements built from the Xatu envelopes. :math:`|P^a_N|^2/E_N` sets
the oscillator strength of exciton :math:`N` in the excitonic linear conductivity. This is a quick way
to tell bright excitons from dark ones.

ome_linear_ex_k_<material>.omeexk
=================================

Written when ``Write_ex_kresolved = true`` (with ``OME_ex = linear``). Plain text. For every k-point it
holds the contribution of that k-point to each :math:`P^a_N`:

.. code-block:: text

   1
   N_ex
   kx ky kz                                        # k-point 1
   1  Re Px Im Px  Re Py Im Py  Re Pz Im Pz        # exciton 1
   ...                                             # N_ex lines
   kx ky kz                                        # k-point 2
   ...

Summing over k-points gives the values in ``.omeex``. Plotting :math:`|P^a_N(\mathbf{k})|` over the
Brillouin zone shows where exciton :math:`N` gets its brightness.

ome_second_ex_<material>.omeex2
===============================

The second-order exciton cache written by ``Cache_ome_ex``. Unformatted binary stream with a
fingerprinting header (format tag ``OPTICX-OMEEX2``, material name, k-point and band counts, exciton
energies), followed by the ground-state and inter-exciton position and velocity matrix elements. The
file is meant to be read by OptiX only; see :ref:`kw-cache`.
