==========
Input file
==========

An OptiX calculation is controlled by one plain-text input file, passed as the only command-line
argument:

.. code-block:: bash

   opticx input.txt

Besides the input file itself, a run needs:

* a **Wannier90 tight-binding file** (``<seedname>_tb.dat``) — always;
* the Xatu **exciton files** (``.eigval`` and ``.states``) — only for excitonic calculations.

Format rules
============

The input file is a sequence of **label / value** blocks. A label is a line beginning with ``#``
followed by **one space** and the keyword. The value goes on the next line(s):

.. code-block:: text

   # Keyword
   value

Some details of the parser are easy to trip over:

* **The space after** ``#`` **matters.** The keyword is read from the third character on, so
  ``#Response`` (no space) is read as ``esponse`` and silently ignored.
* **Order does not matter.** Blocks can appear in any order.
* **Keywords are matched as substrings.** Any line starting with ``#`` that *contains* a keyword triggers
  that keyword. Do not write free-text comments that mention a keyword (e.g. ``# Response below is for
  testing``). Lines starting with ``#`` that contain no keyword are ignored, so ordinary comments are fine.
* **Values are case sensitive** (``true``, ``linear``, ``absorbance`` must be lowercase). The only
  exceptions are ``Broadening_type``, ``Cache_ome_ex``, ``Xnm_derivative`` and ``Exciton_basis_repair``.
* **Unknown keywords are ignored**, and there is no warning for a misspelled optional keyword.
* **File paths** are read as a whole line and may contain spaces. Each path can be up to 1000 characters
  long; the input file name itself can be up to 100 characters.

Complete example
================

A single-particle shift-current calculation using every commonly needed keyword:

.. code-block:: text

   # Periodic dimensions
   2
   # Wannier90_filename
   /home/user/models/GeS_wannier_04062024_tb.dat
   # Xatu_interface
   false
   # Bandlist
   -1 0 1 2
   # Ncells
   102
   # Nfermi
   20
   # OME_sp
   nonlinear
   # Response
   shift
   # Energy_variables
   1 9 0.025 400
   # Broadening_type
   lorentzian

Keyword summary
===============

.. list-table::
   :header-rows: 1
   :widths: 22 14 64

   * - Keyword
     - Required
     - Meaning
   * - :ref:`kw-periodic`
     - always
     - Number of periodic dimensions (1, 2 or 3).
   * - :ref:`kw-wannier`
     - always
     - Path to the Wannier90 ``_tb.dat`` file.
   * - :ref:`kw-orthonormal`
     - optional
     - ``true`` (default) or ``false``: the model file carries an overlap matrix :math:`S(\mathbf R)`.
   * - :ref:`kw-xatu`
     - always
     - ``true``/``false``; if ``true``, followed by the ``.eigval`` and ``.states`` paths.
   * - :ref:`kw-bandlist`
     - sp only
     - Bands included, relative to the Fermi level.
   * - :ref:`kw-ncells`
     - sp only
     - k-points per reciprocal direction.
   * - :ref:`kw-nfermi`
     - always
     - Number of filled bands.
   * - :ref:`kw-cutoff`
     - excitonic only
     - Number of exciton states used.
   * - :ref:`kw-omesp`
     - always
     - Single-particle matrix elements: ``linear``, ``nonlinear`` or ``none``.
   * - :ref:`kw-omeex`
     - excitonic only
     - Excitonic matrix elements: ``linear``, ``nonlinear`` or ``none``.
   * - :ref:`kw-response`
     - always
     - ``absorbance``, ``shift``, ``shift_shiftvector``, ``shift_covariant``, ``shift_sumrule``, ``shift_gender``, ``shg``,
       ``shg_covariant``, ``electrooptic``, ``rectification``, ``general`` or ``none``.
   * - :ref:`kw-sp-method`
     - optional
     - Single-particle second-order method: ``covariant`` (default) or ``per_band``.
   * - :ref:`kw-energy`
     - always
     - Frequency window, broadening and number of points.
   * - :ref:`kw-ratio`
     - optional
     - :math:`\omega_2/\omega_1` for ``Response = general``.
   * - :ref:`kw-energy2`
     - optional
     - A second, independent :math:`\omega_2` grid; turns ``general`` into a 2D map.
   * - :ref:`kw-broadening`
     - optional
     - ``lorentzian`` (default) or ``gaussian``.
   * - :ref:`kw-exk`
     - optional
     - Write k-resolved excitonic matrix elements.
   * - :ref:`kw-cache`
     - optional
     - Cache the second-order excitonic matrix elements on disk.

