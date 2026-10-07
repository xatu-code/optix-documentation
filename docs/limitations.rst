=================
Known limitations
=================

An honest list of what is not reliable, and why.

Physics
=======

Input models must be symmetry-adapted
-------------------------------------

OptiX cannot recover a symmetry the Wannier model does not have. Measured on the band structure itself,
inside the exciton window:

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - model
     - C3 breaking (median / max)
     - time reversal (median / max)
   * - hBN
     - 0 / 0
     - 0 / 0
   * - buckled hBN
     - 0 / 0
     - 0 / 0
   * - ReS\ :sub:`2`
     - (C1 — no rotational symmetry)
     - 6.7e-5 / 3.1e-4 meV
   * - In\ :sub:`2`\ Se\ :sub:`3`
     - 1.73 / 23.4 meV
     - 1.17 / 13.8 meV
   * - MoSe\ :sub:`2`
     - 1.72 / 125.5 meV
     - 1.69 / 121.4 meV

Consequences: MoSe\ :sub:`2`'s single-particle SHG shows 7.7% C3 leakage and its excitonic SHG 168%, against
hBN's 0.00% and 1.4%. The excitonic path is far more sensitive, because the symmetry breaking (~2 meV)
is comparable to the exciton level spacing (~1.9 meV), so eigenvectors mix at order unity; the
single-particle path divides the same perturbation by a ~1.5 eV gap.

An easy symptom to check: hBN has 10 exactly-degenerate exciton pairs among its first 40 states; MoSe\ :sub:`2`
and In\ :sub:`2`\ Se\ :sub:`3` have **zero**. Fixing this needs a symmetry-adapted Wannierisation, not a change here.

Non-Hermitian position matrices, and symmetry broken through the Wannier gauge
------------------------------------------------------------------------------

Some Wannier models in use store position matrices that are not Hermitian (MoS\ :sub:`2` by up to
:math:`6\times10^{-3}` Angstrom, In\ :sub:`2`\ Se\ :sub:`3` by 0.12 Angstrom). OptiX repairs them on reading and says so (:ref:`kw-wannier`), but the repair
cannot restore a symmetry the model never had. The MoS\ :sub:`2` Hamiltonian, for example, is not exactly covariant
under the threefold rotation: its band energies are symmetric to 0.08 meV, but its Bloch matrices deviate
at the :math:`10^{-3}` level, in a way that changes eigenvectors rather than energies. Most responses barely notice
(shift current and SHG: threefold residual below 1%). The **injection current** does: it has no
symmetry-allowed in-plane component in :math:`D_{3h}`, grows as :math:`1/\eta`, and turns that :math:`10^{-3}`
asymmetry into a forbidden component about 4% of the size of an allowed injection current of the same
model. An independent calculation on the same model gives the same number, so this is the model and not
OptiX.

Excitonic rectification and shift current differ at bound excitons
--------------------------------------------------------------------

``Response = rectification`` (causal) and ``Response = shift`` (the convention of the reference paper) agree in
the independent-particle limit and above the gap, but not at bound excitons: on buckled hBN the symmetric
real part of the rectification is 0.53 of the shift current, mesh-converged and nearly independent of
:math:`\eta`. The difference is the exciton-exciton term between distinct bound excitons, which the
shift-current convention cancels by construction (:ref:`dc-term3`). Which one describes an experiment depends
on how the bound excitons relax, which neither formula models.

The rectification's forbidden components also converge more slowly with the k-mesh than SHG's, as for the
electro-optic branch below: on flat hBN the :math:`D_{3h}` residual is 6.6% / 3.1% / 1.3% at 30x30 / 45x45 /
60x60.

Electro-optic needs a finer k-grid than the other branches
----------------------------------------------------------

