==============
Recent changes
==============

Changes that affect results, output files or how you drive OptiX. Ordered newest first. Where a change
alters numbers that earlier runs produced, the size of the difference is stated.

2026-10-08
==========

One ``.omesp`` for every branch; ``OME_ex = none`` reads the cache
------------------------------------------------------------------

* Every ``OME_sp = nonlinear`` run now stores the block-covariant data of **both** covariant methods (the
  shift current and SHG / electro-optic / rectification / ``general``), whatever its ``Response``. A
  ``shift`` run used to store only its own, so a later ``shg`` run with ``OME_sp = none`` stopped with "no
  covariant second-order data". Cost on a ``shift`` run (MoS\ :sub:`2` 60x60, 4 bands): wall time
  +4%, peak memory +37 MB, file 61 :math:`\to` 89.5 MB, the size an ``shg`` run's file already had.
* ``OME_ex = none`` on a second-order run reads the excitonic matrix elements from the :ref:`kw-cache`
  file (``Cache_ome_ex = read`` or ``readwrite``), as ``OME_sp = none`` reads the ``.omesp``; the exciton
  envelopes are then not read either. It used to ignore the cache, read every envelope and fail later; now a
  missing cache or a run without ``Cache_ome_ex`` stops at once with a message.

**No computed number changes**: hBN 30x30 SHG, rectification, electro-optic and a 2D ``general`` map from
the files equal direct runs to :math:`10^{-14}`; shift and SHG on MoS\ :sub:`2` equal the previous version
to :math:`3\times10^{-14}`. Checked by ``make check_ome_cache`` (7 new checks, all failing on the
previous version).

2026-10-07
==========

``Exciton_cutoff`` is optional
------------------------------

Without :ref:`kw-cutoff` an excitonic run now uses every exciton in the Xatu files (the count on the third
line of the ``.eigval`` file) and reports it in the log; a negative value stops with a message. It used to
leave the count unset, and the run crashed in the excitonic matrix elements. **No computed number changes**
for inputs that set ``Exciton_cutoff``. Checked by ``make check_bandlist_guard``.

Faster single-particle matrix elements and second-order kernel
--------------------------------------------------------------

Two hot spots rewritten; the physics is unchanged.

* **Bloch sums.** :math:`H(\mathbf k)`, :math:`S(\mathbf k)`, their k-derivatives and the position kernel are now
  matrix products over the lattice vectors, evaluated for a k-point and its finite-difference neighbours in one
  pass over the hoppings, and reused by the routines that need them (the centre was rebuilt four times and each
  neighbour twice per k-point). These sums took 91% of a single-particle second-order run on MoS\ :sub:`2`.
* **Covariant second-order kernel** (``Sp_method = covariant``: ``shg``, ``electrooptic``, ``rectification``,
  ``general``): frequencies are processed in chunks of 64 with the frequency as the innermost, vectorised index.
  Identical results (:math:`4\times10^{-14}`), and the work arrays no longer grow with the number of frequencies.

Measured, 32 threads: MoS\ :sub:`2` 60x60 SHG 9.9 s :math:`\to` 2.5 s (one thread 112 s :math:`\to` 25 s),
covariant shift 30x30 3.6 :math:`\to` 1.2 s, buckled hBN rectification (2000 frequencies) 1.8 :math:`\to` 0.6 s,
GeS 17-band SHG 3.0 :math:`\to` 1.5 s, SnTe (non-orthonormal) shift 28 :math:`\to` 17 s.
**Numbers change only at round-off level**, amplified by the :math:`10^{-6}` finite-difference step: relative
:math:`10^{-11}` to :math:`10^{-10}` on hBN, up to :math:`5\times10^{-9}` on MoS\ :sub:`2`, GeS and SnTe
(near-degenerate bands); excitonic outputs :math:`5\times10^{-15}`; band structures :math:`10^{-14}`. The
diagnostic ``shift_vector.dat`` of the per-band shift-vector formula moves by up to :math:`2\times10^{-3}` on
MoS\ :sub:`2` and SnTe, where its 50 bohr clip flips on round-off (on hBN :math:`2\times10^{-11}`).

Band structure along a chosen k-path; ``Response = bands``
----------------------------------------------------------

``bands_<material>.dat`` now follows the new :ref:`kw-kpath` block (vertices in reduced coordinates, each with the
number of points to the next; :ref:`kw-kpath-labels` names them). Without it the default path depends on the
lattice: :math:`\Gamma`-M-K-:math:`\Gamma` for hexagonal 2D lattices (K is found as the zone corner), :math:`\Gamma`-X-S-Y-:math:`\Gamma`
otherwise, plus Z in 3D. **The default path changes**: it was :math:`\tfrac12\mathbf G_1\to\Gamma\to\tfrac12\mathbf G_2`,
which missed K on hexagonal lattices. The file gains a header (vertex labels and positions, the ``Bandlist``
window, VBM, CBM and gaps along the path); the data columns are unchanged and ``kz`` is now set (it was
undefined). ``Response = bands`` writes the band structure and stops. New ``tools/plot_bands.py`` and test
``make check_bands``.

