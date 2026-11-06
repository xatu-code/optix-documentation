==========
Input file
==========

An OptiX calculation is controlled by one plain-text input file, passed as the only command-line
argument:

.. code-block:: bash

   opticx input.txt

Besides the input file itself, a run needs:

* a **Wannier90 tight-binding file** (``<seedname>_tb.dat``) — always;
* the Xatu **exciton files** — only for excitonic calculations: either the ``.eigval`` and ``.states`` text
  files, or one HDF5 archive ``<label>.h5`` (``xatu -H``, read by an OptiX built with ``make HDF5=1``).

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
     - ``true``/``false``; if ``true``, followed by the ``.eigval`` and ``.states`` paths, or by one ``.h5`` path.
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
     - excitonic only, optional
     - Number of exciton states used (default: all in the Xatu files).
   * - :ref:`kw-omesp`
     - always
     - Single-particle matrix elements: ``linear``, ``nonlinear`` or ``none``.
   * - :ref:`kw-omeex`
     - excitonic only
     - Excitonic matrix elements: ``linear``, ``nonlinear`` or ``none``.
   * - :ref:`kw-response`
     - always
     - ``absorbance``, ``shift``, ``shift_shiftvector``, ``shift_covariant``, ``shift_sumrule``, ``shift_gender``, ``shg``,
       ``shg_covariant``, ``electrooptic``, ``rectification``, ``general``, ``bands`` or ``none``.
   * - :ref:`kw-sp-method`
     - optional
     - Single-particle second-order method: ``covariant`` (default) or ``per_band``.
   * - :ref:`kw-scissor`
     - optional
     - Rigid shift of the conduction bands (eV), and whether positions or velocities are kept.
   * - :ref:`kw-band-phase`
     - excitonic only, optional
     - Phase rule of Xatu's band states when the exciton input does not store them: ``sum`` (default) or ``weighted``.
   * - :ref:`kw-ex-rect`
     - obsolete
     - Ignored if ``causal``; ``shift`` stops (use ``Response = shift``).
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
   * - :ref:`kw-kpath`
     - optional
     - Path for the band structure: vertices in reduced coordinates, each with the number of points to the next.
   * - :ref:`kw-kpath-labels`
     - optional
     - One label per ``Kpath`` vertex.

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
rectification agree to :math:`2\times10^{-9}` or better.

**Excitons on a non-orthonormal model.** The exciton envelopes are coefficients on Xatu's band states, so OptiX
must use the same states, phases included. Xatu fixes each band's phase by making the sum of its eigenvector's
coefficients real, and with an overlap those coefficients are the Lowdin ones, :math:`S^{1/2}c`; OptiX applies
the same rule to :math:`S^{1/2}c` (since 2026-10-21). Checked against Xatu on a MoSe\ :sub:`2` model with
spin-orbit coupling from CRYSTAL (87x87, 2v x 4c): the excitonic absorbance agrees to :math:`1.3\times10^{-3}`,
the single-particle one to :math:`2.5\times10^{-3}`. An ``.omesp`` written by an earlier version for a
non-orthonormal model carries the old phases; an excitonic run that reads it with ``OME_sp = none`` stops and
asks for it to be regenerated.

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

Instead of the two text files, ``true`` can be followed by **one** path, that of a Xatu HDF5 archive
(``<label>.h5``, written by ``xatu -H`` with the ``-c`` flag). OptiX recognises it by its extension, ``.h5``
or ``.hdf5``:

.. code-block:: text

   # Xatu_interface
   true
   /home/user/xatu_run/hBN.h5

Reading an archive needs an OptiX built with ``make HDF5=1`` (see :doc:`installation`). It holds the same
information at full double precision (the text files carry 7 to 8 significant digits) and states the band
window, the k-mesh and the exciton count explicitly, which allows three checks the text files cannot support.
OptiX stops if:

* ``Nfermi`` differs from the filling of the Xatu run;
* the archive's k-mesh is not the mesh OptiX builds itself (a Xatu ``submesh`` or ``shift``, or a run
  on a different lattice);