"sp only" means the keyword is used when ``Xatu_interface`` is ``false``. With Xatu, the same
information is read from the exciton files instead.

Keyword reference
=================

.. _kw-periodic:

Periodic dimensions
-------------------

.. code-block:: text

   # Periodic dimensions
   2

Integer: ``1``, ``2`` or ``3``. This fixes the dimensionality of the k-mesh and how the reciprocal
lattice and cell "volume" are built. OptiX works out which lattice directions are periodic from the
lattice vectors present in the Wannier90 file. For a 2D model, the in-plane directions are those with
non-zero hoppings.

.. important::

   2D is the main, tested use case. The output unit conversions assume a 2D sheet (see
   :doc:`theory/conventions`), and the band-structure path is only defined in 2D. 1D and 3D inputs are
   accepted, but check the results carefully.

.. _kw-wannier:

Wannier90_filename
------------------

.. code-block:: text

   # Wannier90_filename
   /home/user/models/GeS_wannier_04062024_tb.dat

The full path (absolute, or relative to the directory you run in) of a Wannier90 tight-binding file in
the standard ``<seedname>_tb.dat`` format, as written by Wannier90 with ``write_tb = .true.``.
That file holds the lattice vectors, the Hamiltonian :math:`H(\mathbf{R})` and the position matrix
elements :math:`\mathbf{r}(\mathbf{R})`. The file is read in Angstrom and eV.

The **material name** used to label every output file is the file name without its directory and without
the ``_tb.dat`` suffix. For example, ``/data/GeS_wannier_04062024_tb.dat`` becomes
``GeS_wannier_04062024``.

.. note::

   The basis is assumed orthonormal unless :ref:`kw-orthonormal` is ``false``. The Hamiltonian must include the home cell
   :math:`\mathbf{R}=(0,0,0)`; otherwise OptiX stops with an error.

**Hermiticity.** A physical model has :math:`H_{ij}(\mathbf R)=H_{ji}(-\mathbf R)^*`, the same for the overlap
:math:`S`, and :math:`r_{ij}(\mathbf R)=r_{ji}(-\mathbf R)^*+\mathbf R\,S_{ij}(\mathbf R)` for the position
matrices (the last term vanishes for orthonormal Wannier functions). The reader checks all three and logs the
result:

* a block stored as its lower triangle only (upper triangle identically zero, e.g. the :math:`H` and :math:`S` of
  some non-orthonormal models) is completed by Hermiticity;
* a block that breaks the relation by more than :math:`10^{-8}` of its largest element produces a ``WARNING`` with
  the size and location of the defect, and is replaced by its Hermitian part,
  :math:`[X(\mathbf R)+X(-\mathbf R)^\dagger]/2`;
* a block that is already Hermitian is used unchanged.

The repair matters: OptiX builds the Bloch matrices from the lower triangle, so an unrepaired defect would act
as a symmetry-breaking perturbation that depends on the order of the orbitals in the file.

.. _kw-orthonormal:

Orthonormal
-----------

.. code-block:: text

   # Orthonormal
   false

Optional (default ``true``); the value must be exactly ``true`` or ``false``. With ``false`` the basis
functions of the model file are **not** assumed orthonormal: the file carries an overlap matrix
:math:`S_{ij}(\mathbf R)=\langle 0i|\mathbf Rj\rangle` (for example a tight-binding model built from atomic
orbitals), and OptiX

* solves the generalised eigenproblem :math:`H(\mathbf k)\,c = E\,S(\mathbf k)\,c` (LAPACK ``zhegv``), for the
  responses and for the band file;
* includes the overlap in the velocity and Berry-connection matrix elements, and weights with
  :math:`S(\mathbf k)` every overlap between states at neighbouring k-points (parallel transport, the block
  transport of the covariant methods, the Eq. (A4) basis).

