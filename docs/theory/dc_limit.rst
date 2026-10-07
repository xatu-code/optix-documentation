.. _dc-limit:

=========================================================
The DC limit: shift current, rectification, and the map
=========================================================

OptiX gives two different zero-frequency quantities, by two routes, and they are **not** the same thing once
excitons are bound:

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Route
     - What it computes
     - Broadening
   * - ``Response = shift`` (``shift_covariant``, ``shift_shiftvector``)
     - the **shift current**, Eqs. (9)-(11) of [EsteveParedes2025]_
     - shift-current convention: :math:`\hbar\omega_q=-(\hbar\omega+i\eta)`, :math:`\omega_2=0`
   * - ``Response = rectification``, ``general`` at ``Frequency_ratio = -1``, and the anti-diagonal
       :math:`\omega_2=-\omega_1` of a 2D map
     - the **whole** :math:`\sigma^{abc}(0;\omega,-\omega)`: its :math:`b\leftrightarrow c` symmetric real
       part and its antisymmetric imaginary part, which holds the **injection current**
     - causal, as every other second-order branch: :math:`\hbar\omega_q=-\hbar\omega+i\eta`,
       :math:`\hbar\omega_2=2i\eta`

The shift current is a special route with its own equations. The rectification is the general
two-frequency response evaluated on the DC line, so it is continuous with the 2D map. In the
independent-particle limit, and above the gap, the symmetric real part of the rectification equals the
shift current on resonance (with off-resonant corrections proportional to :math:`\eta`). At bound excitons it
does not (:ref:`dc-term3`).

Two conventions for one line
============================

Every second-order response in OptiX is evaluated at complex frequencies. Each field frequency carries
:math:`+i\eta`, and the sum frequency is built as the **sum of the two complex numbers**:

.. math::

   \hbar\omega_p = \hbar\omega + i\eta, \qquad
   \hbar\omega_q = r\,\hbar\omega + i\eta, \qquad
   \hbar\omega_\Sigma = \hbar\omega_p + \hbar\omega_q .

This is the convention of [Taghizadeh2018]_, and it is what makes their method A (the momentum observable,
Eq. B1a) and method B (the position observable, Eq. B1b) agree. Call it the **causal convention**: every
amplitude decays at the rate :math:`\eta/\hbar`. On the DC line :math:`r=-1` it gives
:math:`\hbar\omega_\Sigma = 2i\eta`.

The shift current of [EsteveParedes2025]_ is derived instead with one complex number
:math:`z=\omega+i\eta` used as :math:`+z` and :math:`-z`:

.. math::

   \hbar\omega_q = -\hbar\omega_p, \qquad \hbar\omega_\Sigma = 0 \;\;\text{exactly}.

Call this the **shift-current convention**. ``Response = shift`` uses it (Eqs. 9-11 of that paper);
every other branch, ``rectification`` included, uses the causal one.

.. _dc-term3:

Why the two differ: the exciton-exciton term
============================================

Term 3 of Eq. (A9b) of [Taghizadeh2018]_ reads the second-order exciton populations and coherences
:math:`\rho_{nm}` through the current between excitons :math:`n` and :math:`m`, with the denominator

.. math::

   D_{nm} = (\hbar\omega_q + E_n)(\hbar\omega_p - E_m)
   = \frac{\hbar\omega_q+E_n+\hbar\omega_p-E_m}{\ldots}
   \;\Longrightarrow\;
   \frac{1}{D_{nm}}=\frac{1}{\hbar\omega_\Sigma+E_n-E_m}
   \left[\frac{1}{\hbar\omega_p-E_m}+\frac{1}{\hbar\omega_q+E_n}\right].

The bracket is generation by one photon; the first factor is the response of :math:`\rho_{nm}`, which
oscillates at :math:`(E_n-E_m)/\hbar`. How :math:`\omega_\Sigma` is broadened decides what this term does:

* **Shift-current convention** (:math:`\omega_\Sigma=0`): :math:`D_{nm}=(E_n-z)(z-E_m)` is symmetric under
  :math:`n\leftrightarrow m`, and with time reversal the numerator is antisymmetric, so term 3 cancels
  identically. Only terms 1 and 2 remain.