* the exciton basis is not in the order OptiX indexes it (k slowest, then conduction, then valence).

``Bandlist`` may then be given only if it equals the archive's band window. Without ``Exciton_cutoff``
every exciton in the archive is used. Text output of earlier Xatu runs converts to an archive with
``tools/xatu_text_to_h5.py`` (``--nfermi`` and ``--ndim`` supply what the text files do not record). It
converts one exciton at a time, so it needs little memory whatever the size of the run, parses the text in
parallel (``-j N`` worker processes, default the CPUs available to the job, at most 32), and
``--compression N`` (gzip level 1-9) compresses the archive, though only by a few per cent for text-converted
data, whose coefficients carry 7 significant digits.

Any value other than ``true`` or ``false`` stops the program.

With ``true``, OptiX takes the **k-mesh** and the **band window** from the ``.states`` file (or the archive). That makes
the single-particle and excitonic calculations use exactly the grid and bands Xatu used. In that case:

* do **not** give ``Bandlist`` with the text files; it would clash with the band list read from Xatu (with an
  archive it may be given, but must equal the archive's window);
* ``Ncells`` is ignored;
* Xatu must have been run on the **same Wannier90 file**, with ``--w90 <filling>`` where
  ``<filling>`` equals ``Nfermi``, and with the ``-e`` and ``-c`` output flags (``-c -H`` for an archive);
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

It is a **list, not a range**: ``-1 2`` selects two bands (the second valence and the second conduction band)
and skips both frontier bands; four bands are ``-1 0 1 2``. OptiX prints the resolved window,
``Band window (offset from Nfermi -> band): -1->25 0->26 1->27 2->28``, and warns
(``WARNING (Bandlist): unusual band window``) when the list omits offset 0 or 1, leaves a gap, or repeats an
entry. The same check applies to the band list of a Xatu ``.states`` file. Such a window is allowed, but it
cuts degenerate pairs; on MoS\ :sub:`2` the window ``-1 2`` gave a rectification dominated by a
symmetry-forbidden component.

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

With Xatu, this **must match** the filling passed to ``xatu --w90``. OptiX checks it: the ``.states`` file
(or the HDF5 archive) says which bands Xatu took as valence and which as conduction, and a ``Nfermi`` that
puts them on the wrong side of the Fermi level stops the run at once, naming the value to use. Any window
without a conduction band or without a valence band also stops the run (except ``Response = bands``).

``Nfermi`` must put the Fermi level in a gap **at every k-point**: occupations follow the band index, not
the energy. If band ``Nfermi`` reaches higher than band ``Nfermi + 1`` anywhere on the mesh, or the two
touch, OptiX prints a ``WARNING`` with both energies. Such a filling describes a metal, and the
second-order responses then contain poles at vanishing transition energy (on GeS, ``Nfermi = 21`` turns :math:`\sigma^{xyy} = 135` into 10566; see :doc:`troubleshooting`).

.. _kw-cutoff:

Exciton_cutoff
--------------

.. code-block:: text

   # Exciton_cutoff
   100

Number of exciton states, lowest in energy first, read from the Xatu files and included in the
excitonic response. The spectrum is converged only up to roughly the energy of the highest state
included. Used only when ``Xatu_interface`` is ``true``.

Optional. Without it OptiX uses every exciton Xatu wrote, and says so in the log
(``Exciton_cutoff not given: using all 900 excitons in the Xatu files``, or ``... in the Xatu archive``). An
archive states the count explicitly. For the text files it is the third line of the ``.eigval`` file; the first line of the ``.states`` file is the size of the exciton basis, which is the
same number only when Xatu wrote every state. Mind the cost (below) before running a large file in full.

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
   (parallel-transported) complex generalised derivative of :math:`v` that Eq. (A3a) needs, and the
   block-covariant data of both covariant methods. Required for every ``shift_*`` response and for
   ``shg``, ``electrooptic``, ``rectification`` and ``general``. Written to the binary file
   ``ome_nonlinear_sp_<material>.omesp``, which serves **every** second-order ``Response`` afterwards
   with ``OME_sp = none``, whichever ``Response`` wrote it.

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
   Additionally computes the exciton-to-exciton (inter-exciton) matrix elements needed for every
   excitonic second-order response. These stay in memory and are written to disk only through
   :ref:`kw-cache`, from which later runs read them with ``OME_ex = none``.

``none``
   Compute nothing. For ``absorbance``, the excitonic matrix elements are read from
   ``ome_linear_ex_<material>.omeex``. For a second-order ``Response`` they are read from the
   :ref:`kw-cache` file, the excitonic counterpart of ``OME_sp = none``: set ``Cache_ome_ex = read`` (or
   ``readwrite``). Neither the envelopes nor anything else is computed, so a missing or non-matching cache
   **stops** the run, as does ``OME_ex = none`` on a second-order run without ``Cache_ome_ex``.

.. important::

   * The inter-exciton elements of the second-order responses are kept only in memory and in the
     :ref:`kw-cache` file. Compute them with ``OME_ex = nonlinear`` (and ``Cache_ome_ex = write`` or
     ``readwrite`` to keep them); later runs read them with ``OME_ex = none`` and ``Cache_ome_ex = read``.
   * ``OME_ex = linear`` or ``nonlinear`` may be combined with ``OME_sp = none``. The exciton envelopes
     must be carried into the same band basis as the single-particle states, using per-k rotation
     matrices built while ``OME_sp`` is computed; the ``.omesp`` file stores them, together with the
     exciton-window states the covariant :math:`X_{NN'}` needs (since 2026-10-06). On
     In\ :sub:`2`\ Se\ :sub:`3`, ``OME_sp = none`` then reproduces the full calculation to
     :math:`4\times10^{-16}` (SHG and absorbance), in 2 s instead of 14 s.

     An ``.omesp`` written by an earlier version lacks them, and the run **stops** rather than mixing
     bases: the error would be :math:`O(1)` (on In\ :sub:`2`\ Se\ :sub:`3`, 13% of the largest SHG
     component and more than 100% of several smaller ones). Regenerate the file once with ``OME_sp`` set,
     or use a :ref:`kw-cache` *hit*, which supplies the excitonic matrix elements directly and never
     touches the envelopes.

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
   Optical rectification, the whole :math:`\sigma^{abc}(0;\omega,-\omega)` with causal broadening, on both
   paths: the symmetric real part and, in the antisymmetric imaginary part, the injection current. It is
   continuous with the anti-diagonal of a 2D map. In the independent-particle limit its real part equals
   the shift current on resonance, plus off-resonant terms that vanish as :math:`\eta\to0`; with bound
   excitons it differs from the shift current (buckled hBN: 0.53 of it). For the shift current itself use
   ``shift``. Read :ref:`dc-limit`.

``general``
   The two-frequency response :math:`\sigma^{abc}(\omega_1+\omega_2;\omega_1,\omega_2)` at an
   arbitrary ratio set by :ref:`kw-ratio`, or a full two-dimensional map when :ref:`kw-energy2` is
   present. ``Frequency_ratio`` of 1, 0 and -1 reproduce ``shg``, ``electrooptic`` and
   ``rectification`` respectively.

``bands``
   Write the band structure (:doc:`outputs/bands`) and stop, before any matrix element is computed. Use it to
   choose ``Nfermi`` and ``Bandlist`` for a new model. Needs only the model, ``Periodic dimensions``,
   ``Xatu_interface = false``, ``Ncells`` (any value), ``Bandlist``, ``Nfermi`` and, optionally, :ref:`kw-kpath`.
   With Xatu input it also works, and checks the Xatu files against the model, but it reads no exciton
   envelopes, so it takes seconds even for a complete exciton basis.

``none``
   Compute no response. Useful to only produce the matrix-element files (see :doc:`workflows`).

Any other value stops the program with a list of the valid options. All second-order responses need the
nonlinear single-particle matrix elements (``OME_sp = nonlinear``, or ``none`` with an
``ome_nonlinear_sp_<material>.omesp`` from any earlier second-order run) and, for the excitonic result,
the inter-exciton elements (``OME_ex = nonlinear``, or ``none`` with ``Cache_ome_ex = read``).

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

.. _kw-scissor:

Scissor and Scissor_mode
------------------------

.. code-block:: text

   # Scissor
   1.0
   # Scissor_mode
   r_unchanged

Optional. ``Scissor`` (eV, default 0) shifts every conduction band rigidly,
:math:`E_c \to E_c + \Delta`, in the single-particle responses and in the excitonic matrix elements between the
ground state and the excitons. It is applied when the responses are computed: the ``.omesp`` always holds the
unshifted model, so ``OME_sp = none`` works with any ``Scissor``. Only conduction-valence pairs change; energy
differences, positions and velocities within the valence or within the conduction bands do not.

``Scissor_mode`` (default ``r_unchanged``, case insensitive) chooses what the shift keeps fixed, with
:math:`\omega_{cv} = E_c - E_v` before the shift:

``r_unchanged``
   The interband position elements :math:`r_{cv}` are kept and the velocities are rescaled,
   :math:`v_{cv} \to v_{cv}(\omega_{cv}+\Delta)/\omega_{cv}`: the scissor operator
   :math:`\Delta P_c`, which commutes with the position operator (Levine & Allan, PRL 63, 1719 (1989); Nastos
   *et al.*, PRB 72, 045223 (2005) for second order). The shift current moves rigidly by :math:`\Delta`, and the
   excitonic route with non-interacting excitons agrees with the single-particle route as it does without a scissor.
   This default reproduces Xatu's Kubo conductivity (MoSe\ :sub:`2` with spin-orbit coupling, 60x60, 2 valence and 8
   conduction bands: single-particle within :math:`2\times10^{-3}`, excitonic xx :math:`1.7\times10^{-3}`).

