===============
Troubleshooting
===============

Messages printed by OptiX, what they mean, and what to do about them.

Errors that stop the run
========================

``Error: Invalid value in Xatu_interface. Expected "true" or "false".``
   The value is not exactly ``true`` or ``false`` (it is case sensitive).

``ERROR: Invalid value in Orthonormal. Expected "true" or "false".``
   The value of :ref:`kw-orthonormal` is not exactly ``true`` or ``false`` (it is case sensitive).

``ERROR: Generalized eigenvalue problem failed. zhegv failed with INFO = ...``
   Only with ``Orthonormal = false``. The overlap :math:`S(\mathbf k)` is not positive definite at some
   k-point (``INFO`` larger than the number of orbitals), or the overlap section of the model file was not
   read as intended. Check that section (:ref:`kw-orthonormal`).

``WARNING (Bandlist): unusual band window``
   The band list omits the top valence band (offset 0) or the bottom conduction band (offset 1), leaves a gap,
   or repeats an entry. ``Bandlist`` is a list of offsets, not a range: write every band out, e.g. ``-1 0 1 2``
   (:ref:`kw-bandlist`). If the window is intentional the warning can be ignored, but expect degenerate pairs
   to be cut.

``ERROR (parser_input_file): Ex_rectification = shift has been removed.``
   The excitonic rectification is now the whole causal response; for the shift current use
   ``Response = shift`` and drop the keyword (:ref:`kw-ex-rect`). ``Ex_rectification = causal`` only prints a
   note and is ignored.

``ERROR (parser_input_file): Sp_method = "..." is not recognised.``
   Use ``covariant`` or ``per_band`` (:ref:`kw-sp-method`).

``ERROR (optical_response): unknown Response = "..."``
   The ``Response`` value is misspelled or not lowercase. Valid values: ``none``, ``absorbance``,
   ``shift``, ``shift_covariant``, ``shift_shiftvector``, ``shift_sumrule``, ``shift_gender``, ``shg``,
   ``shg_covariant``, ``electrooptic``, ``rectification``, ``general``.

``ERROR (ome_ex): the exciton envelopes are not in the same basis as the single-particle matrix elements``
   You asked for an excitonic response with ``OME_sp = none``, no usable second-order cache, and an
   ``.omesp`` written before 2026-10-06, which does not store the Eq. (A4) rotation the exciton envelopes
   must be carried into. Regenerate the ``.omesp`` once with ``OME_sp = nonlinear`` (``linear`` for
   ``OME_ex = linear``); later runs can then use ``OME_sp = none``. A matching cache with
   ``Cache_ome_ex = read`` also works. See :ref:`kw-omeex`.

``ERROR (get_sigma_general_sp): hbar(w_p+w_q) is exactly zero at a grid point``
   With ``Sp_method = per_band``, a single-particle second-order run landed on :math:`\omega_1 + \omega_2 = 0` with zero broadening.
   Term 1 of Eq. (A3a) includes :math:`n = m`, where the outer denominator is
   :math:`\hbar\omega_\Sigma` itself, so this is a genuine 0/0. Use a nonzero ``eta``.

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

``ERROR (sigma_second_sp): the .omesp file has no covariant second-order data``
   ``OME_sp = none`` read an ``.omesp`` that lacks what ``Sp_method = covariant`` needs for SHG,
   electro-optic, rectification or ``general``: it was written by an older version, for another
   ``Response``, or with ``Sp_method = per_band``. Run once with ``OME_sp = nonlinear``.

``ERROR (sigma_second_sp): the .omesp file has no block-covariant derivative``
   The same for ``Response = shift`` / ``shift_covariant``: the ``.omesp`` must come from a run that
   computed the covariant shift current.

``ERROR (sigma_second_sp): the .omesp file has no derivative of |v|``
   The nonlinear matrix-element file was written by an older OptiX version. Regenerate it with
   ``OME_sp = nonlinear``.