* **Causal** (:math:`\hbar\omega_\Sigma=2i\eta`): term 3 survives. For populations and degenerate pairs the
  first factor is :math:`1/(2i\eta)=-i\tau/\hbar`, a lifetime :math:`\tau=\hbar/2\eta`.

What survives, measured on buckled hBN (75x75, full Xatu basis, projection on the shift current at
:math:`\eta=0.1` eV):

.. list-table::
   :header-rows: 1
   :widths: 34 22 44

   * - pairs :math:`(n,m)`
     - share
     - physics
   * - nearly degenerate continuum pairs, dissipative part of :math:`1/(\hbar\omega_\Sigma+E_{nm})`
     - injection current
     - grows as :math:`\tau`; in Im only (:ref:`dc-excitonic-injection`)
   * - two distinct bound excitons, reactive part
     - :math:`-0.46` of the shift current
     - a steady coherence between, e.g., the first bright exciton and other bound states, carrying current
   * - bound-continuum and continuum-continuum
     - :math:`-0.04` and :math:`+0.02`
     - small

So the causal symmetric real part is **0.53 of the shift current** (least squares over the tensor), and this is
mesh-converged (0.5254 at 75x75 and at 90x90, :math:`\eta=0.1` eV) and nearly independent of :math:`\eta`
(0.51 to 0.56 between 0.2 and 0.025 eV). In the spectrum the first bright exciton is halved, a strong peak
appears at the next bright doublet (6.38 eV) and the sign changes around 6.15 eV; above the gap the two
agree. Terms 1 and 2 alone, with causal broadening, reproduce the shift current to a difference
proportional to :math:`\eta` (0.4% of the peak at 0.025 eV). In the independent-particle limit term 3 adds
nothing to the symmetric part (:math:`\Delta v` is odd in :math:`\mathbf k`) and every route agrees.

Which of the two is right at a bound exciton depends on how bound excitons relax (dephasing,
recombination, dissociation), which neither formalism models; the clean-limit formulas only differ in how
the :math:`\eta\to0` limit is taken. OptiX keeps both: ``shift`` as published, ``rectification`` as the
causal response.

.. _dc-single-particle:

The single-particle DC line
===========================

The single-particle rectification (default ``Sp_method = covariant``) uses the causal frequencies and
method B. Its result is the DC current of a real-time simulation, to 0.2% on hBN
(:ref:`second-order-normalisation`). That current contains more than the shift current:

* on resonance it **equals the shift current** (hBN, :math:`\sigma^{xxx}` at the peak: ratio 0.995, same
  sign, correlation over 3-11 eV 0.9999 at :math:`\eta = 0.05` eV);
* below the gap it adds an off-resonant part proportional to :math:`\eta` (hBN, largest deviation below
  6 eV: :math:`1.2\times10^{-2}`, :math:`6.1\times10^{-3}`, :math:`3.1\times10^{-3}` at :math:`\eta` = 0.2,
  0.1, 0.05 eV);
* its antisymmetric imaginary part is the **injection current** (below).

In the non-interacting limit the excitonic rectification equals it: :math:`5\times10^{-4}` below the gap
and :math:`4\times10^{-4}` at the peak on hBN 30x30, and the same injection weight to 1-2%.

.. _dc-excitonic-rectification:

The excitonic rectification
===========================

``Response = rectification`` evaluates Eq. (B1a) of [Taghizadeh2018]_ (method A, which has no
:math:`i\hbar\omega_2` prefactor) at the causal frequencies, with both field orderings evaluated
explicitly and the pair average of :ref:`dc-why-symmetrised`:

.. math::

   \sigma^{abc}(0;\omega,-\omega)=\tfrac12\big[S^{abc}(\omega_p,\omega_q)+S^{acb}(\omega_q,\omega_p)\big],
   \qquad \hbar\omega_p=\hbar\omega+i\eta,\;\; \hbar\omega_q=-\hbar\omega+i\eta .