**File format.** The usual ``_tb.dat`` layout, followed by an overlap section: after the last position
block, one block per cell in the same order as the Hamiltonian, each a header line with the cell and then
:math:`N_\text{orb}^2` lines ``i j Re(S) Im(S)``, with a blank line between blocks (none is needed after the
last). :math:`S` is dimensionless and is not divided by the Wigner–Seitz degeneracy weights (the
Hamiltonian is, the position matrices are not). Blocks may be stored as their lower triangle only (see the
Hermiticity rules above). The position matrices are :math:`\langle 0i|\hat{\mathbf r}|\mathbf Rj\rangle`,
which in a non-orthonormal basis satisfy :math:`r_{ij}(\mathbf R)=r_{ji}(-\mathbf R)^*+\mathbf R\,S_{ij}(\mathbf R)`.

:math:`S(\mathbf k)` must be positive definite at every k-point; otherwise the eigensolver fails and OptiX
stops (see :doc:`troubleshooting`).

Validated by rewriting hBN in a non-orthogonal basis that describes the same physics and requiring the
results of the orthonormal model: with an on-site overlap the shift current, SHG, absorbance and bands
agree to :math:`10^{-10}` or better; with a k-dependent (non-local) overlap the shift current, SHG and
rectification agree to :math:`2\times10^{-9}` or better. The excitonic path has not been tested with a
non-orthonormal model.

.. _kw-xatu:

Xatu_interface
--------------

Without excitons:

.. code-block:: text

   # Xatu_interface
   false

With excitons: ``true``, followed on the next two lines by the paths of the Xatu **energies** file and
the Xatu **eigenstates** file, in that order:

.. code-block:: text

   # Xatu_interface
   true
   /home/user/xatu_run/hBN.eigval
   /home/user/xatu_run/hBN.states

Any value other than ``true`` or ``false`` stops the program.

With ``true``, OptiX takes the **k-mesh** and the **band window** from the ``.states`` file. That makes
the single-particle and excitonic calculations use exactly the grid and bands Xatu used. In that case:

* do **not** give ``Bandlist``; it would clash with the band list read from Xatu;
* ``Ncells`` is ignored;
* Xatu must have been run on the **same Wannier90 file**, with ``--w90 <filling>`` where
  ``<filling>`` equals ``Nfermi``, and with the ``-e`` and ``-c`` output flags;
* Xatu must have written at least ``Exciton_cutoff`` states (its ``-n`` option).

With ``true``, every response is computed twice: once for independent particles (``sp`` files) and once
with excitons (``ex`` files).

.. _kw-bandlist:

Bandlist
--------

.. code-block:: text

   # Bandlist
   -1 0 1 2

A space-separated list of integers selecting the bands that enter the optical transitions, counted
**relative to the Fermi level**, as in Xatu:

* ``0`` is the highest valence band, ``-1`` the one below it, and so on;
* ``1`` is the lowest conduction band, ``2`` the next, and so on.

Entries :math:`\le 0` are valence (occupied) bands; entries :math:`> 0` are conduction (empty) bands.
Internally, entry :math:`j` refers to band number ``Nfermi + j`` of the Wannier Hamiltonian, counted
from 1 at the bottom. Every entry must fall within 1 ... (number of Wannier orbitals), or OptiX stops and
names the offending entry.

Only transitions between the listed bands are included, so the spectrum is only meaningful up to the
energy where bands outside the window start to contribute. Widen the list to push that limit up.

.. tip::

   Keep degenerate bands together. If a set of degenerate bands straddles the edge of ``Bandlist``,
   OptiX prints a warning: ``an Eq. (A4) multiplet straddles the Bandlist edge``. Add the missing
   partners to the list.

Used only when ``Xatu_interface`` is ``false``.

.. _kw-ncells:

Ncells
------

.. code-block:: text

   # Ncells
   102

Number of k-points **per periodic direction**. The Brillouin zone is sampled with a :math:`\Gamma`-centred
Monkhorst–Pack mesh of :math:`N` (1D), :math:`N^2` (2D) or :math:`N^3` (3D) points, with :math:`N` = ``Ncells``. This is the same
mesh Xatu builds, so a single-particle OptiX run with ``Ncells = N`` matches a Xatu run with an
:math:`N\times N` mesh point by point.

Along each reciprocal-lattice vector, the fractional coordinates are
:math:`u_c = c/N - 1/2` for :math:`c = 0,\dots,N-1`. For odd :math:`N` they are shifted by
:math:`1/(2N)`, giving a mesh symmetric about :math:`\Gamma`.

