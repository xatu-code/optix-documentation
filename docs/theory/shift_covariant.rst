.. _shift-covariant:

=================================================
The covariant shift current (``shift_covariant``)
=================================================

``Response = shift_covariant`` evaluates the single-particle shift conductivity from Eq. (9) of
[EsteveParedes2025]_ with a generalised derivative that remains well defined where bands are degenerate or
nearly so. It is what ``Response = shift`` runs by default (:ref:`kw-sp-method`). This page describes what it
computes, the two tolerances it uses, what it costs, how it was validated and how it compares with
``shift_shiftvector``. The same machinery serves the other single-particle second-order responses; see
:ref:`shg-covariant` at the end.

Why per-band formulas fail at degeneracies
==========================================

Eq. (9) needs the generalised derivative of the interband position,

.. math::

   r^{c;a}_{nm} = \partial_{k^a} r^c_{nm} - i\left(\mathcal A^a_{nn} - \mathcal A^a_{mm}\right) r^c_{nm},

which is built for one band at a time: each band carries its own phase, and the Berry connections
:math:`\mathcal A_{nn}` compensate the k-dependence of those phases. Where two bands :math:`n` and
:math:`l` are (nearly) degenerate, the eigensolver may return any mixture of them, and that mixture changes
on the scale of their splitting :math:`\Delta`. The per-band derivative then contains terms of order
:math:`1/\Delta`, and a finite-difference evaluation of them is numerically meaningless. At an exact
degeneracy the individual bands are not even defined.

``shift_shiftvector`` protects itself with cut-offs (it drops band pairs closer than 2.7 meV and discards
shift vectors above 50 bohr). That makes the result finite, but the dropped contributions are real: on
monolayer MoS\ :sub:`2`, whose spin-split bands are degenerate along the :math:`\Gamma`–M lines, the threefold-symmetry residual
of ``shift_shiftvector`` is about 9%, and :math:`\sigma^{yxy}` is about 16% too small.

What is well defined at a degeneracy is any quantity that does not depend on the choice of basis *inside*
the degenerate subspace. ``shift_covariant`` is built from such quantities only.

Blocks
======

At every k-point the bands of the model are grouped into **blocks**: maximal runs of consecutive bands
whose energy gaps are below ``cov_tol`` = 3 meV (:math:`1.1\times10^{-4}` Ha). Bands separated by more than
that form blocks of their own, so a non-degenerate band is a block of size one and is treated exactly as in
a per-band calculation. The grouping is made at the central k-point and applied unchanged to the
finite-difference neighbours.

Blocks are formed over all bands of the model. A block that has members both inside and outside
``Bandlist`` cannot be summed covariantly over the window; OptiX counts such k-points and warns (see
`What the log says`_). Widen ``Bandlist`` if it happens.

The covariant generalised derivative
====================================

For each k-point OptiX diagonalises the Hamiltonian at :math:`\mathbf k` and at the neighbours
:math:`\mathbf k\pm dk\,\hat e_a` (:math:`dk = 10^{-6}` :math:`\text{bohr}^{-1}`, periodic directions only), without the Eq. (A4)
rotation used elsewhere, because the lineshape correction below needs the energy eigenbasis. Then:

1. **Off-block positions.** Between bands in different blocks,
   :math:`r^c_{nm} = -i\,v^c_{nm}/(E_n - E_m)`, evaluated at the centre and at every neighbour in that
   point's own eigenbasis. Elements inside a block are not used.