Terms 1 and 2 use :math:`\Pi_n=-iE_nX_n` and :math:`X_{nm}`, as everywhere else. **Term 3 uses the bare
exciton-exciton current** :math:`P_{nm}` (Eq. A10 of [Taghizadeh2018]_ with the band velocity; OptiX's
``vme_ex_inter``) instead of :math:`\Pi_{nm}=i(E_n-E_m)X_{nm}`. :math:`\Pi_{nm}` has no diagonal and vanishes for
degenerate pairs, which is where the injection current lives; with it the injection current is resolved
only by the k-mesh (buckled hBN 75x75 at :math:`\eta=0.025` eV: 10% of its converged weight) and the
independent-particle limit carries a mesh artifact (0.90 of the exact value at 75x75, :math:`\eta=0.1` eV).
With :math:`P_{nm}` the independent-particle limit is exact on the mesh and the result is mesh-converged at
75x75.

The result obeys the reality of the current without any projection: its real part is
:math:`b\leftrightarrow c` symmetric and its imaginary part antisymmetric, to :math:`10^{-15}` relative.

The log states the branch::

   801 frequency pairs, 5625 excitons  [method A, Eq. (B1a), term 3 on the bare current: omega_2 = 0 is in range]
   causal prescription (every frequency + i*eta); Re = full DC response, Im = injection channel

**Things to know.**

* Term 3 couples nearly degenerate exciton pairs directly, which amplifies the k-derivative discretisation
  like the electro-optic branch. On flat hBN (:math:`\eta=0.05` eV, all excitons) the :math:`D_{3h}` residual
  is 6.6%, 3.1% and 1.3%, and the symmetry-forbidden antisymmetric imaginary part 1.8%, 0.71% and 0.25% of the
  real part, on 30x30, 45x45 and 60x60 meshes. Check the symmetry of your system before trusting a small
  component on a coarse mesh.
* A truncated ``Exciton_cutoff`` that cuts through a degenerate multiplet breaks the symmetry further
  (hBN 30x30 with 100 excitons: forbidden imaginary part 3.65% instead of 1.8%).
* Until 2026-10-07 this branch used the shift-current convention and returned the shift current with a zero
  imaginary part; that is now ``Response = shift``. The keyword ``Ex_rectification`` is obsolete.

.. _dc-antidiagonal:

The anti-diagonal of a 2D map
=============================

A two-dimensional map (``Energy_variables_2``) crosses the DC line along its anti-diagonal
:math:`\omega_2=-\omega_1`, with the same causal broadening as everywhere else in the map. When the map
contains points with :math:`\omega_1+\omega_2=0` it is evaluated entirely with method A and term 3 on the
bare current, so **its anti-diagonal is the rectification**, point by point. Maps without such points use
method B, which is equivalent to method A with :math:`\Pi_{nm}` and approaches the same result with the
k-mesh.

The anti-diagonal is therefore **not** the shift current where bound excitons respond (buckled hBN 75x75,
5-7 eV: least-squares ratio 0.51). Term 3 is not confined to the line: its coherence factor
:math:`1/(\hbar\omega_\Sigma+E_n-E_m)` resonates wherever the sum frequency matches an exciton-exciton energy
difference, which needs one positive and one negative frequency. On buckled hBN its share of the response is
about one in the difference-frequency quadrant within 1 eV of the anti-diagonal (0.45 at 1-2 eV), 1-8% in the
sum-frequency quadrant and 0.1% on the SHG line.

.. warning::

   For the shift current use ``Response = shift``. A slice of a 2D map, or ``rectification``, gives the
   causal response, which differs from it at bound excitons.

A tempting fix that does not work
=================================

The obvious way to make the DC line come out in the shift-current convention automatically is to let the
broadening follow the sign of the frequency, :math:`\omega_j \to \omega_j + i\,\mathrm{sgn}(\omega_j)\,\eta`.
**This was tried and rejected.** For :math:`\omega_p > 0 > \omega_q` the two broadenings cancel in the sum,

.. math::

   \hbar\omega_\Sigma = \hbar\omega_p + \hbar\omega_q
   = \hbar(\omega_p + \omega_q) + i\eta - i\eta ,
   \qquad \mathrm{Im}\,\hbar\omega_\Sigma = 0 \;\;\text{exactly},