Convergence with ``Ncells`` is the main accuracy control. It must be checked, especially for the shift
current. Used only when ``Xatu_interface`` is ``false``.

.. _kw-nfermi:

Nfermi
------

.. code-block:: text

   # Nfermi
   20

The number of **filled bands** in the Wannier Hamiltonian. The system is treated as an insulator at
zero temperature: bands in ``Bandlist`` with index :math:`\le 0` have occupation 1 and the rest have
occupation 0.

With Xatu, this **must match** the filling passed to ``xatu --w90``.

.. _kw-cutoff:

Exciton_cutoff
--------------

.. code-block:: text

   # Exciton_cutoff
   100

Number of exciton states, lowest in energy first, read from the Xatu files and included in the
excitonic response. The spectrum is converged only up to roughly the energy of the highest state
included. Used only when ``Xatu_interface`` is ``true``.

It cannot exceed the number of states Xatu wrote. Asking for more stops the run and tells you how many
are actually there:

.. code-block:: text

   ERROR (get_exciton_data): Exciton_cutoff =  600 but only  500
          exciton energies are present in MoSe2_N45.eigval
          Lower Exciton_cutoff to at most  500 , or rerun Xatu with a larger -n.

.. note:: **Cost**

   Runtime of the excitonic second-order matrix elements grows as :math:`N^2`. Memory is dominated by
   terms **linear** in :math:`N` — the exciton envelopes and their k-derivative, which are
   :math:`\texttt{norb\_ex} \times N` — plus :math:`8N^2` complex numbers for the accumulators, and
   it does **not** depend on the thread count. In practice the cutoff is rarely the binding constraint
   any more: the complete 5625-state basis of a 75x75 two-band model costs 27.8 s and 6.6 GB, and the
   complete **8100-state** basis of the same model on a 90x90 mesh costs 76 s and 12.9 GB. Both are
   the entire BSE space, so neither has a truncation edge anywhere.

   Use :ref:`kw-cache` for any study that sweeps ``Response``, the frequency window or the broadening —
   the matrix elements do not depend on any of those.

.. _kw-omesp:

OME_sp
------

.. code-block:: text

   # OME_sp
   linear

Controls the **single-particle optical matrix elements** (OME), which are computed on the whole k-mesh
and written to disk:

``linear``
   Velocity matrix elements and band energies. Enough for ``absorbance``. Written to the text file
   ``ome_linear_sp_<material>.omesp``.

``nonlinear``
   Everything in ``linear``, plus the quantities second-order responses need: Berry connections, shift
   vectors, generalised derivatives, k-derivatives of :math:`|v|`, and the gauge-fixed
   (parallel-transported) complex generalised derivative of :math:`v` that Eq. (A3a) needs. Required for
   every ``shift_*`` response and for ``shg``, ``electrooptic``, ``rectification`` and ``general``.
   Written to the binary file ``ome_nonlinear_sp_<material>.omesp``.

``none``
   Compute nothing, and read the matrix elements from the file left by a previous run in the same
   directory. See :doc:`workflows`.

The response reads the file that matches its order. ``absorbance`` reads the *linear* file, and the
shift responses read the *nonlinear* file. Pair them accordingly:

.. list-table::
   :header-rows: 1

   * - ``Response``
     - ``OME_sp`` (this run)
     - or, with ``OME_sp = none``, this file must exist
   * - ``absorbance``
     - ``linear``
     - ``ome_linear_sp_<material>.omesp``
   * - ``shift_*``, ``shg``, ``electrooptic``, ``rectification``, ``general``
     - ``nonlinear``
     - ``ome_nonlinear_sp_<material>.omesp``

.. _kw-omeex:

OME_ex
------

.. code-block:: text

   # OME_ex
   linear

Controls the **excitonic optical matrix elements**, built from the Xatu envelopes and the
single-particle matrix elements. Only relevant when ``Xatu_interface`` is ``true``.

``linear``
   Ground-state-to-exciton matrix elements. Needed for the excitonic ``absorbance``. Written to
   ``ome_linear_ex_<material>.omeex``.

``nonlinear``
   Additionally computes the exciton-to-exciton (inter-exciton) matrix elements needed for the excitonic
   shift current. These stay in memory and are not written to disk unless you enable
   :ref:`kw-cache`.