``ERROR (get_exciton_data): Exciton_cutoff = N but only M exciton energies are present``
   ``Exciton_cutoff`` is larger than the number of states Xatu wrote. The message gives ``M``; lower
   the keyword to at most that, or rerun Xatu with a larger ``-n``. A companion message from
   ``load_fk_ex`` covers the case where the ``.states`` file holds fewer wavefunctions than
   ``.eigval`` lists energies.

``ERROR (sigma_second_ex): xme_ex_inter/vme_ex_inter not populated``
   An excitonic shift current was requested without ``OME_ex = nonlinear`` in the same run (or without a
   valid cache). See :ref:`kw-omeex`.

``ERROR (read_ome_ex_second): ... was written for a DIFFERENT system`` / ``cached exciton energies differ``
   The ``.omeex2`` cache belongs to another calculation. Delete it or move it aside.

``ERROR (read_ome_ex_second): ... was written for a DIFFERENT band set``
   The cache was built from different bands, **or from the same bands in a different order**, which is
   just as wrong: the exciton envelopes would be paired with the wrong band. The message prints both
   band lists. Delete the cache or move it aside. This check exists because band *counts* alone cannot
   tell ``[60, 61]`` from ``[61, 60]``, and that ambiguity once invalidated a whole set of published
   numbers. See the note on format version 2 in :ref:`kw-cache`.

``ERROR (read_ome_ex_second): ... has a DIFFERENT number of bands``
   Same cause, detected one step earlier. Delete the cache.

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

Messages that are not errors
============================

``Cache ... is format version 1, which does NOT record the band list``
   The ``.omeex2`` file predates 2026-09-30. It is ignored and the matrix elements are recomputed —
   the run continues and the result is correct. Version 1 recorded only the band *counts*, so it
   cannot be checked for the band-order hazard above, and the order it was written with cannot be
   recovered from the file. Delete it; regenerating is far cheaper than it used to be.

``Cache ... is truncated or unreadable, recomputing.``
   A partial file, usually from an interrupted run. Harmless; delete it.

Warnings
========

``WARNING (parser_wannier90_tb): ... not Hermitian: max defect ...``
   The model file breaks the Hermiticity of :math:`H(\mathbf R)`, :math:`S(\mathbf R)` or the position matrices
   (:ref:`kw-wannier`). OptiX replaces the block by its Hermitian part and continues, and the message gives the
   size and location of the largest defect. Small defects come from the precision the file was written with;
   larger ones (MoS\ :sub:`2`: :math:`6\times10^{-3}` Angstrom; In\ :sub:`2`\ Se\ :sub:`3`: 0.12 Angstrom) are a property of the Wannierisation. Regenerate or repair the
   file to silence the warning; the results will then not change.

``WARNING (ome_sp): an Eq. (A4) multiplet straddles the Bandlist edge``
   A set of degenerate bands is only partly inside ``Bandlist``. Extend the list so that it contains
   every member of each degenerate set.

``WARNING (ome_sp): the Eq. (A4) rotation is active but the per-k rotation matrices are unavailable``
   Excitonic matrix elements were requested with ``OME_sp = none`` and an ``.omesp`` from before
   2026-10-06. The run then stops with the error above; regenerate the ``.omesp`` once.

``WARNING (ome_sp): Nfermi = N does not put the Fermi level in a gap on this mesh``
   Band ``Nfermi`` reaches higher than band ``Nfermi + 1`` somewhere (or they touch); the message gives
   both energies. OptiX occupies bands by index, so this filling describes a metal, and second-order
   responses then contain poles at vanishing transition energy. Check ``Nfermi`` (:ref:`kw-nfermi`). If
   the filling is intentional, the warning can be ignored.

``WARNING (exciton_envelopes): ndim = ... but ... lattice direction(s) appear active``
   ``Periodic dimensions`` does not match the number of periodic directions in the Wannier90 file.
   Check the input.

``WARNING: shift_sumrule is unreliable unless the band window is large``
   Expected when using ``shift_sumrule``. Prefer ``shift``.

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