``Response = electrooptic`` is correct on both paths but is the most grid-hungry. As
:math:`\omega_q \to 0` two poles of one term coincide, and the resulting near-double pole amplifies the
k-derivative discretisation error of the exciton matrix elements. The error is ordinary discretisation —
it falls as :math:`1/N^2` (measured x4.2 from a 30x30 to a 60x60 grid) and grows as :math:`\eta` shrinks
— but at a production :math:`\eta` it can be several times larger than SHG on the same grid. On an
*exactly* symmetric model (buckled hBN, full basis) the four regimes give C3 residuals of 0.17%
(SHG), 0.14% (rectification), 0.21% (sum frequency) and **2.62%** (electro-optic) on a 75x75 grid, so
this is a property of the branch and not of the input.

Refining that model to 90x90 (the complete 8100-state basis) confirms both halves of the statement: the
other three branches fall exactly as :math:`1/N^2` — 0.1188%, 0.0993% and 0.1442%, i.e. ratios of
0.691, 0.690 and 0.690 against the predicted :math:`(75/90)^2 = 0.694` — while electro-optic remains
the worst by more than a factor of ten at **1.67%**. For comparison the *single-particle* C3 residual
is 0.0005% on every branch at the same grid, since the single-particle path has no exciton-envelope
k-derivative, which is where this error lives.

Check your system's own symmetry before trusting an electro-optic number at small :math:`\eta`, and
apply the same caution to the small-:math:`|\omega_2|` strip of a 2D map. See :doc:`theory/second_order`.

The anti-diagonal of a 2D map is not a shift current
-----------------------------------------------------

See :ref:`dc-antidiagonal`. The map's :math:`\omega_2 = -\omega_1` line is ``Response = rectification``
(identical when the map contains those points), which differs from the shift current at bound excitons.

``shift_sumrule`` is unreliable
-------------------------------

Identically ~0 for a two-band model, and it disagrees strongly with ``shift_shiftvector`` on GeS's
27-band window. It prints a runtime warning. Do not use it outside large band windows.

The excitonic injection current depends on the broadening
------------------------------------------------------------

Both rectification outputs carry the injection current in the :math:`b\leftrightarrow c` antisymmetric
part of :math:`\mathrm{Im}\,\sigma` (:ref:`dc-excitonic-injection`). The single-particle one scales
exactly as :math:`1/\eta`, as an injection rate times a lifetime :math:`\tau=\hbar/2\eta` should. The
excitonic one does not: on buckled hBN, :math:`\eta` times its weight changes from 1.04 to 0.58 between
:math:`\eta` = 0.2 and 0.025 eV, mesh-converged, with a cause not yet established. Its line shape at
finite :math:`\eta` is a Lorentzian, while the single-particle one is a squared Lorentzian of the same
weight. Compare the two at the same :math:`\eta`, and quote it.

Single-particle rectification: slow mesh convergence of mixed out-of-plane components
--------------------------------------------------------------------------------------

The single-particle rectification (and the other single-particle second-order outputs of the covariant
method) evaluates its k-derivatives analytically at each mesh point. For components with exactly one z index
(:math:`\sigma^{zxx}`, :math:`\sigma^{xxz}`, ...) the resulting k-sums converge slowly and non-monotonically with
the mesh when :math:`\eta` is small, because the resonances are sharper than the k-spacing; in-plane components
and :math:`\sigma^{zzz}` are not affected (symmetry cancels the leftover sums). Measured on non-interacting buckled
hBN against a real-time propagation that is exact on the same mesh:

* :math:`\eta=0.1` eV, :math:`\sigma^{zxx}/\sigma^{xxx}` at 8.59 eV: 1.035, 1.373, 1.174 on 30x30, 45x45, 60x60, against
  1.239, 1.271, 1.254 in real time;
* 30x30 at 8.59 eV: :math:`\sigma^{zxx}` off by -21.5%, -16.2%, -11.3% and :math:`\sigma^{xxz}` by +14.6%, +11.1%,
  +7.7% at :math:`\eta` = 0.05, 0.1, 0.15 eV; at 0.3 eV all routes agree to 0.1%.

