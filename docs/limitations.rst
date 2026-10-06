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

See :ref:`dc-antidiagonal`. ``Response = rectification`` is the shift current; the map's
:math:`\omega_2 = -\omega_1` line is close to its **negative**.

``shift_sumrule`` is unreliable
-------------------------------

Identically ~0 for a two-band model, and it disagrees strongly with ``shift_shiftvector`` on GeS's
27-band window. It prints a runtime warning. Do not use it outside large band windows.

No excitonic injection current
-------------------------------

The DC branch reports the **shift** current on both paths. The **single-particle** injection current is
recoverable from the output that is already written — it is the :math:`b\leftrightarrow c`
antisymmetric part of :math:`\mathrm{Im}\,\sigma`, and it is validated by both the symmetry selection
rule and its :math:`1/\eta` scaling.

The **excitonic** injection current is not available, and cannot be recovered by post-processing: the
excitonic expression carries no denominator that vanishes, so it never produces the factor of
:math:`\tau` that defines an injection rate. See :ref:`dc-imaginary-part`.

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