Warning for an unusual band window
----------------------------------

OptiX now prints the resolved band window (offset from Nfermi and band number) and warns when ``Bandlist`` (or
the band list of a Xatu ``.states`` file) omits the top valence or bottom conduction band, leaves a gap, or
repeats an entry. ``Bandlist`` is a list, not a range: ``-1 2`` is two bands. **No computed number changes.**
New test ``make check_bandlist_guard``.

Sign of the injection current, and of every b-c antisymmetric two-frequency part
---------------------------------------------------------------------------------

Term 3 of Eq. (A9b) of Taghizadeh & Pedersen (the exciton populations and coherences) pairs :math:`U_n` with the
field at :math:`\omega_q` and :math:`U^*_m` with the field at :math:`\omega_p`. The excitonic methods A and B and the
single-particle covariant method had the two field indices the other way round. Only the part antisymmetric
under :math:`b\leftrightarrow c` depends on this, so shift currents, SHG and every symmetric (linear-polarisation)
component are **unchanged** (bit-identical). What changes:

* the **injection current** (antisymmetric Im of ``rectification``, single-particle covariant and excitonic): it had
  the wrong sign. Against a real-time propagation with circular light (non-interacting buckled hBN, 8 eV,
  :math:`\eta=0.3` eV): real time 1.763; before -1.686 (single-particle) and -1.455 (excitonic); now 1.756 and 1.761.
  ``Sp_method = per_band`` (Eq. A3a) already had the right sign and is unchanged.
* the :math:`b\leftrightarrow c` antisymmetric part of ``general`` and ``electrooptic`` outputs (single-particle
  covariant and excitonic), which is physical when :math:`\omega_1\neq\omega_2`.

New test ``make check_out_of_plane``.

Single-particle shift current along z
-------------------------------------

The single-particle shift current (``Response = shift``, covariant) was **zero for every current along a
non-periodic direction** (z of a 2D model: :math:`\sigma^{zxx}`, :math:`\sigma^{zzz}`, ...): the generalised derivative
along z, which has no :math:`k_z` part but keeps the connection term (:ref:`out-of-plane-convention`), was dropped.
It is now included: on non-interacting buckled hBN :math:`\sigma^{zxx}` and :math:`\sigma^{zzz}` equal the excitonic
shift-current route to :math:`2\times10^{-3}` and :math:`5\times10^{-3}` of their maxima. In-plane components and
models without out-of-plane response (flat hBN, MoS\ :sub:`2`: the forbidden odd-z components stay at
:math:`1.5\times10^{-4}` of the in-plane maximum) are unchanged.

Excitonic rectification is the whole causal response; the shift current is ``Response = shift``
--------------------------------------------------------------------------------------------------

``Response = rectification`` (and ``general`` at ``Frequency_ratio = -1``) now evaluates the whole
:math:`\sigma^{abc}(0;\omega,-\omega)` with the causal broadening of every other branch, method A of
Taghizadeh & Pedersen (2018) with the bare exciton-exciton current in its term 3, both field orderings
explicit (:ref:`dc-excitonic-rectification`). It is continuous with the 2D map: a map containing
:math:`\omega_1+\omega_2=0` points uses the same evaluation, so its anti-diagonal equals the rectification.
The shift current in the convention of the reference paper stays ``Response = shift``, unchanged.

**What changes in** ``second_ex_rectification_lengthgauge_<material>.dat``:

* **Im columns**, zero until now, hold the antisymmetric response to circular light, which contains the
  excitonic **injection current** (:ref:`dc-excitonic-injection`). Non-interacting limit: integrated weight
  0.99 of the single-particle injection current; real excitons: mesh-converged at 75x75.
* **Re columns** were the shift current; they are now the causal response. In the non-interacting limit
  they equal the single-particle rectification (:math:`5\times10^{-4}`), including the off-resonant part the
  old branch left out. With bound excitons they differ from the shift current: on buckled hBN the
  least-squares ratio is 0.53 (mesh-converged), the first bright exciton is halved and a strong peak appears
  at the next bright doublet (:ref:`dc-term3`). Above the gap the two agree.
* 2D maps that contain :math:`\omega_1+\omega_2=0` points change in their difference-frequency half, where
  the exciton-exciton term carries most of the response (term 3 now on the bare current).
* ``Ex_rectification`` is obsolete: ``causal`` is ignored with a note, ``shift`` stops and points to
  ``Response = shift``.
* The excitonic rectification step costs about twice as much (two method-A passes instead of one); the
  exciton matrix-element stage is unchanged.