``none``
   Compute nothing. For ``absorbance``, the excitonic matrix elements are read from
   ``ome_linear_ex_<material>.omeex``.

.. important::

   * The excitonic shift current needs ``OME_ex = nonlinear`` **in the same run**, because the
     inter-exciton elements are not kept in a file. Use ``Cache_ome_ex`` to avoid recomputing them.
   * When ``OME_ex`` is ``linear`` or ``nonlinear``, ``OME_sp = none`` is **refused** and the run
     stops. The exciton envelopes must be carried into the same band gauge as the single-particle
     states, and the per-k rotation matrices that do it are rebuilt only while ``OME_sp`` is being
     computed — they are not stored in the ``.omesp`` file. With ``OME_sp = none`` the two would sit in
     different bases inside every near-degenerate multiplet, and the error is :math:`O(1)`: on In\ :sub:`2`\ Se\ :sub:`3` it
     moves the excitonic SHG by 13% of the largest tensor component and by more than 100% of several
     smaller ones.

     The **one exception** is a :ref:`kw-cache` *hit*, which supplies the excitonic matrix elements
     directly and never touches the envelopes. ``OME_sp = none`` together with ``Cache_ome_ex = read``
     is therefore valid, and is the intended fast path for scanning several ``Response`` branches over
     one set of matrix elements. A cache *miss* under the same settings stops rather than quietly
     recomputing in a mismatched basis.

.. _kw-response:

Response
--------

.. code-block:: text

   # Response
   absorbance

Which optical response to compute:

``absorbance``
   Linear optical conductivity :math:`\sigma^{ab}(\omega)`, full :math:`3\times 3` tensor. Output:
   :doc:`outputs/linear_conductivity`.

``shift``
   Shift conductivity :math:`\sigma^{abc}(0;\omega,-\omega)` by the recommended method:
   ``shift_covariant`` with the default :ref:`kw-sp-method`, ``shift_shiftvector`` with
   ``Sp_method = per_band``. **Use this unless you want a specific method.** Output:
   :doc:`outputs/shift_conductivity`.

``shift_shiftvector``
   Shift conductivity from the shift-vector formula, with the amplitude-gradient correction. It drops band
   pairs closer than 2.7 meV, which costs accuracy where bands are degenerate (MoS\ :sub:`2`: 9% symmetry
   residual). Output: :doc:`outputs/shift_conductivity`.

``shift_covariant``
   Shift conductivity from paper Eq. (9) with a generalised derivative that is covariant over groups of
   (nearly) degenerate bands (:ref:`shift-covariant`). Needs **no degeneracy cut-off**, so it stays
   symmetric where bands are degenerate, e.g. along the :math:`\Gamma`–M lines of MoS\ :sub:`2` or on non-symmorphic zone
   boundaries. Same output files as ``shift_shiftvector``. The ``.omesp`` file must have been written by a
   ``shift_covariant`` run (or any run with ``Sp_method = covariant``). Single-particle only; the
   excitonic result is unaffected. Default for ``Response = shift`` since 2026-10-06.

``shift_sumrule``
   Shift conductivity from the sum-rule form of the generalised derivative. It is only reliable when
   ``Bandlist`` includes many remote bands; for a two-band window it is :math:`\approx` 0. OptiX prints a warning when
   it is used. Mostly useful as a cross-check.

``shift_gender``
   Reserved for a numerical generalised-derivative method. **Not implemented yet**: the single-particle
   result is identically zero.

``shg_covariant``
   Same as ``shg`` with ``Sp_method = covariant``, whatever that keyword says. Since 2026-10-06 this is
   also what plain ``shg`` does by default.

``shg``
   Second-harmonic generation, :math:`\sigma^{abc}(2\omega;\omega,\omega)`. Output:
   :doc:`outputs/second_order`. Note that column 1 of the file is the **fundamental** photon energy
   :math:`\hbar\omega`, not :math:`2\hbar\omega`.

``electrooptic``
   Linear electro-optic (Pockels) response, :math:`\sigma^{abc}(\omega;\omega,0)`. This is the branch
   most sensitive to the k-mesh; see :doc:`theory/second_order`.

``rectification``
   Optical rectification, :math:`\sigma^{abc}(0;\omega,-\omega)`, the DC limit. The excitonic result
   is the shift current, by a second route. The single-particle result also contains the off-resonant
   terms and the injection current. On resonance it equals the shift current, and the rest vanishes as
   :math:`\eta\to0`. Read :ref:`dc-limit` for the conventions and why the anti-diagonal of a 2D map is
   different.