so terms 1 and 2 of Eq. (B1a) acquire an **undamped** two-photon pole wherever
:math:`\omega_p + \omega_q = \pm E_n`. Measured: :math:`|\sigma|` jumps to 107.6 against a background of
4.67, with the height set only by how close the grid lands to the pole, and ``Inf``/``NaN`` on an exact
hit, over the whole :math:`\omega_p\omega_q < 0` half of the map, plus a 2.5x jump across
:math:`\omega_q = 0`.

References
==========

.. [Taghizadeh2018] A. Taghizadeh and T. G. Pedersen, *Gauge invariance of excitonic linear and
   nonlinear optical response*, Phys. Rev. B **97**, 205432 (2018). Appendix A (Eqs. A7, A9b, A10) and
   Appendix B: Eq. (B1a) is the momentum-observable form (method A), Eq. (B1b) the position-observable form
   (method B).

.. [EsteveParedes2025] J. J. Esteve-Paredes, M. A. García-Blázquez, A. J. Uría-Álvarez,
   M. Camarasa-Gómez and J. J. Palacios, *Excitons in nonlinear optical responses: shift current in
   MoS2 and GeS monolayers*, npj Comput. Mater. **11**, 13 (2025). Main Eqs. (8)-(11);
   Supplementary Note 5 for the real part of the static factor.

.. _dc-imaginary-part:

The DC tensor contains both the shift and the injection current
----------------------------------------------------------------

The quadratic DC photocurrent splits into a **shift** and an **injection** contribution, and following
the symmetry classification of Wang and Qian they couple to different parts of the field bilinear:

.. math::

   J^a = \big[\sigma^{abc} + \eta_M^{abc}\big]\,\mathrm{Re}\{E^bE^{c*}\}
       + i\big[\sigma_M^{abc} + \eta^{abc}\big]\,\mathrm{Im}\{E^bE^{c*}\}.

:math:`\mathrm{Re}\{E^bE^{c*}\}` is **symmetric** under :math:`b\leftrightarrow c` and
:math:`\mathrm{Im}\{E^bE^{c*}\}` is **antisymmetric**, so with the reality constraint:

* **shift** = the :math:`b\leftrightarrow c` **symmetric** part (of Re),
* **injection** = the :math:`b\leftrightarrow c` **antisymmetric** part (of Im).

Both rectification outputs, single-particle and excitonic, keep both parts.

How large the antisymmetric part is, by point group (determined by explicit search over operations that
preserve the lattice, the Wannier centres and :math:`H(\mathbf R)`):

.. list-table::
   :header-rows: 1
   :widths: 30 14 20 20 16

   * - model
     - group
     - independent of 27
     - antisym (injection)
     - measured
   * - flat hBN
     - :math:`D_{3h}`
     - 1
     - **0** (forbidden)
     - 0.2 % (noise)
   * - buckled hBN
     - :math:`C_{3v}`
     - 5
     - 1
     - 154 %
   * - in-plane-displaced hBN
     - :math:`C_1`
     - 27
     - 9
     - 98 %

The computed tensors land in the allowed subspace: buckled's antisymmetric part lies in its single
allowed injection channel to 2e-6 (single-particle) and 0.6 % (excitonic, k-grid discretisation).

.. _dc-why-symmetrised:

Why the DC output is symmetrised
--------------------------------

The current is :math:`J^a=\sum_{pq}\sigma^{abc}(\omega_p,\omega_q)\,E^b(\omega_p)E^c(\omega_q)`, summed over
both orderings of the two fields. For the DC response the terms :math:`(\omega,-\omega)` and
:math:`(-\omega,\omega)` multiply the same pair of field components, so only the combination

.. math::

   \tfrac12\left[\sigma^{abc}(0;\omega,-\omega) + \sigma^{acb}(0;-\omega,\omega)\right]

ever reaches the current. Any part of a kernel that changes sign under that swap gives **zero current for
every field**. Such a part is also not unique: Eqs. (B1a) and (B1b) of [Taghizadeh2018]_, or the same formula
with its terms in another order, give different unsymmetrised tensors but the same symmetrised one. On
buckled hBN the unsymmetrised single-particle kernel has an antisymmetric real part of 3.17 (at
:math:`\eta=0.05` eV), while the physical tensor of a time-reversal-symmetric system has none. The
symmetrisation removes exactly that part and nothing else. Both paths evaluate the swapped-frequency
partner explicitly: on the causal DC line it is **not** the complex conjugate of the first ordering (they
differ by O(1) on buckled hBN), although the symmetrised sum obeys the reality of the current.