The sum :math:`\sigma^{zxx}+2\sigma^{xxz}` is the same in every evaluation; only its split between the index positions
converges slowly. The excitonic rectification (method A with mesh-neighbour derivatives) equals the real-time
result on every mesh (1e-4 at 45x45), also in the non-interacting limit. The same kind of slow, oscillating
mesh convergence is familiar from the independent-particle linear conductivity at small :math:`\eta`. Converge the
mesh, or use a larger :math:`\eta`, before quoting a single-particle out-of-plane rectification component.

``shift_gender`` is a stub
--------------------------

It accumulates nothing and writes a file of zeros.

Two inconsistent degeneracy guards
-----------------------------------

``eps_deg = 1e-4`` Ha gates :math:`\Delta E`; ``clip_threshold = 50`` bohr gates
:math:`|r| = |v|/\Delta E`. A band pair can pass one and fail the other.

The linear excitonic conductivity uses the bare momentum
---------------------------------------------------------

``sigma_first_ex`` uses :math:`P`, not :math:`\Pi`. It is identical to Xatu's ``skubo_w.f90``
(agreement 3e-7), so the two codes agree — but both use :math:`P`. With :math:`\Pi` the hBN peak is
1.345 instead of 3.147 a.u. Which to use is a pending physics decision, flagged in the source.

Not audited
-----------

The overall sign of *e*. The spin degeneracy factor *g* is dropped throughout.

Numerics and performance
========================

Excitonic memory (no longer thread-dependent)
----------------------------------------------

This used to be the main limit: the exciton k-loop held thread-private :math:`(3,N,N)` and
:math:`(N,N)` buffers, so peak memory grew with the **core count** as well as with the exciton number,
and the loop stopped parallelising once those buffers left cache.

The k-sum is now one matrix multiplication per term over all k at once, so those buffers are gone. Peak
memory is dominated by terms **linear** in :math:`N` — the exciton envelopes and their k-derivative,
:math:`\texttt{norb\_ex} \times N` — plus :math:`8N^2` complex numbers for the accumulators, and is
**independent of the thread count**. Measured: a 75x75 two-band model at its complete 5625-state basis
costs 27.8 s and 6.6 GB, and the same model on a 90x90 mesh, at its complete 8100-state basis, costs
76 s and 12.9 GB. Use the cores you have.

The practical ceiling is therefore usually runtime (:math:`O(N^2)`), not memory. For a two-dimensional
map it is the frequency grid rather than the exciton count that dominates, since the cost is
:math:`n_w\times n_{wb}` kernel evaluations.

Excitonic results are truncation-limited
-----------------------------------------

The sub-gap floor of MoSe\ :sub:`2`'s excitonic SHG collapses ~70x going from 100 to 1000 excitons, and ~3190
states are needed to converge the two-photon resonances. Treat excitonic magnitudes as indicative unless
you have run a truncation study — peak *positions* converge much faster than peak *heights*. A bright
ridge that moves when you change ``Exciton_cutoff`` is a truncation artifact, not a resonance.

The single-particle second-order kernel has the frequency loop outermost
-------------------------------------------------------------------------

All band-index work is recomputed for every frequency: :math:`O(n_\text{freq} \times n_\text{band}^3)`
per k-point with no blocking. The excitonic path already uses the blocked matrix-multiplication pattern
that would fix this.

Electro-optic magnitudes are strongly :math:`\eta`-dependent
-------------------------------------------------------------

The electro-optic response is the field-derivative of the linear susceptibility, so it carries a
**double** pole and scales as :math:`1/\eta^2`. Always quote electro-optic magnitudes with their
:math:`\eta`.

Testing gaps
============

``check_sp_shg`` cannot catch a gauge-covariance regression: it tests band-window convergence,
finiteness and :math:`b\leftrightarrow c` permutation, none of which is sensitive to the gauge. A gauge-invariance test with
*k-dependent* per-band phases would close that hole.

There is no runtime check that OptiX's eigenvector gauge matches Xatu's. The excitonic path assumes it;
a mismatch moves the linear peak by 0.32 eV.

The second-order cache records the material, k-grid, band counts and every exciton energy, but **not the
band list**, so a cache built with a different valence/conduction ordering reads back cleanly. Delete
caches by hand whenever the band window or the input files change.
