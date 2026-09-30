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
  exceptions are ``Broadening_type`` and ``Cache_ome_ex``.
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
   shift_shiftvector
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
     - ``absorbance``, ``shift_shiftvector``, ``shift_sumrule``, ``shift_gender`` or ``none``.
   * - :ref:`kw-energy`
     - always
     - Frequency window, broadening and number of points.
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

   The Wannier functions are assumed orthonormal. The Hamiltonian must include the home cell
   :math:`\mathbf{R}=(0,0,0)`; otherwise OptiX stops with an error.

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
excitonic response. It cannot exceed the number of states Xatu wrote. The spectrum is converged only
up to roughly the energy of the highest state included.

The cost of excitonic **second-order** runs grows steeply with this number, both in time and in memory
(the inter-exciton matrix elements have :math:`3N^2` entries for :math:`N` states). Used only when
``Xatu_interface`` is ``true``.

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
   vectors, generalised derivatives and k-derivatives of :math:`|v|`. Required for every ``shift_*``
   response. Written to the binary file ``ome_nonlinear_sp_<material>.omesp``.

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
   * - ``shift_*``
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
   * When ``OME_ex`` is ``linear`` or ``nonlinear``, compute ``OME_sp`` in the same run as well (not
     ``none``). The exciton envelopes have to be brought into the same band gauge as the
     single-particle states, and that needs the rotation built while computing ``OME_sp``. Otherwise
     OptiX warns ``fk_ex CANNOT be carried into the rotated basis``.

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

``shift_shiftvector``
   Shift conductivity :math:`\sigma^{abc}(0;\omega,-\omega)` from the shift-vector formula, with the
   amplitude-gradient correction. **This is the recommended shift-current method.** Output:
   :doc:`outputs/shift_conductivity`.

``shift_sumrule``
   Shift conductivity from the sum-rule form of the generalised derivative. It is only reliable when
   ``Bandlist`` includes many remote bands; for a two-band window it is :math:`\approx 0`. OptiX prints a warning when
   it is used. Mostly useful as a cross-check.

``shift_gender``
   Reserved for a numerical generalised-derivative method. **Not implemented yet**: the single-particle
   result is identically zero.

``none``
   Compute no response. Useful to only produce the matrix-element files (see :doc:`workflows`).

Any other value stops the program with a list of the valid options.

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
* exciton energies, compared against the current ``.eigval`` — a mismatch **stops** the run;
* number of stored excitons — if the cache has fewer than ``Exciton_cutoff``, it is recomputed. A cache
  with *more* excitons is fine, and the needed subset is used.

.. warning::

   The cache does **not** fingerprint the Wannier90 file. If you change the tight-binding model but
   keep the same file name and exciton spectrum, delete the cache by hand.

The file is large: about :math:`96\,N^2` bytes for :math:`N` = ``Exciton_cutoff`` (:math:`\approx` 340 MB for
:math:`N = 1875`, :math:`\approx` 3 GB for :math:`N = 5625`). The cache is not used when ``Write_ex_kresolved`` is
``true``.
