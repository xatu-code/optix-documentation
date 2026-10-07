=====================
Calculation workflows
=====================

``OME_sp``, ``OME_ex`` and ``Response`` are independent switches, so one calculation can be done in a
single run or split into several. This page collects the common patterns.

All intermediate files are read from, and written to, the **current working directory**. They are
named after the material (the Wannier90 file name without ``_tb.dat``). To reuse them, run later steps
in the same directory with the same Wannier90 file name.

Single-particle calculations
============================

All in one run
--------------

.. code-block:: text

   # OME_sp
   linear            (or nonlinear for shift current)
   # Response
   absorbance        (or shift)

Matrix elements first, spectra later
------------------------------------

Computing the matrix elements over the whole k-mesh is the expensive step. Evaluating the spectrum from
them is cheap. To try several frequency windows or broadenings, compute the matrix elements once:

.. code-block:: text

   # OME_sp
   nonlinear
   # Response
   none

then rerun as often as needed with:

.. code-block:: text

   # OME_sp
   none
   # Response
   shift
   # Energy_variables
   0.5 6 0.02 1000
   # Broadening_type
   gaussian

With ``OME_sp = none``, keep ``Ncells``, ``Bandlist`` and ``Nfermi`` exactly as in the run that wrote
the file. The binary nonlinear file records its k-point and band counts, and OptiX stops if they no
longer match. The **linear** text file is **not** checked, so a mismatch there gives wrong results
without any error.

Absorbance from a nonlinear run
-------------------------------

``absorbance`` always reads the *linear* file ``ome_linear_sp_<material>.omesp``. A nonlinear run only
writes the *nonlinear* one. To get both responses, run ``OME_sp = linear`` once as well, which is cheap.

Excitonic calculations
======================

When ``Xatu_interface = true``, the exciton envelopes are rotated into the single-particle band basis.
The ``.omesp`` file stores that basis (since 2026-10-06), so an excitonic run may reuse it with
``OME_sp = none``; an ``.omesp`` from an earlier version is refused (see :ref:`kw-omeex`).

Faster still is a second-order cache. Once ``Cache_ome_ex = write`` has stored the excitonic
matrix elements, later runs may use ``OME_sp = none`` **and** ``Cache_ome_ex = read`` together, which
skips both the single-particle and the excitonic matrix-element stages and reads everything from disk.
That is the cheap way to scan several ``Response`` branches, several frequency windows or several
broadenings over one set of matrix elements — the branches all share the same elements.

Excitonic absorbance
--------------------

.. code-block:: text

   # OME_sp
   linear
   # OME_ex
   linear
   # Response
   absorbance

writes both ``sigma_first_sp_*`` and ``sigma_first_ex_*``. To recompute only the spectrum (for
example with a different broadening), set ``OME_sp = none`` and ``OME_ex = none``. Both linear
matrix-element files are then read back.

Excitonic shift current
-----------------------

.. code-block:: text

   # OME_sp
   nonlinear
   # OME_ex
   nonlinear
   # Response
   shift
   # Cache_ome_ex
   readwrite

The inter-exciton matrix elements are only kept in memory, so ``OME_ex = nonlinear`` is needed every
time an excitonic shift current is computed. Building them dominates the cost, and
``Cache_ome_ex = readwrite`` turns later runs (new ``Energy_variables`` or broadening) into a quick
read of ``ome_second_ex_<material>.omeex2``.

Typical sequence:

1. Run with ``Cache_ome_ex = write`` (or ``readwrite``) once.
2. Change ``Energy_variables`` or ``Broadening_type`` and rerun with ``Cache_ome_ex = read``. The log
   shows ``Second-order excitonic OMEs read from cache ... exciton k-loop skipped``.
3. If you later **lower** ``Exciton_cutoff``, the same cache is still used (a subset of it). If you
   raise it, the elements are recomputed.

Delete the ``.omeex2`` file whenever you change the Wannier90 model; see the warning in :ref:`kw-cache`.

Large calculations
==================

For an excitonic second-order study the expensive stage is building the exciton matrix elements, and
it does not depend on ``Response``, the frequency window or the broadening. So:

#. run once with ``Cache_ome_ex = write``;
#. run every branch afterwards with ``OME_sp = none`` and ``Cache_ome_ex = read``.

That second form skips both the single-particle and the excitonic matrix-element stages, and it also
skips reading the exciton envelopes from the ``.states`` file — which for a large basis is the biggest
remaining start-up cost, since that file is plain ASCII and can run to gigabytes.

**Memory.** The peak is dominated by terms linear in ``Exciton_cutoff`` (the envelopes and their
k-derivative, :math:`\texttt{norb\_ex} \times N`) plus :math:`8N^2` complex numbers for the
accumulators. It does **not** scale with the number of OpenMP threads, so there is no memory reason to
run on fewer cores. As a reference point, the complete 5625-state basis of a 75x75 two-band model
needs 6.6 GB, and its complete 8100-state basis on a 90x90 mesh needs 12.9 GB.

**Threads.** The matrix-element stage is one large matrix multiplication per term and is threaded
through BLAS; the response stage likewise. Use the cores you have. If you link a threaded BLAS, make
sure it is the OpenMP build (or set ``OPENBLAS_NUM_THREADS`` explicitly), so that it stands down inside
OptiX's own parallel regions instead of oversubscribing.

**Frequency grids.** A two-dimensional map costs :math:`n_w\times n_{wb}` kernel evaluations, so it is the one
place where the frequency grid, rather than the exciton count, dominates: a 320x480 map is 153 600
pairs. Size it deliberately.

Convergence checklist
=====================

Before trusting a spectrum, check it against each of these:

``Ncells`` (sp) / the Xatu k-mesh (ex)
   Increase until the features you care about stop changing. Shift currents typically need denser meshes
   than linear absorption.

``Bandlist`` / the Xatu band window
   The spectrum is only complete up to the energy where transitions from bands outside the window
   start. Widen the window and compare.

``Exciton_cutoff``
   Excitonic spectra are converged only up to about the energy of the highest exciton included.

``eta``
   Results at a fixed broadening should be converged in the mesh first. Reduce ``eta`` only together
   with a denser mesh.