New test ``make check_ex_rectification``; ``make check_sp_shift`` and ``make run_test_second_symmetry``
updated.

2026-10-06
==========

Excitonic runs can reuse the single-particle matrix elements (``OME_sp = none``)
--------------------------------------------------------------------------------

The ``.omesp`` files now store the Eq. (A4) basis of the exciton window, and the nonlinear one also the
exciton-window states the covariant :math:`X_{NN'}` needs (:doc:`outputs/matrix_elements`). An excitonic
run (``OME_ex = linear`` or ``nonlinear``) may therefore use ``OME_sp = none``; until now it had to recompute
the single-particle matrix elements, because those quantities were rebuilt only while ``OME_sp`` was being
computed. Measured on In\ :sub:`2`\ Se\ :sub:`3` (200 excitons): identical to the full calculation to
:math:`4\times10^{-16}`, SHG in 2 s instead of 14 s. **No computed number changes.** An ``.omesp`` written
before this date lacks the basis; with it the excitonic run still stops and asks you to regenerate the file
once. The nonlinear file's tail now starts with a tag and a flags word; older files remain readable.

Warning for a metallic filling
------------------------------

OptiX now warns when ``Nfermi`` does not put the Fermi level in a gap on the k-mesh (band ``Nfermi``
reaching above band ``Nfermi + 1`` anywhere, or the two touching), with both energies. Occupations follow
the band index, so such a filling describes a metal, and second-order responses then contain poles at
vanishing transition energy: on GeS, ``Nfermi = 21`` turns :math:`\sigma^{xyy} = 135` into 10566. **No
computed number changes.**

New: ``Ex_rectification = causal`` (opt-in)
-------------------------------------------

The excitonic rectification can now be evaluated with the causal prescription of the single-particle path
(:ref:`kw-ex-rect`), which includes the off-resonant part. It is opt-in because its resonant part converges
slowly with the k-mesh (non-interacting hBN, :math:`\eta = 0.15` eV: 98% / 59% / 35% off at 30x30 / 45x45 /
60x60); OptiX warns when it is used. **The default, ``shift``, is unchanged.**

Input errors now fail with exit code 1
--------------------------------------

Three input errors printed a message but ended the run with exit code 0, so scripts and job schedulers saw a
success: an ``Orthonormal`` or ``Xatu_interface`` value other than ``true`` or ``false``, and a keyword whose
value line is missing at the end of the input file (``Error reading file``). They now exit with code 1, like
every other input error. **No computed number changes.**

Tight-binding reader: Hermiticity check and repair
--------------------------------------------------

The reader now checks that :math:`H(\mathbf R)`, the overlap :math:`S(\mathbf R)` and the position matrices
are Hermitian (:ref:`kw-wannier`), logs the result, and repairs what is not: it completes blocks stored as their
lower triangle only, and replaces a non-Hermitian block by its Hermitian part with a ``WARNING`` that gives the
size of the defect. Exactly Hermitian files are read unchanged, so hBN and the other model files used in the tests
give the same numbers as before.

Why: OptiX builds the Bloch matrices from the lower triangle of each block. A non-Hermitian file was therefore
replaced, silently, by a completion that depends on the order of the orbitals, which breaks the crystal symmetries.
Several of the models in use have non-Hermitian **position matrices**: MoS\ :sub:`2` by up to :math:`6.2\times10^{-3}` Angstrom,
ReS\ :sub:`2` :math:`2.5\times10^{-2}` Angstrom, MoSe\ :sub:`2` :math:`8.9\times10^{-2}` Angstrom, In\ :sub:`2`\ Se\ :sub:`3` 0.12 Angstrom (SnTe :math:`2\times10^{-4}` Angstrom); their Hamiltonians are Hermitian.

How much the numbers move (single particle, ``Sp_method = covariant``):

* **Monolayer MoS**\ :sub:`2` (30x30): shift and SHG by 0.4% and 0.8% of their maxima; their threefold-symmetry residuals
  fall from 0.73% to 0.40% (shift) and from 1.24% to 0.85% (SHG). The symmetry-forbidden injection current in the
  rectification output, which reached 12% of the tensor at :math:`\eta = 0.05` eV, falls by a factor 3.3. What
  remains comes from the model itself, whose Hamiltonian breaks the threefold symmetry slightly. OptiX reproduces
  it to within a few per cent of an independent calculation.
* **In**\ :sub:`2`\ **Se**\ :sub:`3`: shift by 1.7%, SHG by 0.4% of the maximum. **ReS**\ :sub:`2`: by 0.2%.
* **SnTe**: its :math:`H` and :math:`S` are stored as lower triangles, which the old code completed the same way,
  and its position-matrix defect is negligible.

Excitonic results use the same single-particle matrix elements and change by comparable amounts; they were not
re-measured. ``make check_tb_hermiticity`` covers the new behaviour.