``general``
   The two-frequency response :math:`\sigma^{abc}(\omega_1+\omega_2;\omega_1,\omega_2)` at an
   arbitrary ratio set by :ref:`kw-ratio`, or a full two-dimensional map when :ref:`kw-energy2` is
   present. ``Frequency_ratio`` of 1, 0 and -1 reproduce ``shg``, ``electrooptic`` and
   ``rectification`` respectively.

``none``
   Compute no response. Useful to only produce the matrix-element files (see :doc:`workflows`).

Any other value stops the program with a list of the valid options. All second-order responses need
``OME_sp = nonlinear`` (and ``OME_ex = nonlinear`` for the excitonic result).

All second-order outputs use one normalisation and the physical sign of the electron charge
(:ref:`second-order-normalisation`, since 2026-10-06).

.. _kw-sp-method:

Sp_method
---------

.. code-block:: text

   # Sp_method
   covariant

Optional (default ``covariant``), case insensitive. Chooses how the **single-particle** second-order
responses are computed. The excitonic results do not depend on it.

``covariant``
   Uses a generalised derivative that is covariant over groups of nearly degenerate bands
   (:ref:`shift-covariant`, :ref:`shg-covariant`), so no band pairs are dropped and no degeneracy
   cut-off is applied. ``shift`` runs ``shift_covariant``. ``shg``, ``electrooptic``, ``rectification``
   and ``general`` evaluate Eq. (B1b) of Taghizadeh & Pedersen 2018 in the independent-particle limit.

``per_band``
   The earlier per-band routes: ``shift`` runs ``shift_shiftvector``, and the other responses evaluate
   Eq. (A3a) of Taghizadeh *et al.* 2017. They need each band's phase to be differentiable, so they fail
   where bands are degenerate (MoS\ :sub:`2`: 85–92% symmetry residual, against 1–4% with ``covariant``). Kept
   for comparison.

On models without degeneracies the two agree, e.g. hBN to :math:`10^{-10}` (SHG) and
:math:`4\times10^{-5}` (rectification). ``covariant`` costs extra diagonalisations in the matrix-element
stage and writes a larger ``.omesp``. With ``OME_sp = none``, the ``.omesp`` read back must come from a
``covariant`` run; otherwise OptiX stops and says so. The explicit names ``shift_shiftvector`` and
``shift_covariant`` ignore this keyword. Any value other than the two above stops the program.

.. _kw-energy:

Energy_variables
----------------

.. code-block:: text

   # Energy_variables
   1 9 0.025 400

Four numbers on one line: ``E_min  E_max  eta  n_w``.

``E_min``, ``E_max`` (eV)
   Photon-energy window :math:`\hbar\omega`.

``eta`` (eV)
   Broadening of the spectral lines: the half-width for a Lorentzian, the standard deviation for a
   Gaussian (see :ref:`kw-broadening`).

``n_w`` (integer)
   Number of frequency points.

The grid is :math:`\hbar\omega_i = E_\text{min} + (i-1)\,\Delta` with
:math:`\Delta = (E_\text{max}-E_\text{min})/n_w` and :math:`i = 1,\dots,n_w`. **The last point is**
:math:`E_\text{max}-\Delta` **, so** :math:`E_\text{max}` **itself is not included.** With
``1 9 0.025 400`` the grid runs 1.00, 1.02, ..., 8.98 eV.

``eta`` should be comparable to, or larger than, the typical energy spacing between transitions on
your k-mesh. Otherwise the spectrum shows spurious mesh oscillations. Denser meshes allow smaller
``eta``.

.. _kw-ratio:

Frequency_ratio
---------------

.. code-block:: text

   # Frequency_ratio
   -1.0

Optional real number :math:`r` (default ``1.0``). Sets :math:`\omega_2 = r\,\omega_1` for
``Response = general``. It is ignored by every other ``Response``, and it is overridden by
:ref:`kw-energy2`.

:math:`r = 1` is second-harmonic generation, :math:`r = 0` the electro-optic response and
:math:`r = -1` optical rectification, so ``general`` with these three values reproduces the dedicated
branches. Any other value is a sum-frequency response.