Two cases where symmetrising **would** discard something real, and why they do not apply:

* the antisymmetric part couples only to circularly polarised light, since
  :math:`\mathrm{Im}\{E^bE^{c*}\}=0` for linear polarisation. For circular light, the injection current
  is in the imaginary column of both outputs;
* a circular *shift* current, antisymmetric but not growing with the relaxation time, exists only when time
  reversal is broken.

Extracting the injection current
---------------------------------

The two contributions separate by **where they sit in the complex tensor**, not merely by
:math:`b\leftrightarrow c` parity:

.. math::

   \text{shift} = \text{sym}_{bc}\big[\mathrm{Re}\,\sigma\big],
   \qquad
   \text{injection} = \text{antisym}_{bc}\big[\mathrm{Im}\,\sigma\big].

The injection term arises from taking the imaginary part of *every* denominator [GarciaBlazquez2025]_. For
:math:`n \neq m` that vanishes as the scattering time :math:`\tau` grows, but where a denominator itself
vanishes (:math:`n = m`, the intraband/group-velocity term) it produces a factor :math:`\tau`. **That**
:math:`\tau` **scaling is the signature**, and it is what distinguishes an injection current from any other
antisymmetric response.

**Single particle.** ``Response = rectification`` writes ``second_rectification_lengthgauge_<material>.dat``
with real and imaginary parts. Take the :math:`b\leftrightarrow c` antisymmetric part of the imaginary
columns. Both ``Sp_method`` values give the same injection current, and its sign and size equal a real-time
propagation with circularly polarised light (buckled hBN, 0.4%, ``make check_out_of_plane``). Verified on a model pair
with identical bands (values in the units used before 2026-10-06; today's output is :math:`-4` times larger,
which leaves the ratios unchanged):

* it obeys the selection rule: 1.4e-5 where injection is forbidden (:math:`\bar 6 m2`) against 3.75
  where it is allowed (:math:`3m`), a ratio of :math:`2.8\times10^{5}`;
* its integrated weight scales as :math:`1/\eta` to three digits (ratios 2.002 and 2.000 across
  :math:`\eta` = 0.025, 0.05, 0.10 eV), i.e. :math:`\propto\tau`, as an injection *rate* must.

The intraband term that generates it is 44 % of the raw tensor on a low-symmetry model, and is
numerically zero (2.7e-5) where symmetry forbids it. Its line shape at finite :math:`\eta` is a *squared*
Lorentzian (from the generalised-derivative double pole).

.. _dc-excitonic-injection:

The excitonic injection current
-------------------------------

The imaginary column of ``second_ex_rectification_lengthgauge_<material>.dat`` comes from the same causal
formula as its real part (:ref:`dc-excitonic-rectification`). Its injection current, the part that grows as
:math:`\tau`, is term 3 evaluated on nearly degenerate continuum pairs:

#. **The term.** Term 3 reads :math:`X^b_n\,P^a_{nm}\,X^{c*}_m/[(\hbar\omega_q+E_n)(\hbar\omega_p-E_m)]`; in the
   shift-current convention it cancels, which is why ``Response = shift`` has no injection current.
#. **The current.** :math:`P_{nm}` is the bare exciton-exciton current. In the non-interacting limit the
   current of the transition :math:`(\mathbf k,c,v)` is :math:`P_{nn}=v_{cc}-v_{vv}`, the group-velocity
   difference of the single-particle injection current. Inside degenerate *bound* multiplets
   :math:`|P_{nm}|\le 9\times10^{-8}` (buckled hBN): bound excitons carry no injection current.
#. **The lifetime.** For degenerate pairs the coherence factor :math:`1/(\hbar\omega_\Sigma+E_n-E_m)` is
   :math:`1/(2i\eta)=-i\tau/\hbar`. Its dissipative part, :math:`-2i\eta/[(E_n-E_m)^2+4\eta^2]`, is the
   injection channel proper; the reactive part adds circular features at split bound pairs that grow more
   slowly than :math:`1/\eta`.