``v_unchanged``
   The velocities are kept and the positions rescaled, :math:`r_{cv} \to r_{cv}\,\omega_{cv}/(\omega_{cv}+\Delta)`.
   No Hamiltonian has these matrix elements, so expressions that
   are equivalent for a real model can disagree: on buckled hBN (30x30, :math:`\Delta` = 1 eV) the excitonic and
   single-particle routes differ by 1.2% in the out-of-plane shift components (zxx, zyy, xxz, yyz), against
   :math:`3\times10^{-4}` with ``r_unchanged``. In-plane components agree in both modes.

What changes with each mode: the single-particle energies in every lineshape and denominator (both modes); the
single-particle velocities (``r_unchanged``) or positions (``v_unchanged``) of conduction-valence pairs; for
excitons, :math:`P_n` (``r_unchanged``, used by the linear response) or :math:`X_n` (``v_unchanged``, used by the
second-order responses). Single-particle second order is supported with the default :ref:`kw-sp-method` only;
``per_band`` with a scissor stops the run.

**Excitons.** Xatu applies its own scissor (``scissor`` in the exciton configuration) to the BSE; give OptiX the same
value. With a Xatu archive, OptiX compares ``Scissor`` with the scissor the archive records and stops if they
differ. Text files and archives converted from them record none, and the log says the value could not be checked.
The second-order excitonic cache (:ref:`kw-cache`) records the scissor and its mode, and a cache written with
different ones stops the run. Any ``Scissor_mode`` other than the two above stops the program.