Second-order outputs: one normalisation, the physical sign, covariant by default
--------------------------------------------------------------------------------

**Every second-order output except the two shift-current files and the excitonic rectification changes.**
Three things were done together, and all of them were checked against a direct real-time simulation of the
current (``make check_realtime_sign``, below):

#. **One normalisation.** All outputs now follow Taghizadeh & Pedersen 2018 and the npj paper,
   :math:`J^{(2)}(t)=\tfrac14\sum\sigma E E\,e^{-i(\omega_p+\omega_q)t}` with
   :math:`E(t)=\tfrac12\sum E(\omega_p)e^{-i\omega_p t}` (:ref:`second-order-normalisation`). The
   single-particle SHG, electro-optic, rectification and ``general`` outputs used the 2017 convention
   without the :math:`\tfrac14`, so the same current gave a :math:`\sigma` four times smaller. The warning "Two
   normalisations" of 2026-10-05 (below) is resolved.
#. **The physical sign.** The kernels of Taghizadeh *et al.* already contain the electron charge, and the
   :math:`e^3 = -1` applied in the unit conversion since 2026-10-04 counted it a second time for them. The
   SHG, electro-optic, ``general`` and single-particle rectification outputs therefore had the wrong sign.
   The shift current (npj Eq. 9, written with :math:`e = 1`) and the excitonic rectification were right and
   are unchanged.
#. **Covariant by default.** A new keyword, :ref:`kw-sp-method` (default ``covariant``), selects the
   single-particle method for every second-order response. ``covariant`` uses the block-covariant
   generalised derivative (:ref:`shg-covariant`) for ``shg``, ``electrooptic``, ``rectification`` and
   ``general``. ``per_band`` restores the earlier per-band routes. A new value, ``Response = shift``,
   runs the recommended shift current: ``shift_covariant`` by default, or ``shift_shiftvector`` with
   ``Sp_method = per_band``. The explicit names still work as before.

How old files relate to new ones:

.. list-table::
   :header-rows: 1
   :widths: 46 18 36

   * - Output
     - new / old
     - Note
   * - single-particle ``shg_sp_*``, ``second_{electrooptic,rectification,general}_*``
     - :math:`-4`
     - plus the change of method where bands are degenerate (below)
   * - excitonic ``shg_ex_*``, ``second_ex_{electrooptic,general}_*``
     - :math:`-1`
     -
   * - excitonic ``second_ex_rectification_*`` (and ``general`` at ``Frequency_ratio = -1``)
     - 1
     - unchanged
   * - ``shift_sp_*``, ``shift_ex_*``
     - 1
     - unchanged

**Real-time check.** On two-band hBN the position operator is just the Wannier centres, so minimal
coupling :math:`\mathbf k\to\mathbf k+\mathbf A(t)` is exact. Propagating the density matrix under a field
:math:`E_0\cos(\omega t+\phi)e^{\eta t}` and separating the second-order current by its phase dependence
gives :math:`\sigma` with no convention left open. At :math:`\eta = 0.15` eV and 4–9 eV, OptiX now agrees
with it in sign and magnitude: SHG to :math:`\sim10^{-4}`, single-particle rectification to 0.2%,
``general`` at (6 eV, 3 eV) to :math:`10^{-4}`. Before this change SHG and rectification had the opposite
sign and were 4 times too small.

**What the default change does on MoS**\ :sub:`2` (monolayer, npj model, 30x30 and 60x60, full-tensor
threefold-symmetry residual):

* SHG and ``general``: 1.1–1.4% (``per_band``: 85–87%).
* Rectification, shift-current part (:math:`b\leftrightarrow c` symmetric, real): 3.6%, the same on both
  grids (``per_band``: 89–92%). The imaginary antisymmetric part, the injection channel, is forbidden
  for :math:`D_{3h}` but is about 12% of the tensor at :math:`\eta = 0.05` eV. It scales as
  :math:`1/\eta`, so it is a small injection current carried by the model's own symmetry breaking (its
  :math:`H(\mathbf R)` breaks :math:`C_3` by 0.13 meV) rather than discretisation error. This is the
  most likely explanation but it is not proven.
* Electro-optic: 20% at 30x30, 14% at 60x60 (``per_band``: 84–92%). Grid hungry as on the excitonic
  path; check convergence before trusting it.

On hBN, ``covariant`` and ``per_band`` agree to :math:`10^{-10}` (SHG) and :math:`4\times10^{-5}`
(rectification). The covariant path also carries the injection current: on buckled hBN its
antisymmetric imaginary part equals the ``per_band`` one and scales as :math:`1/\eta`.

**Single-particle rectification is no longer just the shift current.** It now uses the causal
prescription :math:`\omega_q = -\omega + i\eta`, which is what the real-time current follows, and it
includes the off-resonant terms. On resonance it equals the shift current (hBN peak ratio 0.995, same
sign). Below the gap the two differ by an amount proportional to :math:`\eta`, which halves with every
halving of :math:`\eta`. The excitonic rectification keeps its DC convention (:ref:`dc-limit`) and gives
the resonant, shift-current part only.

