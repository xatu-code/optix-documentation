===============
Troubleshooting
===============

Messages printed by OptiX, what they mean, and what to do about them.

Errors that stop the run
========================

``Error: Invalid value in Xatu_interface. Expected "true" or "false".``
   The value is not exactly ``true`` or ``false`` (it is case sensitive).

``ERROR (optical_response): unknown Response = "..."``
   The ``Response`` value is misspelled or not lowercase. Valid values: ``none``, ``absorbance``,
   ``shift_sumrule``, ``shift_shiftvector``, ``shift_gender``.

``ERROR (parser_input_file): Cache_ome_ex = "..." is not recognised.``
   Use ``read``, ``write``, ``readwrite`` (= ``true``, ``both``) or ``off`` (= ``false``, ``none``).

``ERROR: Bandlist entry j resolves to band n, outside the valid range 1..norb``
   ``Nfermi + Bandlist(j)`` falls outside the Wannier bands. Check ``Nfermi``, and that ``Bandlist`` counts
   from the Fermi level (``0`` = top valence band).

``ERROR (parser_wannier90_tb): no R=(0,0,0) cell found in the _tb.dat file.``
   The Wannier90 file is incomplete or not in ``_tb.dat`` format.

``ERROR (read_ome_sp_nonlinear): .omesp file was generated for a different grid/Bandlist``
   You used ``OME_sp = none`` after changing ``Ncells`` or ``Bandlist``. Regenerate the file with
   ``OME_sp = nonlinear``.

``ERROR (sigma_second_sp): the .omesp file has no derivative of |v|``
   The nonlinear matrix-element file was written by an older OptiX version. Regenerate it with
   ``OME_sp = nonlinear``.

``ERROR (sigma_second_ex): xme_ex_inter/vme_ex_inter not populated``
   An excitonic shift current was requested without ``OME_ex = nonlinear`` in the same run (or without a
   valid cache). See :ref:`kw-omeex`.

``ERROR (read_ome_ex_second): ... was written for a DIFFERENT system`` / ``cached exciton energies differ``
   The ``.omeex2`` cache belongs to another calculation. Delete it or move it aside.

``ERROR (get_exciton_dim): no repeated valence-band index found ...``
   The ``.states`` file does not look like a Xatu eigenstates file. Check the path, and that Xatu ran
   with ``-c``.

Fortran runtime error ``Attempting to allocate already allocated variable 'nband_index'``
   ``Bandlist`` was given together with ``Xatu_interface = true``. Remove ``Bandlist``, since the band
   list comes from the Xatu files.

Fortran runtime error when opening ``ome_linear_sp_*.omesp`` / ``ome_nonlinear_sp_*.omesp``
   ``OME_sp = none`` was used, but the file does not exist in the current directory. Either the previous
   run was done elsewhere, or it used a different Wannier90 file name (the material name is part of the
   file name), or it was of the other order (see the table in :ref:`kw-omesp`).

Crashes and slow runs
=====================

Segmentation fault early in a run, especially for large meshes
   Usually a stack overflow. Run ``ulimit -s unlimited`` and ``export OMP_STACKSIZE=512M`` (or larger)
   before starting OptiX.

The run is slow
   * Check that ``OMP_NUM_THREADS`` is set to the number of physical cores.
   * Compile without ``-fcheck=all`` for production runs (see :doc:`installation`).
   * Split the calculation and reuse matrix elements (see :doc:`workflows`). For excitonic shift
     currents, use ``Cache_ome_ex``.

Warnings
========

``WARNING (ome_sp): an Eq. (A4) multiplet straddles the Bandlist edge``
   A set of degenerate bands is only partly inside ``Bandlist``. Extend the list so that it contains
   every member of each degenerate set.

``WARNING (ome_sp): the Eq. (A4) rotation is active but the per-k rotation matrices are unavailable``
   Excitonic matrix elements were requested with ``OME_sp = none``. Compute ``OME_sp`` in the same run;
   otherwise the excitonic results are wrong.

``WARNING (exciton_envelopes): ndim = ... but ... lattice direction(s) appear active``
   ``Periodic dimensions`` does not match the number of periodic directions in the Wannier90 file.
   Check the input.

``WARNING: shift_sumrule is unreliable unless the band window is large``
   Expected when using ``shift_sumrule``. Prefer ``shift_shiftvector``.

Results look wrong
==================

The spectrum is zero or tiny
   * Is the frequency window above the band gap? Check ``bands_<material>.dat``.
   * Is ``Nfermi`` right? If it is too small or too large, the "valence" bands are not the occupied ones.
   * ``shift_gender`` is not implemented and gives zeros.

Spiky or noisy spectra
   The k-mesh is too coarse for the broadening. Increase ``Ncells`` (or the Xatu mesh), or increase
   ``eta``.

The magnitude differs from a paper by a factor ~2
   Check spin degeneracy (not included), Gaussian vs Lorentzian width, sheet vs bulk units, and the
   field-amplitude convention of the second-order response. See :doc:`theory/conventions`.

The excitonic spectrum stops abruptly at high energy
   The ``Exciton_cutoff`` excitons do not reach that energy. Ask Xatu for more states, and increase
   ``Exciton_cutoff``.