.. note::

   At :math:`r = -1` OptiX switches to the DC convention described in :ref:`dc-limit` — the same
   convention ``Response = rectification`` uses. This happens only for a **one-dimensional** scan; a 2D
   map does not switch. That is deliberate, and it is the single most important thing to know before
   reading a map along its anti-diagonal.

.. _kw-energy2:

Energy_variables_2
------------------

.. code-block:: text

   # Energy_variables_2
   -1.8 1.8 480

Optional. Three numbers: ``F_min  F_max  n_wb``, an **independent** :math:`\omega_2` grid in eV, built
the same way as :ref:`kw-energy` (so ``F_max`` is not included). Its presence turns
``Response = general`` into a full two-dimensional map over :math:`(\omega_1,\omega_2)` and overrides
:ref:`kw-ratio`. The broadening ``eta`` is shared with ``Energy_variables``.

The output has :math:`n_w\times n_{wb}` rows with :math:`\omega_1` as the slow index; see
:doc:`outputs/second_order`. Cost scales with the product, so a 320x480 map is 153 600 frequency pairs.

:math:`\omega_2` may be negative. If the grid contains a point with
:math:`\omega_1 + \omega_2 = 0`, OptiX evaluates the **whole** map with Eq. (B1a) (method A), because
Eq. (B1b)'s prefactor vanishes there; the log says which form was used.

.. warning::

   The line :math:`\omega_2 = -\omega_1` of a map is **not** the shift current. See
   :ref:`dc-antidiagonal`.

.. _kw-broadening:

Broadening_type
---------------

.. code-block:: text

   # Broadening_type
   gaussian

Optional, case insensitive. Shape of the function that replaces the energy-conserving
:math:`\delta(\hbar\omega - \Delta E)`:

``lorentzian`` *(default)*
   :math:`\dfrac{1}{\pi}\dfrac{\eta}{(\hbar\omega-\Delta E)^2+\eta^2}`

``gaussian``
   :math:`\dfrac{1}{\sqrt{2\pi}\,\eta}\exp\!\left[-\dfrac{(\hbar\omega-\Delta E)^2}{2\eta^2}\right]`

Both are normalised to one. Any other value falls back to Lorentzian. ``# Broadening`` is accepted as
the label too.

.. _kw-exk:

Write_ex_kresolved
------------------

.. code-block:: text

   # Write_ex_kresolved
   true

Optional (default ``false``). With ``OME_ex = linear``, it also writes the **k-resolved** contribution
to each exciton's optical matrix element to ``ome_linear_ex_k_<material>.omeexk`` (see
:doc:`outputs/matrix_elements`). This is useful for seeing where in the Brillouin zone an exciton's
brightness comes from. It has no effect for ``OME_ex = nonlinear``.

.. _kw-cache:

Cache_ome_ex
------------

.. code-block:: text

   # Cache_ome_ex
   readwrite

Optional (default ``off``), case insensitive. It controls an on-disk cache of the **second-order
excitonic matrix elements** (``OME_ex = nonlinear``). Building them is the most expensive part of an
excitonic shift-current run, and the cache lets later runs skip it.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Value
     - Behaviour
   * - ``off`` (= ``false``, ``none``)
     - No cache.
   * - ``write``
     - Compute the elements and save them to ``ome_second_ex_<material>.omeex2``.
   * - ``read``
     - Load them from that file if it matches the current system; otherwise compute them (without saving).
   * - ``readwrite`` (= ``true``, ``both``)
     - Load if possible; otherwise compute and save.

Each time it reads, OptiX checks that the cache belongs to the current calculation:

* material name, number of k-points, and numbers of valence and conduction bands — a mismatch **stops**
  the run;
* the **band list** itself, not just the band counts — a different band set, *or the same bands in a
  different order*, **stops** the run;
* exciton energies, compared against the current ``.eigval`` — a mismatch **stops** the run;
* how the inter-exciton position elements were built (``Xnm_derivative``) — a mismatch **stops** the
  run;
* number of stored excitons — if the cache has fewer than ``Exciton_cutoff``, it is recomputed. A cache
  with *more* excitons is fine, and the needed subset is used.

.. warning::

   The cache does **not** fingerprint the Wannier90 file. If you change the tight-binding model but
   keep the same file name and exciton spectrum, delete the cache by hand.