Cost: ``Sp_method = covariant`` needs the same extra diagonalisations as ``shift_covariant`` in the
matrix-element stage and a larger ``.omesp`` file. That holds for excitonic runs too, which use the
single-particle matrix elements. An ``.omesp`` written by an earlier version, or with ``Sp_method = per_band``, lacks
the covariant data: a run with ``OME_sp = none`` then stops and asks you to regenerate it.

Test plot of the excitonic SHG follows the fundamental frequency axis
-----------------------------------------------------------------------

``make run_test_shg_real`` ended with ``Error 1 (ignored)`` and wrote no plot: since the SHG axis became
the fundamental photon energy :math:`\hbar\omega` (2026-09-24, below), the test's spectra file names its
first column ``Ew_eV``, while ``tools/plot_test_outputs.py`` still looked for ``E2w_eV``. The script now
reads ``Ew_eV`` and labels the axis as the fundamental. Spectra files from before that date (column
``E2w_eV``, :math:`2\hbar\omega`) are still accepted and halved onto the same axis. **No computed number
changes**; the test itself always passed.

2026-10-05
==========

New: non-orthonormal models (``Orthonormal = false``)
-----------------------------------------------------

Models whose basis functions overlap, such as tight-binding models built from atomic orbitals, can now be
used: set :ref:`kw-orthonormal` to ``false`` and add an overlap section to the model file. OptiX then
solves the generalised eigenproblem and carries the overlap through every matrix element. **Nothing changes
for orthonormal models** (the default): their results are the same to :math:`6\times10^{-16}`. Validated
against hBN rewritten in a non-orthogonal basis: the results equal those of the orthonormal model to
:math:`10^{-10}` (on-site overlap) and :math:`2\times10^{-9}` (k-dependent overlap).

Faster single-particle matrix elements for large models
-------------------------------------------------------

The Berry-connection step of ``OME_sp = nonlinear``, which scaled as the fourth power of the number of
orbitals and dominated the run for large models, now uses matrix products: 10.5x faster for SnTe
(144 orbitals), where a 201x201 shift-current run now takes 15–20 min on 32 threads instead of 2.5–3.3 h.
Results change only at round-off (:math:`10^{-14}`).

New: ``Response = shg_covariant``
---------------------------------

Single-particle SHG without degeneracy cut-offs (:ref:`shg-covariant`). **Nothing changes unless you
select it.** It writes the same file, in the same convention, as ``Response = shg``. On hBN the two agree
to :math:`10^{-10}`. On monolayer MoS\ :sub:`2`, ``shg`` breaks the threefold symmetry by 82–87%, with a
symmetry-forbidden :math:`\sigma^{yyy}` up to 170 times :math:`\sigma^{xxx}`; ``shg_covariant`` holds it to
0.6% and is converged to 4% on a 60x60 grid.

.. warning::

   **Two normalisations for second-order conductivities.** The single-particle SHG, rectification,
   electro-optic and ``general`` outputs follow Taghizadeh *et al.* 2017, where
   :math:`J^{(2)}(t)=\sum\sigma E E e^{-i(\omega_p+\omega_q)t}`. All excitonic outputs and both shift-current
   outputs follow Taghizadeh & Pedersen 2018 (and the npj paper), where
   :math:`J^{(2)}(t)=\tfrac14\sum\sigma E E e^{-i(\omega_p+\omega_q)t}`. Both use
   :math:`E(t)=\tfrac12\sum E(\omega_p)e^{-i\omega_p t}`. For the same physical current the second
   convention gives a :math:`\sigma` **four times larger**: an excitonic SHG is 4x the single-particle one in the
   independent-particle limit (measured 3.98–4.00). This is a convention difference, not a physics one,
   and it will be unified.

   **Resolved 2026-10-06** (above): every output now uses the second convention.

New: ``Response = shift_covariant``
-----------------------------------

A new way to compute the single-particle shift current (:ref:`kw-response`, :ref:`shift-covariant`). It
evaluates Eq. (9) of the reference paper with a generalised derivative that stays well defined where
bands are degenerate, so it needs none of the cut-offs of ``shift_shiftvector``. **Nothing changes unless
you select it**; ``shift_shiftvector`` remains the default recommendation for now.

What it gives:

* **hBN**: identical to the exact independent-particle result to :math:`10^{-7}`, including
  :math:`\sigma^{yxy}`, which ``shift_shiftvector`` underestimates by 2%.
* **Monolayer MoS**\ :sub:`2` (90x90): threefold-symmetry residual 0.6% (``shift_shiftvector``: 9.2%).
  :math:`\sigma^{xxx}` and :math:`\sigma^{xyy}` agree with ``shift_shiftvector`` to about 1%, while
  :math:`\sigma^{yxy}` is about 16% larger.
