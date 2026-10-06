==========
Validation
==========

Test suite
==========

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - command
     - what it checks
   * - ``make check_sp_shift``
     - single-particle shift current on synthetic non-interacting hBN, against (a) an exact independent NumPy evaluation and (b) the excitonic code's IPA limit, per component, plus C3
   * - ``make check_sp_shg``
     - single-particle SHG on GeS's 27-band model: band-window convergence, finiteness, :math:`b\leftrightarrow c` permutation symmetry
   * - ``make run_test_shg_real``
     - excitonic SHG on real hBN data: X_nm Hermiticity, scalar vs matrix kernel, method A (:math:`\Pi` from X) vs method B
   * - ``make run_test_shift_real``
     - excitonic shift current vs the paper's Eq. 11, evaluated independently in the test
   * - ``make run_test_shg_consistency``
     - 19 checks on synthetic physical data
   * - ``make test``, ``make test_matrix``
     - shift-kernel scalar vs matrix equivalence (1458 comparisons at 1e-10)
   * - ``make run_test_second_symmetry``
     - the general two-frequency branch at :math:`\omega_2/\omega_1 \neq 1`: method A vs B, D3h, the :math:`r\leftrightarrow 1/r` identity, and the DC branch's convention
   * - ``make check_ome_cache``
     - the five ``Cache_ome_ex`` modes: what each run does *and* what it reports doing
   * - ``make check_a4_basis_guard``
     - that ``OME_sp = none`` is refused for excitonic runs, and that the ``Cache_ome_ex = read`` exemption is allowed and exact
   * - ``make check_gauge_covariance``
     - that eigenvector phases, and rotations inside degenerate blocks, do not move X_nm or any shift/SHG output
   * - ``make check_shift_covariant``
     - the covariant single-particle methods (23 checks): shift vs exact Eq. 9 on hBN; SHG and rectification vs ``Sp_method = per_band`` on hBN; C3 on MoS\ :sub:`2`; invariance under rotations inside degenerate blocks
   * - ``make check_tb_hermiticity``
     - the tight-binding reader's Hermiticity check and repair: exact files untouched, lower-triangle storage completed, non-Hermitian H / r (and, where supported, non-orthonormal S and r with the R S term) warned about and equal to a hand-Hermitised twin
   * - ``make check_realtime_sign``
     - **absolute sign and normalisation**: SHG, rectification and the shift current on hBN against a real-time propagation of the density matrix (:ref:`second-order-normalisation`)

All must print ``ALL CHECKS PASSED`` / ``ALL TESTS PASSED``.

Symmetry checks on hBN
======================

hBN's two-band Wannier model is exactly C3- and time-reversal-symmetric, so symmetry gives exact
targets.

.. list-table::
   :header-rows: 1
   :widths: 66 34

   * - check
     - result
   * - SHG gauge invariance under per-band phases :math:`\phi_n(\mathbf k)`
     - machine precision
   * - D3h: :math:`\sigma^{xxx} = -\sigma^{xyy} = -\sigma^{yxy} = -\sigma^{yyx}`
     - 6e-6 (30x30, 60x60, 120x120)
   * - OptiX vs an independent NumPy evaluation of Eq. (A3a), absolute
     - 5e-7
   * - ``general`` at :math:`\omega_2 = \omega_1` vs the dedicated SHG path
     - 4e-16
   * - excitonic ``general`` at :math:`\omega_2 = \omega_1` vs the excitonic SHG path
     - 8e-17
   * - excitonic method A vs method B at :math:`\omega_2 = \omega_1`
     - 5e-3
   * - excitonic ``rectification`` vs the independent Eq. 11 shift current
     - 3e-9
   * - SHG (single particle) vs a real-time simulation, absolute, sign included
     - 1e-4
   * - ``Sp_method = covariant`` vs ``per_band``: SHG / rectification
     - 9e-11 / 4e-5
   * - non-orthonormal rewrite of hBN vs the orthonormal model: on-site / k-dependent overlap
     - 1e-10 / 2e-9
   * - thread-count independence, 1 / 4 / 26 threads
     - 3e-14

Gauge invariance
----------------

:math:`\sigma` is an observable and must not change under
:math:`U_n(\mathbf k) \to U_n(\mathbf k)e^{i\phi_n(\mathbf k)}`. This is the single most valuable check
on a length-gauge second-order implementation: two bugs that made :math:`\sigma` gauge-*dependent* for
any band count survived a 12-significant-figure cross-check against an independent implementation,
because both shared the same index slip. **No test that does not vary the gauge can detect that class
of error.**

If you modify a second-order kernel, re-run a gauge test with *k-dependent* per-band phases. A
k-independent phase is not enough: on a two-band model it multiplies the whole tensor by a common
factor, which cancels in every ratio-based symmetry test.

Test away from :math:`\omega_2 = \omega_1`
-------------------------------------------