.. _kw-band-phase:

Band_phase
----------

.. code-block:: text

   # Band_phase
   weighted

Optional, excitonic runs only. The exciton envelopes are coefficients on Xatu's band states; OptiX rebuilds those
states from the model and must give each band the phase Xatu gave it. Xatu fixes a band's phase by making a sum of
its coefficients :math:`c_i` real (with an overlap, of the Lowdin coefficients :math:`S^{1/2}c`):

``sum`` (default)
   :math:`\sum_i c_i` real.

``weighted``
   :math:`\sum_i w_i c_i` real, :math:`w_i = e^{2\pi i g (i-1)}`, :math:`g = (\sqrt{5}-1)/2`: Xatu builds that avoid
   the plain sum's accidental zeros (it vanishes for symmetric or antisymmetric orbital combinations, and the phase
   is then rounding noise).

The keyword matters only when the exciton input does not store the band states: Xatu text output, and archives
converted from it. An archive written by ``xatu -H -c`` stores them (``/bands/eigenvectors``), and OptiX then takes
the exciton-window states from it directly, at degenerate k-points too, and ignores ``Band_phase`` (the log says
so, names the rule it finds in the archive, and reports the overlap deficit between Xatu's states and OptiX's; a
deficit above :math:`10^{-2}` means another model and stops the run). A wrong rule does not stop anything: it
scrambles every excitonic matrix element (In\ :sub:`2`\ Se\ :sub:`3` 102x102: excitonic absorbance xx - yy 34%
where C3 requires 0). If in doubt, compare OptiX's linear excitonic absorbance with Xatu's own. The ``.omesp`` and
the excitonic cache record which states they hold, and reading one made for other states stops the run.