A single exciton never carries an injection current: with time reversal its dipole is real up to a phase
and its diagonal current vanishes. Between two states, a Hermitian time-odd operator in a real basis is
imaginary and antisymmetric, which is exactly the :math:`b\leftrightarrow c` antisymmetric imaginary
channel.

**Validation** (``make check_ex_rectification``, ``make check_out_of_plane`` and the measurements below):

* **Absolute sign and size**: with circularly polarised light, :math:`(\hat x\pm i\hat z)/\sqrt2`, the difference of
  the two helicities in a real-time propagation gives the antisymmetric imaginary part directly. On
  non-interacting buckled hBN (30x30, 8 eV, :math:`\eta=0.3` eV) the excitonic rectification gives 1.761 against
  1.763 in real time, and both single-particle methods 1.756. Until 2026-10-07 term 3 paired its two field
  factors with the wrong frequencies (Eq. A9b pairs :math:`U_n` with :math:`\omega_q` and :math:`U^*_m` with
  :math:`\omega_p`) and the injection current had the opposite sign (excitonic -1.455, single-particle covariant
  -1.686).

* **Non-interacting limit**, buckled hBN 30x30: integrated injection weight 0.9902 and 0.9805 of the
  single-particle one at :math:`\eta=0.05` and 0.1 eV (terms 1 and 2 contribute a part proportional to
  :math:`\eta`), and :math:`\eta` times the weight constant to 1%. The line shape at finite :math:`\eta` is a
  Lorentzian, the single-particle one a squared Lorentzian of the same weight.
* **Real excitons**, buckled hBN (:math:`C_{3v}`, one allowed channel :math:`xxz=yyz`), full Xatu basis:
  75x75 and 90x90 agree to about 1%. Flat hBN (:math:`D_{3h}`): forbidden, at the discretisation levels listed
  in :ref:`dc-excitonic-rectification`.
* **Independent route**: method B (the position operator only, never :math:`P_{nm}`) converges slowly with
  the mesh; extrapolated to an infinite mesh with the convergence law it shows in the non-interacting limit,
  its integrated injection weight agrees with this one to about 10% at :math:`\eta` = 0.1 and 0.05 eV (measured
  before the term-3 pairing fix, which affected both alike). The two-point extrapolation is the uncertain step.

**Things to know.** With excitons the injection weight is not a pure :math:`1/\eta`. On buckled hBN,
:math:`\eta` times the integrated weight of :math:`\sigma^{yyz}` between 4 and 12 eV is 1.04, 0.81, 0.67, 0.58 at
:math:`\eta` = 0.2, 0.1, 0.05, 0.025 eV (the independent-particle value is a constant 1.58). This is mesh-converged and its
physical origin has not been established; quote the :math:`\eta` used. Above the gap the continuum keeps only
9% of the independent-particle oscillator strength on hBN, yet the injection weight is 37-66% of the
independent-particle one.

.. [GarciaBlazquez2025] M. A. García Blázquez, *Symmetry and Excitonic Effects in the Response Properties
   of Materials: a First-Principles approach based on Gaussian functions*, PhD thesis, Universidad Autónoma
   de Madrid (2025), ch. 5, footnote 7: the injection current as the contribution from the imaginary part
   of every denominator.

.. [Sipe2000] J. E. Sipe and A. I. Shkrebtii, *Second-order optical response in semiconductors*,
   Phys. Rev. B **61**, 5337 (2000). Sec. VII derives
   :math:`\mathrm{Im}\,\sigma(0;\omega,-\omega) = 0` where the injection current is forbidden, and the
   selection rule that forbids it in classes :math:`\bar 6 m2`, :math:`\bar 6` and :math:`\bar 4 3m`.

.. [Ahn2020] J. Ahn, G.-Y. Guo and N. Nagaosa, *Low-frequency divergence and quantum geometry of the
   bulk photovoltaic effect in topological semimetals*, Phys. Rev. X **10**, 041041 (2020). Sign
   convention of the shift vector used by OptiX.