2. **Block parallel transport.** With :math:`C` the eigenvectors at :math:`\mathbf k` and :math:`C'` those
   at a neighbour, the overlap :math:`O = C^\dagger S(\mathbf k)\, C'` is restricted to each block,
   :math:`O_B = X\Sigma Y^\dagger` (singular value decomposition), and the neighbour's block is rotated by
   :math:`T_B = Y X^\dagger`. This makes every block overlap Hermitian and positive: it is the discrete
   parallel transport of the block as a whole (Löwdin's choice of basis), a U(n) rotation instead of the
   single phase per band of the per-band methods. For a block of size one it reduces to that phase.
   :math:`S = 1` for orthonormal Wannier functions; with ``Orthonormal = false`` the model's overlap enters
   here (:ref:`kw-orthonormal`).

3. **Derivative.** The transported neighbour positions :math:`\tilde r(\mathbf k') = T^\dagger r(\mathbf k') T`
   are differenced, and the remaining connection is added as a commutator:

   .. math::

      r^{c;a} = \frac{\tilde r^c(\mathbf k + dk\,\hat e_a) - \tilde r^c(\mathbf k - dk\,\hat e_a)}{2\,dk}
              - i\left[\xi^a_B,\; r^c(\mathbf k)\right].

   Here :math:`\xi^a_B` is the Hermitian part of the block-diagonal Wannier-centre connection
   :math:`C^\dagger \mathcal A^a(\mathbf k)\, C` (the position matrices of the model file, :ref:`kw-wannier`),
   kept as a full matrix inside each block. In the transported gauge the other piece of the Berry
   connection, :math:`iC^\dagger\partial C`, has no Hermitian part and does not appear.

If the states inside a block are replaced by any other orthonormal combination, at any k-point,
:math:`r^{c;a}` changes by the same unitary rotation as :math:`r^c` itself. Every sum over complete blocks is
therefore independent of the basis the eigensolver happened to return, and exactly degenerate bands need no
special treatment.

Evaluating Eq. (9)
==================

With these elements the shift conductivity is evaluated directly from Eq. (9),

.. math::

   \sigma^{abc}(0;\omega,-\omega) \;\propto\; \sum_{\mathbf k}\sum_{n\in\mathrm c,\,m\in\mathrm v}
   \mathrm{Im}\!\left[r^b_{nm}\,r^{c;a}_{mn} + r^c_{nm}\,r^{b;a}_{mn}\right]\delta(\omega - \omega_{nm}),
   \qquad \omega_{nm} = E_n - E_m ,

with the prefactor and sign of :ref:`the shift-current page <shift-current-page>`. There is no split into a
shift-vector term and an amplitude-gradient term, and therefore none of their cut-offs: the split was only
needed because the per-band derivative is basis dependent.

Split pairs inside a block: the lineshape correction
====================================================

Grouping is exact for the derivative but not for the lineshape. Two bands that share a block but are split
by :math:`0 < \Delta < 3` meV have transition energies that differ by :math:`\Delta`, and a per-band
calculation would weigh each with its own :math:`\delta(\omega-\omega_{nm})`. Where the per-band formula is
valid (bands split by more than its numerical resolution), it differs from the block formula by a commutator
with the intra-block, off-diagonal Berry connection of the energy eigenbasis,
:math:`\xi^{\mathrm{od}}_{nl} = -i\,v_{nl}/(E_n - E_l)`, with the per-band lineshapes attached. Those terms are
antisymmetric under :math:`n\leftrightarrow l`, so they do not reduce to a derivative of the lineshape; they
enter as a finite difference of the two lineshapes. OptiX adds them explicitly.

For two conduction bands :math:`n \ne l` in one block and a valence band :math:`m`,

.. math::

   G^{abc}_{nl;m} = \mathrm{Im}\!\left[r^b_{nm}\left(v^a_{nl}\,r^c_{lm}\right)^* + r^c_{nm}\left(v^a_{nl}\,r^b_{lm}\right)^*\right],

.. math::

   \Delta\sigma^{abc} \;\propto\; \sum_{n<l}\sum_m \tfrac12\left(G^{abc}_{nl;m} - G^{abc}_{ln;m}\right)
   \frac{\delta(\omega-\omega_{nm}) + \delta(\omega-\omega_{lm})}{\omega_{nm} - \omega_{lm}},

with the same prefactor as the main term, and the analogous expression for two valence bands
:math:`l, m` in one block and a conduction band :math:`n`, with
:math:`G^{abc}_{n;lm} = \mathrm{Im}[r^b_{nm}(-r^c_{nl}\,v^a_{lm})^* + (b\leftrightarrow c)]` and the
denominator :math:`\omega_{nm} - \omega_{nl}`. Only velocities and off-block positions enter, so the term is
basis independent wherever it is evaluated.

Without it the block formula is incomplete: on MoS\ :sub:`2` with its degeneracies lifted by an out-of-plane field it
is 13% off the exact per-band result; with it, 1.6%. At zero field the term is small (about 1%), because the
spin partners there barely couple.

Numerically exact degeneracies
==============================

A pair split by less than ``cov_exact_tol`` = 27 :math:`\mu\text{eV}` (:math:`10^{-6}` Ha) is treated as **exactly**
degenerate. The lineshape correction is skipped for it, and all members of such a group are given their
mean energy in every lineshape. Below that splitting the eigenvectors are an arbitrary mixture, the
correction would be basis dependent and divided by a noise-level :math:`\Delta`, and the block formula
alone is the exact answer. The threshold matters in practice: the :math:`\Gamma`–M degeneracy of the MoS\ :sub:`2` Wannier model
is split by :math:`10^{-10}`–:math:`10^{-6}` Ha, depending on the k-point, by the finite precision of the model.
Thresholds from :math:`10^{-7}` to :math:`10^{-5}` Ha give identical results; :math:`10^{-8}` Ha already
breaks the threefold symmetry by 18%. Moving a transition energy by less than 27 :math:`\mu\text{eV}` has no visible effect.

The two tolerances
==================

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - tolerance
     - value
     - sensitivity (measured on MoS\ :sub:`2`)
   * - ``cov_tol`` (block grouping)
     - 3 meV
     - results identical for 1, 3, 10 and 30 meV (to :math:`10^{-9}` in the NumPy reference
       implementation); 0 (no grouping) is the per-band method and fails
   * - ``cov_exact_tol`` (exact degeneracy)
     - 27 :math:`\mu\text{eV}`
     - identical for :math:`10^{-7}`–:math:`10^{-5}` Ha; :math:`10^{-8}` Ha gives an 18% symmetry residual

Neither is an input keyword; both are fixed in ``ome_sp.f90``.

Cost and stored data
====================

The block construction needs its own eigensystems at the centre and at the neighbours: five per k-point for
a two-dimensional material, seven in three dimensions, on top of the matrix-element stage's usual work. It
stores, per k-point, the covariant derivative (:math:`9N_b^2` complex numbers for :math:`N_b` bands in
``Bandlist``), the velocities in the plain eigenbasis (:math:`3N_b^2`) and the block labels, appended to the
``.omesp`` file (:doc:`../outputs/matrix_elements`). A later run with ``OME_sp = none`` can use the file only
if it contains these arrays; otherwise OptiX stops and says so. The response stage itself costs the same as
``shift_shiftvector``.

Outputs are the same files as for ``shift_shiftvector`` (:doc:`../outputs/shift_conductivity`). The
diagnostic ``shift_vector.dat`` is still built from the per-band shift vectors, so near degeneracies it does
not describe what the covariant result contains. The excitonic shift current does not depend on the choice.

What the log says
=================

.. code-block:: text

   Evaluating shift conductivity (sp), block-covariant generalised derivative...
   pairs degenerate to numerical precision inside blocks (no lineshape term):  N

The second line appears when some pairs fell below ``cov_exact_tol``; it counts (k-point, pair)
occurrences and is informative only. If a block straddles the ``Bandlist`` edge at some k-points:

.. code-block:: text

   WARNING (shift_covariant): at N k-points a block of degenerate bands crosses the
            Bandlist edge; the window sum is not gauge covariant there. Widen Bandlist.

Validation
==========

.. list-table::
   :header-rows: 1
   :widths: 58 42

   * - check
     - result
   * - hBN vs an independent exact evaluation of Eq. (9), every component
     - :math:`10^{-7}` (``shift_shiftvector``: :math:`\sigma^{yxy}` at 0.981)
   * - MoS\ :sub:`2`, threefold-symmetry residual of the full tensor (90x90)
     - 0.6% (``shift_shiftvector``: 9.2%)
   * - MoS\ :sub:`2` with the degeneracies lifted by a field, vs the exact per-band result
     - 1%
   * - MoS\ :sub:`2` vs the independent NumPy reference implementation of the same method
     - about 1%
   * - random unitary rotation inside every degenerate group (``OPTICX_BLOCK_SCRAMBLE``)
     - :math:`1.2\times10^{-7}`
   * - smooth, rapidly varying eigenvector phases (``OPTICX_GAUGE_TEST``)
     - round-off
   * - hBN rewritten in a non-orthonormal basis (on-site and k-dependent overlap) vs orthonormal hBN
     - :math:`2\times10^{-11}`

``make check_shift_covariant`` runs the hBN and MoS\ :sub:`2` checks, the gauge and block-rotation tests and two
sensitivity checks (the per-band method must fail on MoS\ :sub:`2`, and the rotation test must actually change the
basis). Removing the grouping makes exactly the MoS\ :sub:`2` symmetry and rotation checks fail.

Comparison with ``shift_shiftvector``
=====================================

On MoS\ :sub:`2` (90x90) the two methods agree on :math:`\sigma^{xxx}` and :math:`\sigma^{xyy}` to about 1%;
:math:`\sigma^{yxy}` is about 16% larger with ``shift_covariant``. That difference is the amplitude-gradient
contribution that ``shift_shiftvector`` drops at nearly degenerate pairs, and it is also what breaks the
threefold symmetry there. On models without (near-)degeneracies, such as hBN, the two agree.

Use ``shift_covariant`` (the default) for production. Use ``shift_shiftvector``
(``Sp_method = per_band``) to compare with results computed before 2026-10-06 or with work based on the
shift-vector formulation.

.. note::

   **Open issue.** On one non-orthonormal SnTe model (201x201 mesh, 12 bands) the two methods satisfy the
   crystal symmetry equally well but disagree in magnitude, by up to a factor 3.6 on :math:`\sigma^{xxx}`.
   The covariant result does not depend on the grouping tolerance there (0, 1, 3 and 10 meV give identical
   results on 61x61), so the difference is not a degeneracy effect. The cause has not been identified and the
   model itself is being revised; treat SnTe shift currents from either method with caution.

.. _shg-covariant:

The same machinery for SHG, electro-optic, rectification and ``general``
========================================================================

With ``Sp_method = covariant`` (the default) the other single-particle second-order responses use the same
blocks, block transport and intra-block connection. They evaluate the length-gauge expression Eq. (B1b) of
[Taghizadeh2018]_ in the independent-particle limit, directly on the k-mesh: each transition
:math:`(c, v, \mathbf k)` plays the role of a non-interacting exciton, and the intraband position acts on the
transition fields :math:`F = r^c_{cv}/(z - \omega_{cv})` through the block-covariant derivative,

.. math::

   (X^b F)_{cv} = \left(r^b_{CC}F - F\,r^b_{VV}\right)_{cv} + i\,(D^b_B F)_{cv},

with :math:`z` the complex frequency. Because the energy denominators sit *inside* the derivative, the
couplings within a block cancel exactly, and no lineshape correction is needed. Every branch, including the
DC line, is evaluated at the causal frequencies (:ref:`dc-single-particle`).

Results: on hBN the covariant SHG equals the per-band (Eq. A3a) result to :math:`10^{-10}`, and the
rectification to :math:`4\times10^{-5}`. On MoS\ :sub:`2` the threefold-symmetry residual is about 1% for SHG and
``general`` (``per_band``: 85–87%), and the SHG agrees to 0.3% with the same quantity obtained by feeding
non-interacting excitons to the excitonic code. The covariant path also carries the injection current (it
equals the per-band one on buckled hBN, with the :math:`1/\eta` scaling). The electro-optic branch is
grid hungry, as on the excitonic path (:doc:`second_order`).

These responses store their own additional data in the ``.omesp`` (the per-neighbour transport, positions and
energies, and the intra-block connection), so an ``.omesp`` written by a ``shift`` run does not serve them.