.. _kw-ex-rect:

Ex_rectification
----------------

**Obsolete since 2026-10-07.** The excitonic rectification is always the whole causal
:math:`\sigma^{abc}(0;\omega,-\omega)`, injection current included (:ref:`dc-excitonic-rectification`); the shift
current in the convention of the reference paper is ``Response = shift``. ``Ex_rectification = causal`` is
accepted and ignored, with a note in the log. ``Ex_rectification = shift`` stops the run and points to
``Response = shift``, so an old input never silently returns a different quantity.

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

   At :math:`r = -1` the scan is ``Response = rectification``: causal broadening as everywhere, evaluated
   with Eq. (B1a) and the bare exciton-exciton current in its term 3 (:ref:`dc-excitonic-rectification`).
   It is not the shift current; that is ``Response = shift``.

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
:math:`\omega_1 + \omega_2 = 0`, OptiX evaluates the **whole** map with Eq. (B1a) (method A, term 3 on the
bare exciton-exciton current), and its anti-diagonal then equals ``Response = rectification`` point by
point; the log says which form was used.

.. warning::

   The line :math:`\omega_2 = -\omega_1` of a map is **not** the shift current. See
   :ref:`dc-antidiagonal`.

.. _kw-kpath:

Kpath
-----

.. code-block:: text

   # Kpath
    0.00000000  0.00000000  0.00000000  150
    0.50000000  0.00000000  0.00000000  100
    0.33333333  0.33333333  0.00000000  150
    0.00000000  0.00000000  0.00000000  1

Optional. The path of the band structure written to ``bands_<material>.dat``, one vertex per line: three
**reduced coordinates** along the reciprocal lattice vectors (in the order of the lattice vectors of the
``_tb.dat`` file) and the **number of points** from this vertex to the next. The last vertex takes ``1`` to be
included (``0`` leaves it out). A count of ``1`` on an intermediate vertex writes that vertex alone and jumps to
the next one, so a path can be broken (e.g. ``... K 1`` then ``M ...``); the path length does not advance across
the jump. The block ends at the next ``#`` line, a blank line or the end of the file.

Reduced coordinates depend on the choice of lattice vectors: for a hexagonal lattice K is
:math:`(\tfrac13,\tfrac13)` when the reciprocal vectors are 60 degrees apart and :math:`(\tfrac23,\tfrac13)` when they
are 120 degrees apart (as in the ``hBN_tb.dat`` of the examples). The file header lists the reduced coordinates of
every vertex, and the default path finds K itself.

Without ``Kpath`` OptiX uses a default for the lattice: :math:`\Gamma`-M-K-:math:`\Gamma` for a hexagonal 2D lattice,
:math:`\Gamma`-X-S-Y-:math:`\Gamma` for any other 2D lattice (X, Y, S at :math:`\tfrac12` of the reciprocal vectors and
their sum), the same plus :math:`\Gamma`-Z in 3D, and :math:`\Gamma`-X in 1D, with about 300 points in all.