* With an out-of-plane field that lifts the degeneracies, it reproduces the exact per-band result to 1%.

Cost: seven extra diagonalisations per k-point in the matrix-element stage, and a larger ``.omesp``
file. A run with ``OME_sp = none`` must read an ``.omesp`` written by a ``shift_covariant`` run.

Single-particle shift current: shift vector evaluated in a parallel-transported gauge
-------------------------------------------------------------------------------------

``shift_sp_*`` changes for multi-orbital models. The shift vector combines the k-derivative of a
phase with a Berry connection; the two are individually gauge dependent and only their sum is not.
The Berry connection was taken in the raw eigenvector gauge and **discarded when it exceeded
50 bohr**, which that gauge can do anywhere, while the matching part of the phase derivative was
kept. Where that happened the shift vector was meaningless, and the error was not symmetric under the
crystal's mirror planes. Both pieces are now taken in a parallel-transported gauge, in which nothing
gauge dependent can reach the cut-off.

How much the numbers move:

* **hBN**: by :math:`3\times10^{-12}` — unchanged.
* **Monolayer MoS**\ :sub:`2` (4-band window): by at most 2.5% of the peak on a 102x102 grid; the comparison
  with the reference paper [npj Comput. Mater. 11, 13] is unaffected. With the full 34-band window,
  by up to 14%. Mirror-forbidden components shrink 2–4x.
* **SnTe** (non-orthonormal model): components forbidden by the mirror :math:`y\to-y` were up to 8% of
  the largest; they now vanish (forbidden fraction 2.9% to 0.01%). :math:`\sigma^{xxx}` moves by up to
  29% of its peak.

Single-particle shift current: off-diagonal components no longer truncated
--------------------------------------------------------------------------

The amplitude-gradient term, which only enters components with :math:`b\neq c` (e.g.
:math:`\sigma^{yxy}`), was dropped wherever its logarithmic derivative :math:`\partial\ln|r|` exceeded
50 bohr. That quantity diverges wherever a matrix element passes through zero, while the combination
that actually enters the current stays finite, so the cut discarded real contributions. It is gone;
the cut on nearly degenerate bands (2.7 meV) stays. On monolayer MoS\ :sub:`2` :math:`\sigma^{yxy}` changes by
up to 8% (102x102) and 12% (90x90) of its peak and the threefold-symmetry residual improves (11.9% to
9.2% at 90x90; 8.2% to 3.2% when the band degeneracies are lifted). hBN is unchanged; :math:`b = c`
components are unchanged everywhere.

.. note::

   **Comparing with published spectra:** the default ``Broadening_type`` is Lorentzian since
   2026-09-16; earlier OptiX versions, and figures made with them (e.g. npj Comput. Mater. 11, 13), used a
   Gaussian of the same width. At equal :math:`\eta` the Gaussian peaks are about 20–30% higher: the
   MoS\ :sub:`2` single-particle spectrum matches that paper's Fig. 3 to 1–5% with ``gaussian`` but only to
   0.78–0.89 with the default.

.. warning::

   ``Nfermi`` must put the Fermi level in a gap **at every k-point**. OptiX assigns occupations by band
   index, so if band ``Nfermi`` and band ``Nfermi + 1`` overlap in energy anywhere in the zone (a metal
   or semimetal at that filling), transitions with :math:`\varepsilon_{nm}\to0` enter the shift current
   with a :math:`1/\varepsilon_{nm}^2` weight. Previously the corrupted shift vector at such crossings
   was often discarded, which hid the problem; now it shows up as a large spurious signal growing
   towards low frequency. Check the band file before choosing ``Nfermi``.

2026-10-04
==========

Excitonic second-order responses: inter-exciton position elements made gauge invariant
--------------------------------------------------------------------------------------

**Every excitonic second-order output changes** (``shift_ex_*``, ``shg_ex_*``, ``second_ex_*``). The
inter-exciton position elements :math:`X_{nm}` contain a k-derivative of the exciton envelopes, which was
taken as a plain difference between neighbouring k-points. That is only correct if the phases of the
band states vary smoothly across the k-mesh, and for models with many orbitals and spin–orbit coupling
they do not. The derivative is now taken **covariantly** (:ref:`kw-xnm`): the neighbouring envelope is
carried into the local band basis before differencing. The result no longer depends on band phases at
all, and a fourth-order stencil makes it more accurate than the old method even where that one was valid.

How much the numbers move:

* **hBN**, 30x30: by about 2.4% (excitonic shift) and 2.1% (SHG) of the peak, i.e. discretisation error.
  The symmetry residuals improve: D3h 4.4% to 2.7%, electro-optic 15% to 6%.