.. note::

   **Format version 2.** Caches written before 2026-09-30 are version 1, which recorded only the band
   *counts*. Counts cannot distinguish a band list of ``[60, 61]`` from ``[61, 60]``, and that exact
   ambiguity once let a whole set of results be computed with two conduction bands swapped. Version 2
   stores the list itself.

   A version 1 file is now treated as a **clean miss**: OptiX says so and recomputes, because the order
   it was written with cannot be recovered from the file. Delete it. Regenerating is much cheaper than
   it used to be — the exciton k-loop is now batched into one matrix multiply per term.

   **Format version 3** (2026-10-04) also records the ``Xnm_derivative`` method. Version 2 files are
   clean misses for the same reason: they were built with the old inter-exciton position elements, which
   can be wrong by O(1) on multi-band spin–orbit models (see :ref:`kw-xnm`).

The file is large: about :math:`96\,N^2` bytes for :math:`N` = ``Exciton_cutoff`` (:math:`\approx` 340 MB for
:math:`N = 1875`, :math:`\approx` 3 GB for :math:`N = 5625`). The cache is not used when ``Write_ex_kresolved`` is
``true``.

A hit skips more than the exciton k-loop. It also skips **reading the exciton envelopes** from the
``.states`` file, since the cached matrix elements are exactly what the k-loop would have built from
them. That read is plain ASCII and can dominate start-up for a large exciton basis — on a
2700-exciton ReS\ :sub:`2` run it is 1.9 GB and 16.8 s, against 0.9 s to read the 700 MB binary cache — so a
cached run starts in seconds rather than tens of seconds. If the cache turns out to miss, the
envelopes are read at that point instead, costing exactly what they would have cost anyway.

.. _kw-xnm:

Xnm_derivative
--------------

.. code-block:: text

   # Xnm_derivative
   covariant

Optional (default ``covariant``), case insensitive. It selects how the **inter-exciton position matrix
elements** :math:`X_{nm}` are evaluated. These feed every excitonic second-order response.
:math:`X_{nm}` contains a k-derivative of the exciton envelopes, which are expressed in the band basis,
so the derivative is only meaningful if that basis varies smoothly from one k-point to the next.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Value
     - Behaviour
   * - ``covariant``
     - Each neighbouring envelope is first carried into the band basis at k, using the overlaps of the
       band states between the two k-points, and only then differenced (fourth-order stencil). The result
       does not depend on the phases of the band states, or on how bands are mixed inside a degenerate
       group, so it is safe for any model.
   * - ``finite_difference`` (= ``plain``)
     - The original method: a plain difference of the envelopes between neighbouring k-points. It is
       correct only where the band phases vary smoothly, which holds for simple models like hBN but not
       for models with many orbitals and spin–orbit coupling.

On monolayer MoS\ :sub:`2` (34 orbitals, spin–orbit coupling) the phase convention jumps on about 12% of the links
between neighbouring k-points. The ``finite_difference`` method then breaks the crystal's threefold
symmetry by 20–65% in the excitonic shift, rectification and SHG spectra, against 2–5% with
``covariant``. On hBN the two agree, and ``covariant`` is the more accurate of the two (see
:doc:`changes`). Keep the default unless you are reproducing results from before 2026-10-04.

.. _kw-basis-repair:

Exciton_basis_repair
--------------------

.. code-block:: text

   # Exciton_basis_repair
   true

Optional (default ``true``), case insensitive; used with ``Xnm_derivative = covariant``. Where two bands of
the window are exactly degenerate at a k-point — for MoS\ :sub:`2`, along the :math:`\Gamma`–M lines — any combination of the two
states is an equally valid choice, and Xatu writes the exciton envelopes in whichever one its eigensolver
returned. OptiX cannot read that choice from the Xatu files. Left alone, it changes the excitonic
second-order spectra of MoS\ :sub:`2` by 25–35%, depending only on which choice Xatu happened to make.

With ``true``, OptiX determines the choice itself. At each such k-point it picks the combination that makes
the envelopes vary smoothly from the neighbouring k-points, using all excitons at once. The spectra then no
longer depend on Xatu's choice, and the symmetry residual of MoS\ :sub:`2` drops to the level reached when the
degeneracy is lifted. The log reports how many k-points were treated. Models without exact degeneracies,
such as hBN, are not affected.