Every defect found in these kernels has been invisible at :math:`\omega_2 = \omega_1`, because there
the two field indices are interchangeable and the frequency swap is the identity. Three examples: an
index transposition in the SHG generalised-derivative term, a broadening convention that resurrected a
term required to cancel at :math:`\omega_2 = 0`, and the electro-optic behaviour above.
``make run_test_second_symmetry`` therefore works at :math:`r` of 1, 1/2, 0 and -1.

What it deliberately does **not** assert is the raw permutation residual
:math:`\sigma^{abc}(\omega_p,\omega_q) = \sigma^{acb}(\omega_q,\omega_p)`. Each kernel is *one
ordering* — the pair average is the symmetrisation — so that residual is :math:`\approx` 1 at every :math:`r \neq 1`
for both routes, and asserting it would be wrong.

Crystal-class selection rules
------------------------------

[Sipe2000]_ Sec. VII: the injection tensor is antisymmetric in (b,c) and forbidden in classes
:math:`\bar 6m2`, :math:`\bar 6` and :math:`\bar 43m`. Taking the antisymmetric part of the
unsymmetrised :math:`\sigma^{abc}` at :math:`\omega_2 = -\omega_1`:

.. list-table::
   :header-rows: 1
   :widths: 26 22 20 32

   * - material
     - class
     - injection
     - measured antisym. part
   * - hBN
     - :math:`\bar 6m2`
     - forbidden
     - 0.0010 %
   * - **buckled hBN**
     - **3m**
     - **allowed**
     - **98.6 %**
   * - In\ :sub:`2`\ Se\ :sub:`3`
     - 3m
     - allowed
     - 4.46 %

The code reproduces a selection rule it was never told. The hBN / buckled-hBN pair is the sharpest form
of this test, because the two models have **identical bands** and differ only by the mirror (see below),
so the ratio of their Im :math:`\sigma` reaches 290 000.

Rectification equals the shift current
---------------------------------------

:math:`\sigma(0;\omega,-\omega)` and the shift current are the same equation in the same regime, and
the code shows it: the excitonic ``rectification`` reproduces the independently validated shift-current
route to 3e-9 on hBN and 9e-8 in the non-interacting limit, with :math:`\mathrm{Im}\,\sigma = 0` exactly.
(The single-particle ``rectification`` is the full causal response and matches the shift current on
resonance only; see :ref:`dc-single-particle`.) Each
is then an independent cross-check of the other. Getting there required the DC convention described in
:ref:`dc-limit`; under the resonant convention the two disagree by a factor of ~2 with a spurious
dispersive line shape.

Across materials the residual tracks the model's **time reversal**, not its point group:

.. list-table::
   :header-rows: 1
   :widths: 24 22 28 26

   * - material
     - point group
     - :math:`\max|E_n(-\mathbf k)-E_n(\mathbf k)|`
     - agreement
   * - hBN
     - :math:`D_{3h}`
     - exact
     - 3.4e-9
   * - ReS\ :sub:`2`
     - :math:`C_1` (none)
     - 3.1e-4 meV
     - 2.1e-6
   * - In\ :sub:`2`\ Se\ :sub:`3`
     - :math:`C_{3v}`
     - 13.8 meV
     - 9.5e-2
   * - MoSe\ :sub:`2`
     - :math:`D_{3h}`
     - 121.4 meV
     - 6.4e-1

ReS\ :sub:`2` has no point symmetry at all and still agrees to :math:`10^{-6}`, while MoSe\ :sub:`2` shares hBN's crystal
class and is the worst of the four.

The ReS\ :sub:`2` figure is essentially independent of the exciton basis — 1.54e-6, 1.78e-6 and 2.13e-6 at 100,
400 and 800 excitons, with a correlation of 1.0000000000 in every case, and agreement to :math:`10^{-6}`
or better on each of the 27 tensor components individually. These values were regenerated on 2026-09-30
with the corrected conduction-band order :math:`c = [60, 61]`.

The DC limit
------------

* :math:`\mathrm{Im}\,\sigma(0;\omega,-\omega) = 0` to :math:`10^{-12}`, as [Sipe2000]_ derives
  analytically — note that the *excitonic* branch imposes this by construction, so the meaningful test
  is the single-particle one;
* the :math:`\omega_\Sigma \to 0` limit is path-independent: approaching from :math:`\omega_\Sigma > 0`
  and :math:`< 0` gives 0.21742 and 0.21652 at equal :math:`|\omega_\Sigma|`, converging on 0.22539.

Buckled hBN: an exactly symmetric target with out-of-plane response
====================================================================

``buckled-hBN_tb.dat`` differs from ``hBN_tb.dat`` in exactly two numbers — the z-components of the two
Wannier centres, :math:`\mp 0.5` Angstrom. :math:`H(\mathbf R)` is bit-identical, so the bands are unchanged
and the only thing that moves is the Wannier-centre Berry connection. That breaks :math:`\sigma_h`,
taking :math:`D_{3h} \to C_{3v}` while leaving C3 and time reversal **exact**.