* **Monolayer MoS**\ :sub:`2`: by O(1). The old spectra broke the threefold symmetry by 19% (shift), 64%
  (rectification) and 62% (SHG); now 2.3%, 3.3% and 5.3%. **Discard excitonic second-order results for
  multi-band spin–orbit models computed before this date.**

A small residual remains where bands are exactly degenerate (for MoS\ :sub:`2` along the :math:`\Gamma`–M lines), because the
basis Xatu uses inside a degenerate group is not known to OptiX. The old method is still available as
``Xnm_derivative = finite_difference``. The cache format moved to version 3; older cache files are
recomputed.

Excitonic second-order responses: envelope basis repaired at degenerate k-points
---------------------------------------------------------------------------------

At k-points where two bands are exactly degenerate, the basis Xatu uses for the exciton envelopes is
arbitrary and was taken at face value. OptiX now reconstructs it (:ref:`kw-basis-repair`). Excitonic
second-order spectra of models with such degeneracies change — for MoS\ :sub:`2` by up to ~9% of the peak — and the
threefold-symmetry residual drops from 2–5% to under 1% (with exchange off in Xatu). Models without exact
degeneracies, such as hBN, are unchanged.

.. warning::

   With ``Exchange = true`` in Xatu, the MoS\ :sub:`2` exciton spectrum itself breaks the threefold symmetry: the
   bright exciton pairs come out split by a few meV (3.2 meV on a 45x45 grid, 1.1 meV on 90x90). The
   excitonic second-order spectra inherit a residual of about 14%, which OptiX cannot remove.

Single-particle shift current: branch-cut error fixed
-----------------------------------------------------

``shift_sp_*`` changes for models whose velocity matrix elements are real at many k-points, such as
hBN. A phase derivative was computed as the difference of two principal-value phases, which jumps by
:math:`2\pi` when an element crosses the negative real axis; those k-points were then dropped. On hBN
30x30, :math:`\sigma^{xyy}` rises by 6.9% and now matches an independent exact calculation to
:math:`3\times10^{-4}`; the other components are unchanged. MoS\ :sub:`2` is unaffected.

Sign of every second-order output: electron charge :math:`e = -|e|`
-------------------------------------------------------------------

**Every second-order output file changes sign**: ``shift_sp/ex_lengthgauge_*.dat``,
``shg_sp/ex_lengthgauge_*.dat`` and every ``second_*`` / ``second_ex_*`` file (rectification,
electro-optic, general). Magnitudes are unchanged (old + new = 0 to :math:`10^{-15}`). First-order
outputs are not affected.

All second-order conductivities are proportional to :math:`e^3`. OptiX now uses the electron charge
:math:`e = -|e|`, applied once in the atomic-unit to :math:`\mu\mathrm{A\,nm/V}^2` conversion factor.
With this convention OptiX reproduces the published MoS\ :sub:`2` shift-current spectrum of its reference paper
[npj Comput. Mater. 11, 13 (2025), Fig. 3a and Supplementary Fig. 2b] in sign, peak positions and line
shape. The previous release used :math:`e = +1`, which gave the opposite sign. To compare against
results from before this date, multiply them by -1.

.. note::

   **Partly reverted 2026-10-06** (above). A real-time simulation showed that the kernels behind SHG,
   electro-optic, ``general`` and the single-particle rectification already contain the electron charge,
   so for those outputs this change introduced a wrong sign. The 2026-10-06 change removes it. The
   shift currents and the excitonic rectification keep the sign given here.

.. warning::

   On monolayer MoS\ :sub:`2` with spin–orbit coupling, the SHG and rectification outputs (single-particle and
   excitonic) do not yet satisfy the :math:`D_{3h}` symmetry of the crystal. Do not use them for that
   material until this is resolved. The single-particle shift current is unaffected apart from its known
   weaker accuracy on :math:`b \neq c` components.

   *Update 2026-10-06:* with the default ``Sp_method = covariant`` the single-particle SHG and ``general``
   now hold :math:`C_3` to about 1%, and the shift-current part of the rectification to 3.6%. The
   electro-optic response is still grid hungry. See the 2026-10-06 entry.

2026-09-30
==========

Exciton matrix-element cache: format version 2
----------------------------------------------

The ``.omeex2`` header now records the **band list**, not just the band counts. Counts alone cannot
distinguish a band set of ``[60, 61]`` from ``[61, 60]``, and that ambiguity once let a whole set of
results be computed with two conduction bands swapped — the counts matched, so nothing caught it.

* A cache whose band list differs from the current one, **in membership or in order**, now stops the
  run and prints both lists.
* A version 1 file (anything written before this date) is treated as a **clean miss**: OptiX says so
  and recomputes. It is not upgraded in place, because the order it was written with cannot be
  recovered from the file. Delete it.

Regenerating is much cheaper than it used to be — see the matrix-element speed-up below. See
:ref:`kw-cache` and :doc:`troubleshooting`.