.. _kw-kpath-labels:

Kpath_labels
------------

.. code-block:: text

   # Kpath_labels
   G M K G

Optional. One label per ``Kpath`` vertex, separated by spaces; they are written to the file header (and used by
``tools/plot_bands.py``, which draws ``G`` as :math:`\Gamma`). With a different number of labels than vertices they
are ignored with a warning.

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
excitonic matrix elements**. Building them is the most expensive part of an excitonic second-order run,
and the cache lets later runs skip it. With ``OME_ex = nonlinear`` the cache is used as in the table
below; with ``OME_ex = none`` (any second-order ``Response``) the elements must come from the cache, so
``read`` or ``readwrite`` is required and a miss stops the run.

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
* exciton energies, compared against the current Xatu files to :math:`10^{-10}` — a mismatch **stops** the run.
  An archive and the text files of the **same** Xatu run differ at that level (the archive keeps full
  precision), so a cache written from one does not serve the other;
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
``.states`` file (or the archive), since the cached matrix elements are exactly what the k-loop would have
built from them. That read is plain ASCII and can dominate start-up for a large exciton basis — on a
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
       group, so it is safe for any model. On a 2D hexagonal mesh the differences are taken along the
       three mesh directions related by the threefold rotation (the two reciprocal axes and their sum or
       difference), so that the derivative itself respects that symmetry; on any other mesh along the
       crystal axes.
   * - ``finite_difference`` (= ``plain``)
     - The original method: a plain difference of the envelopes between neighbouring k-points. It is
       correct only where the band phases vary smoothly, which holds for simple models like hBN but not
       for models with many orbitals and spin–orbit coupling.

On monolayer MoS\ :sub:`2` (34 orbitals, spin–orbit coupling) the phase convention jumps on about 12% of the links
between neighbouring k-points. The ``finite_difference`` method then breaks the crystal's threefold
symmetry by 20–65% in the excitonic shift, rectification and SHG spectra, against 2–5% with
``covariant``. On hBN the two agree, and ``covariant`` is the more accurate of the two (see
:doc:`changes`). Keep the default unless you are reproducing results from before 2026-10-04.

The three-direction stencil matters for excitons the mesh resolves poorly. Excited and near-gap excitons of
weakly screened materials can sit on a handful of k-points (MoSe\ :sub:`2`, 87x87: half the weight of some states
on 5-9 points, a quarter on K itself), and differences along the two crystal axes alone then make
:math:`X_{nm}` anisotropic: the excitonic SHG of MoSe\ :sub:`2` broke the threefold symmetry by 38.6%, against
1.7% with the three directions. A denser mesh does not cure this (120x120: 30.6%), because more of the near-gap
series appears and its states are narrower still. The log line ``X_nm: covariant envelope derivative on the
hexagonal star of mesh directions`` says that the three-direction stencil is in use.

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
the envelopes vary smoothly from the neighbouring k-points, fitted on the lowest excitons (at most half of the
exciton basis) and applied to all of them. The spectra then no longer depend on Xatu's choice, and the symmetry
residual of MoS\ :sub:`2` drops to the level reached when the degeneracy is lifted. The log reports how many
k-points were treated and on how many excitons the fit was made, and warns if it does not converge. The fit uses
the lowest excitons because, summed over a complete exciton basis, the overlap it is built from is exactly zero
between different k-points and determines nothing. Models without exact degeneracies,
such as hBN, are not affected.

The repair is only needed when OptiX does not know Xatu's choice, i.e. with Xatu text files and archives converted
from them. An archive written by ``xatu -H -c`` stores the band states themselves (:ref:`kw-band-phase`); OptiX then
uses exactly those, inside degenerate groups too, and skips the repair (the log says so). Applying it there would
rotate the envelopes away from the states they belong to: MoSe\ :sub:`2` with spin-orbit coupling, 87x87, lowest 3900
excitons, excitonic SHG threefold-symmetry residual 7.1% with the repair against 0.45% without.