It is therefore the reference for anything out-of-plane: flat hBN is exact but its mirror forbids every
odd-z component and the injection current, while In\ :sub:`2`\ Se\ :sub:`3` is :math:`C_{3v}` but breaks C3/TR by ~14 meV.

.. list-table::
   :header-rows: 1
   :widths: 62 38

   * - check
     - result
   * - :math:`|v^z|` vs :math:`i[H,A_z]` evaluated independently
     - 2.2e-16
   * - :math:`\xi^z_{nn}` vs :math:`\langle n|A_z|n\rangle`
     - 8.9e-16
   * - in-plane block, buckled vs flat — **single-particle** (shift / SHG)
     - 4.4e-16 / 2.3e-15
   * - in-plane block, buckled vs flat — **excitonic** (rectification / SHG)
     - 0.95 / 1.08  (*not* invariant — see below)
   * - :math:`\sigma_h` residual, flat hBN (shift / SHG)
     - exactly 0 / exactly 0
   * - :math:`\sigma_h` residual, buckled (shift / SHG)
     - 79.9% / 96.3%
   * - C3 residual, buckled SHG (with the new z components)
     - 0.0002%

The z-channel is untestable on flat hBN, where both sublattices sit at :math:`z = 0` and
:math:`\xi^z \equiv 0`.

.. warning::

   **The in-plane invariance is a single-particle statement only.** Because :math:`H(\mathbf R)` is
   bit-identical, the single-particle in-plane block cannot move, and it does not: buckled and flat
   agree to 1e-11 or better. The **excitonic** in-plane block is a different matter — Xatu's BSE kernel
   sees the Wannier centres through the electron–hole Coulomb interaction, so the two models have
   genuinely different exciton spectra. On the 75x75 grid the lowest exciton moves
   **5.3357 to 5.4574 eV (122 meV)**, and :math:`\max|\Delta| / \max|\sigma|` over the in-plane block
   is **0.95** (rectification) and **1.08** (SHG) — an O(1) difference, not a small one.

   Use the buckled/flat pair to test the *symmetry content* of the response (which components are
   forced to zero, and the C3 and :math:`\sigma_h` residuals), not to assert that in-plane excitonic
   numbers are unchanged. Measured 2026-09-30; it corrects a caption in the archived N75 figure set
   that applied the single-particle 4e-16 to excitonic curves.

A second material: In\ :sub:`2`\ Se\ :sub:`3`
=============================================

In\ :sub:`2`\ Se\ :sub:`3`'s Xatu run has four valence bands and one conduction band on a 90x90 mesh over a 30-orbital
model, and the monolayer is polar :math:`C_{3v}` — so it exercises paths hBN cannot, including the
Eq. (A4) rotation and the cache fingerprint at ``nv > 1``.

.. list-table::
   :header-rows: 1
   :widths: 66 34

   * - check
     - result
   * - ``rectification`` vs ``general`` at r = -1
     - byte-identical
   * - Im :math:`\sigma` on the DC branch
     - exactly 0
   * - DC branch vs the excitonic shift current, scale / correlation
     - 0.9993–0.9999 / 0.9997+
   * - ... on the dominant polar components
     - 0.7%
   * - single-particle ``rectification`` / single-particle shift
     - -0.2525, corr -0.9959
   * - cache at nv = 4: cached vs recomputed
     - 4e-14
   * - cache slicing, 800 excitons down to 400
     - 8e-15
   * - complete C3 residual, single-particle SHG / shift
     - 0.19% / 0.55%

The remaining few percent between the two DC routes is the **model**, not the kernel: 87% of it lies in
the C3-forbidden sector, and it is 0.7% on the polar components that carry the signal against 28% on the
weak in-plane block.

.. warning:: **Measure C3 on the full tensor, not the in-plane block**

   In\ :sub:`2`\ Se\ :sub:`3`'s in-plane SHG is ~400x smaller than :math:`\sigma^{zxx}` — physically right for an
   out-of-plane-polar monolayer. An in-plane-only leakage fraction therefore measures cancellation
   noise and reads ~20% for a tensor whose true C3 residual is 0.2%. Use the complete projector on the
   full rank-3 tensor, :math:`\lVert T - PT\rVert/\lVert T\rVert` with :math:`P = (1+C_3+C_3^2)/3`.

Two tests do **not** transfer to In\ :sub:`2`\ Se\ :sub:`3`. The electro-optic excitonic-vs-single-particle comparison needs
a basis large enough to approach the independent-particle limit, and 400 excitons is 1.2% of In\ :sub:`2`\ Se\ :sub:`3`'s
32400-state basis. And its excitonic C3 residual is 8–15% at these basis sizes and still falling, so
In\ :sub:`2`\ Se\ :sub:`3` is a qualitative excitonic target only.

Checking your own material first
=================================

See :doc:`theory/conventions`. Most surprising results come from the input model, not the code.