Unit-conversion factor for the excitonic shift conductivity
-----------------------------------------------------------

``shift_ex_lengthgauge_*.dat`` changes by :math:`1.7\times10^{-8}` relative. The atomic-unit to
:math:`\mu\mathrm{A\,nm/V}^2` factor was written out by hand at six places in the source and one copy
had lost a ``d0``, making it single precision. It is now a single named constant. No other output file
is affected, and no conclusion changes at this size. See :doc:`outputs/shift_conductivity`.

Clarification: :math:`\mathrm{Im}\,\sigma` on the DC branch
------------------------------------------------------------

Not a code change — a correction to what the documentation claimed. :math:`\mathrm{Im}\,\sigma = 0` for
:math:`\sigma(0;\omega,-\omega)` holds only where the **injection current is forbidden by symmetry**.
On a lower-symmetry material a nonzero imaginary part on the single-particle branch is physics. See the
warning in :doc:`theory/dc_limit`.

Clarification: the DC branch reports the shift current only
------------------------------------------------------------

Not a code change. The DC tensor contains both the shift and the injection current; the
:math:`b\leftrightarrow c` symmetrisation OptiX applies selects the shift and discards the injection.
An earlier version of this documentation said the discarded part was a convention artifact — that was
wrong, and it came from examining the tensor *after* the symmetrisation had already removed the
antisymmetric content. See :ref:`dc-imaginary-part`.

Clarification: the anti-diagonal of a 2D map
---------------------------------------------

The anti-diagonal of a two-frequency map is close to the *negative* of the shift current **in
aggregate** (correlation :math:`-0.92` over the whole tensor), but this is **not a per-component
identity**: component by component the anti-correlation runs from :math:`-0.99` on the largest
components down to :math:`-0.10` on the smallest. Do not use it as a correction factor. The table in
:doc:`theory/dc_limit` has been recomputed.

Earlier
=======

Exciton k-loop batched into one matrix multiply per term
---------------------------------------------------------

The dominant cost of any excitonic second-order run. Each term is now a single large matrix
multiplication instead of one rank-deficient update per k-point. Measured on a 60x60 two-band model at
800 excitons: **105.5 s and 3.05 GB to 1.14 s and 0.43 GB**, and it scales with threads again.

The memory law no longer contains the thread count, so there is no longer any reason to run the
matrix-element stage on few cores. Complete exciton bases are now routine: the entire 8100-state BSE
space of a 90x90 two-band model costs 76 s and 12.9 GB. See :doc:`limitations` and :doc:`workflows`.

``OME_sp = none`` is refused for excitonic runs without a cache
----------------------------------------------------------------

The Eq. (A4) rotation matrices are rebuilt only while ``OME_sp`` is computed and are not stored in the
``.omesp`` file, so with ``OME_sp = none`` the exciton envelopes stay in Xatu's basis while the
single-particle quantities are rotated. The error is :math:`O(1)`. This used to print a warning and
finish; it now stops. ``OME_sp = none`` together with ``Cache_ome_ex = read`` remains valid, because a
cache hit never reads the envelopes. See :ref:`kw-omesp`.

A cache hit also skips reading the exciton envelopes
------------------------------------------------------

The envelopes are exactly what the k-loop would have consumed, so they are now read lazily and only if
the cache misses. That read is plain ASCII and can dominate start-up: 1.9 GB and 16.8 s on a
2700-exciton run, against 0.9 s to read the binary cache.

SHG output frequency axis
--------------------------

Column 1 of ``shg_*_lengthgauge_*.dat`` is :math:`\hbar\omega`, the **fundamental** photon energy. It
used to be :math:`2\hbar\omega`. Files written before 2026-09-24 are off by a factor of two if read
with the current convention; the file's own header line now states it. See :doc:`theory/conventions`.

Rectification and ``general`` at ``Frequency_ratio = -1``
-----------------------------------------------------------

These now use the DC convention :math:`\omega_q = -\omega_p`, :math:`\omega_2 = 0` exactly. Under the
previous convention the branch failed the non-interacting limit and produced a spurious peak. The
excitonic result now matches the independent shift-current implementation to :math:`3.4\times10^{-9}`.
A two-dimensional map is deliberately **not** changed, which is why its anti-diagonal is not a shift
current. See :doc:`theory/dc_limit`.

k-mesh built by OptiX itself
-----------------------------

With ``Xatu_interface = false``, the mesh is now the same Monkhorst-Pack, :math:`\Gamma`-centred grid
Xatu builds. It used to include both zone edges at full weight, which is not a periodic mesh: the shift
conductivity of a two-band model was 12.3% / 6.2% / 4.2% high at 30x30 / 60x60 / 90x90, and is now
1.25% / 0.17% / 0.16%. Results obtained on an OptiX-generated mesh before 2026-09-22 change.
Xatu-interface runs were never affected.
